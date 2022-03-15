import datetime as dt
import json
import math
import ast
from math import radians, sin, cos, acos
import statistics

from flask import Flask, request, Response, Blueprint,jsonify

from WeatherAPI.models import db, Location, Weather

from flask_restful import Resource, Api, fields, marshal,marshal_with

from WeatherAPI.parsers import WeatherRequestParser, WeatherGetParser, LocationParser, WeatherEraseParser, TemperatureGetParser, PreferredLocationsParser
from WeatherAPI.marshallers import resource_fields, temp_fields, no_temp_fields, location_details, preferred_location_details

weather_bp = Blueprint('WeatherAPI', __name__)

weatherapi = Api(weather_bp)

def dist_bw(lat1,lon1,lat2,lon2):
    slat = radians(lat1)
    slon = radians(lon1)
    elat = radians(lat2)
    elon = radians(lon2)
    dist= 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    return round(dist)


class WeatherList(Resource):


    def get(self):
        if 'lat' in request.args:
            lat=request.args['lat']
            lon=request.args['lon']
            #print("lat: ", lat," lon: ",lon)
            wea_list=Weather.get_by_latlon(lat,lon)
            if wea_list==None:
                #print("no records-------------------")
                return Response(json.dumps([]),status=404, mimetype="application/json")
            wea_list=[ast.literal_eval(str(x)) for x in wea_list]
            #return marshal(wea_list,resource_fields),200
            #print(wea_list)
            #print(marshal(wea_list,resource_fields))
            return Response(json.dumps(marshal(wea_list,resource_fields)),
                            status=200, mimetype="application/json")
        wea_list=[ast.literal_eval(str(x)) for x in Weather.get_all()]


        #print(wea_list)
        #print(marshal(wea_list,resource_fields))
        return Response(json.dumps(marshal(wea_list,resource_fields)),
                        status=200, mimetype="application/json")



    def post(self):
        #print("in post")

        ###### setting parsers
        ######################
        WP_args = WeatherRequestParser.parse_args()
        LP_args = LocationParser.parse_args(req=WP_args)

        ###### Getting values using parser
        ##################################
        in_id=WP_args['id']
        in_date=WP_args['date']
        in_temp=WP_args['temperature']

        in_lat=LP_args['lat']
        in_lon=LP_args['lon']
        in_city=LP_args['city']
        in_state=LP_args['state']

        ###### checking in DB
        #########################
        if not Weather.is_exist(in_id,in_date,in_lat,in_lon):

            ########Getting location tatus
            ################################
            loc_status=Location.find_new_id(in_lat,in_lon)
            #print(loc_status)

            if loc_status[0] == 'new':
                ########If location doesnot exist adding to DB
                ################################################
                loc_data=dict(id=loc_status[1],lat=in_lat,lon=in_lon,city=in_city,state=in_state)
                new_loc=Location(loc_data)
                new_loc.save()
                #print(new_loc)

            ###########create weather with location id
            ##########################################
            wea_data=dict(id=in_id,date=in_date,location=loc_status[1])
            new_wea=Weather(wea_data)
            new_wea.temperature=in_temp
            new_wea.save()
            #print(new_wea)

            return Response(status=201, mimetype="application/json")
            #return "",201
            #return {"weater":str(new_wea)}

        #print(loc_data)
        return Response(status=400, mimetype="application/json")
        #return "",400


class WeatherErase(Resource):

    def delete(self):
        #print("in delete")
        ###### setting parsers
        ######################
        WE_args = WeatherEraseParser.parse_args()

        if 'lat' in request.args:
            s_dt=WE_args['start']
            e_dt=WE_args['end']
            lat=WE_args['lat']
            lon=WE_args['lon']
            #print("s_date: ",s_dt,"e_dt: ",e_dt,"lat: ", lat," lon: ",lon)
            num_of_rows=Weather.delete_by_latlon(lat,lon,s_dt,e_dt)
            #return  {"message":str(num_of_rows)+" from selected weather deleted"},200
            return Response(status=200, mimetype="application/json")
        Weather.delete_all_weather()
        #return  {"message":"all weather deleted"+str(num_of_rows)},200
        return Response(status=200, mimetype="application/json")





