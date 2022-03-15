from WeatherAPI.models import Location
from flask_restful import fields, marshal

## Define the following marshallers below
# 1. 'location_details' : It defines the output formation of a location entry
location_details={
'city':fields.String,
'lat':fields.Float,
'lon':fields.Float,
'state':fields.String
}

# 2. 'resource_fields' :
resource_fields={
'date':fields.String,
'id':fields.Integer,
'location':fields.Nested(location_details),
'temperature':fields.List(fields.Float)
}
# 3. 'temp_fields' :
temp_fields={
'city':fields.String,
'highest':fields.Float,
'lat':fields.Float,
'lon':fields.Float,
'lowest':fields.Float,
'state':fields.String
}
# 4. 'no_temp_fields' :
no_temp_fields={
'city':fields.String,
'lat':fields.Float,
'lon':fields.Float,
'message':fields.String,
'state':fields.String
}



# 5. 'preferred_location_details' :
preferred_location_details={
'city':fields.String,
'distance':fields.Integer,
'lat':fields.Float,
'lon':fields.Float,
'median_temperature':fields.Float,
'state':fields.String
}
