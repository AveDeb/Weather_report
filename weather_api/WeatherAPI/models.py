import re
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func
import ast


db = SQLAlchemy()
migrate = Migrate()

# Define two models : Location and Weather

# Location Model must contain the following attributes.
#    'id' - a primary key holding Integer value
#    'lat' - Float field
#    'lon' - Float field
#    'city' - String field of maximum length 100 characters.
#    'state' - String field of maximum length 100 characters.
class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer(), primary_key=True)
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())
    city = db.Column(db.String(100))
    state=db.Column(db.String(100))
    weathers = db.relationship(
        'Weather',
        backref='locations',
        lazy='dynamic'
    )


    def __init__(self, data):
        self.id=data.get('id')
        self.lat = data.get('lat')
        self.lon = data.get('lon')
        self.city = data.get('city')
        self.state = data.get('state')

    def __repr__(self):
        return str(dict(lat=self.lat,lon=self.lon,city=self.city,state=self.state))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def delete_all_location():
        db.session.query(Location).delete()
        db.session.commit()



    @staticmethod
    def get_all():
        return Location.query.all()

    @staticmethod
    def get_by_id(in_id):
        return Location.query.filter_by(id=in_id).first()

    @staticmethod
    def get_by_latlon(in_lat,in_lon):
        return Location.query.filter_by(lat=in_lat,lon=in_lon).first()

    @staticmethod
    def find_new_id(in_lat,in_lon):
        result=Location.get_by_latlon(in_lat,in_lon)
        if result != None:
            return ('old',result.id,result)
        new_place=Location.query.order_by(Location.id.desc()).first()
        if new_place!= None:
            return ('new',new_place.id + 1, None)
        return ('new', 1,None)
        #return n_location.id


# Weather Model must contain the following attributes.
#    'id' - a primary key holding Integer value
#    'date' - Date Time Field
#    '_temperature' - A string field to store 24 temperature values, separated by semicolon (';').
# Define a property named 'temparature', whose getter method returns 24 temperature values in a list and
# setter method sets the joined temperature string to '_temperature'

# Establish one to many relationship between Location and Weather models.
# A location object must able to access associated weather details of the location using 'weathers' attribute, and
# A weather object must able to access associated location details using 'location' attribute.

class Weather(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    _temperature=db.Column(db.String())
    location = db.Column(db.Integer(), db.ForeignKey('locations.id'))

    def __init__(self, data):
        self.id=data.get('id')
        self.date=data.get('date')
        self.location=data.get('location')

    @property
    def temperature(self):
        if self._temperature == None:
            return None
        return [float(x) for x in self._temperature.split(';')]

    @temperature.setter
    def temperature(self, t_list):
        self._temperature = ';'.join(str(x) for x in t_list)

    def __repr__(self):
        loc=ast.literal_eval(str(Location.get_by_id(self.location)))
        return str(dict(id=self.id,date=self.date.strftime("%Y-%m-%d"),location=loc,temperature=self.temperature))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def delete_all_weather():
        num_of_rows=db.session.query(Weather).delete()
        db.session.commit()
        #Weather.query.delete()
        #Weather.query.commit()
        Location.delete_all_location()
        return num_of_rows


    @staticmethod
    def delete_by_latlon(in_lat,in_lon,s_dt,e_dt):
        result=Location.get_by_latlon(in_lat,in_lon)
        print(result)
        num_of_rows=0
        if result != None:
            #weathers=Weather.query.filter_by(location=result.id,date<=e_dt,date>=s_dt).all()
            num_of_rows=db.session.query(Weather).filter(Weather.location==result.id,
                                            Weather.date >= s_dt,
                                            Weather.date <= e_dt).delete()
            if Weather.query.filter_by(location=result.id).all() == None:
                db.session.query(Location).filter(Location.id ==  result.id).delete()

            db.session.commit()
            #for w in weathers:
            #    print(w)
        return num_of_rows


    @staticmethod
    def get_all():
        return Weather.query.order_by(Weather.id).all()

    @staticmethod
    def get_by_latlon(in_lat,in_lon):
        result=Location.get_by_latlon(in_lat,in_lon)
        if result != None:
            return Weather.query.filter_by(location=result.id).order_by(Weather.id).all()
        return None

    @staticmethod
    def get_by_loc_and_dt(in_loc,in_dt):
        return db.session.query(Weather).filter(Weather.location==in_loc,
                                        Weather.date == in_dt).first()

    @staticmethod
    def get_by_date(in_s_dt,in_e_dt):
        return Weather.query.filter( Weather.date >= in_s_dt,
                                    Weather.date <= in_e_dt).order_by(Weather.location).all()



    @staticmethod
    def is_exist(in_id,in_date,in_lat,in_lon):
        if Weather.query.filter_by(id=in_id).first() != None:
            return True
        result=Location.get_by_latlon(in_lat,in_lon)
        print(result)
        if result != None:
            return Weather.query.filter(Weather.location == result.id, Weather.date==in_date).first()
        return False
        #return (Weather.query.filter_by(id=in_id).first() or Weather.query.filter_by(date=in_date).first())