class LocationTemp(Resource):

    def get(self):
        ###### setting parsers
        ######################
        TG_args = TemperatureGetParser.parse_args()

        s_dt=TG_args['start']
        e_dt=TG_args['end']

        all_locations=Location.get_all()
        if all_locations != None:
            all_locations=sorted(all_locations,key=lambda x: (x.city,x.state))
            loc_temp_details=[]
            temp_dict={}
            for l in all_locations:
                #loc_temp_details.append(dict(city=l.city,highest=None,lat=l.lat,lon=l.lon,lowest=None,state=l.state))
                temp_dict[l.id]={"mx":None,"mn":None}
            #print(temp_dict)
            weather_details=Weather.get_by_date(s_dt,e_dt)
            for w in weather_details:
                mx=max(w.temperature)
                mn=min(w.temperature)
                #print(mx,"-----------",mn)

                if temp_dict[w.location]["mx"] == None or temp_dict[w.location]["mx"] < mx:
                    temp_dict[w.location]["mx"]=mx
                if temp_dict[w.location]["mn"] == None or temp_dict[w.location]["mn"] > mn:
                    temp_dict[w.location]["mn"]=mn
            for l in all_locations:
                if temp_dict[l.id]["mx"] != None:
                    loc_temp_details.append(marshal(
                    dict(city=l.city,highest=temp_dict[l.id]["mx"],lat=l.lat,lon=l.lon,lowest=temp_dict[l.id]["mn"],state=l.state)
                    ,temp_fields))
                else:
                    loc_temp_details.append(marshal(
                    dict(city=l.city,lat=l.lat,lon=l.lon,message="There is no weather data in the given date range",state=l.state)
                    ,no_temp_fields))
            #print(loc_temp_details)
            return Response(json.dumps(loc_temp_details),status=200, mimetype="application/json")
            #return loc_temp_details,200
        return Response(status=200, mimetype="application/json")









class PreferredLocationsAPI(Resource):

    def get(self):
        ###### setting parsers
        ######################
        PL_args = PreferredLocationsParser.parse_args()

        p_dt=PL_args['date']
        in_lat=PL_args['lat']
        in_lon=PL_args['lon']

        #print(p_dt)
        s_dt=p_dt+dt.timedelta(days=1)
        e_dt=p_dt+dt.timedelta(days=3)
        #print(s_dt,"----",e_dt)
        all_locations=Location.get_all()
        loc_temp_details=[]

        if all_locations != None:
            #for l in all_locations:
            #    loc_temp_details.append(dict(city=l.city,distance=None,lat=l.lat,lon=l.lon,median_temperature=None,state=l.state))

            curr_location=Location.get_by_latlon(in_lat, in_lon)
            weather_of_curr=Weather.get_by_loc_and_dt(curr_location.id,p_dt)
            max_curr=max(weather_of_curr.temperature)
            min_curr=min(weather_of_curr.temperature)
            weather_details=Weather.get_by_date(s_dt,e_dt)
            temp_id=0
            temp_arr=[]
            temp_dict={}
            for w in weather_details:
                #print(w)
                #print("ID before start------------------->",temp_id)
                if temp_id==0:
                    temp_id=w.location
                elif temp_id != w.location:
                    if abs(max(temp_arr)-min_curr) <=20 and abs(min(temp_arr)-max_curr) <=20:
                        temp_dict[temp_id]=round(statistics.median(temp_arr),2)
                    else:
                        temp_dict[temp_id]=None
                    temp_id=w.location
                    temp_arr=[]
                temp_arr+=w.temperature
                #print("ID at end------------------->",temp_id)
                #print(temp_dict)
            if temp_id!=0:
                if abs(max(temp_arr)-min_curr) <=20 and abs(min(temp_arr)-max_curr) <=20:
                    temp_dict[temp_id]=round(statistics.median(temp_arr),2)
                else:
                    temp_dict[temp_id]=None
            #print(temp_dict)
            #print(temp_dict)
            for l in all_locations:
                #print(l)
                if (l.lat==in_lat and l.lon==in_lon) or l.state == curr_location.state:
                    continue
                if l.id not in temp_dict.keys():
                    mt=None
                elif temp_dict[l.id] == None:
                    continue
                else:
                    mt=temp_dict[l.id]

                dis=dist_bw(in_lat,in_lon,l.lat,l.lon)
                loc_temp_details.append(dict(city=l.city,distance=dis,lat=l.lat,lon=l.lon,median_temperature=mt,state=l.state))
            loc_temp_details=sorted(loc_temp_details,key=lambda  x:(x["distance"],x["median_temperature"],x["city"],x["state"]))
            #print(loc_temp_details)
            #return marshal(loc_temp_details,preferred_location_details),200
            return Response(json.dumps(marshal(loc_temp_details,preferred_location_details)),status=200, mimetype="application/json")


        return Response(status=404, mimetype="application/json")




#weatherapi.add_resource(WeatherAPI, '/weather')
#weatherapi.add_resource(WeatherEraseAPI, '/erase')
#weatherapi.add_resource(TemperatureAPI, '/weather/temperature')
#weatherapi.add_resource(PreferredLocationsAPI, '/weather/locations')

weatherapi.add_resource(WeatherList, '/weather','/weather/')
weatherapi.add_resource(WeatherErase, '/erase')
weatherapi.add_resource(LocationTemp, '/weather/temperature')
weatherapi.add_resource(PreferredLocationsAPI, '/weather/locations')
