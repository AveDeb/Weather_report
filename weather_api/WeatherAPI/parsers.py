from flask_restful import reqparse
from WeatherAPI import validators

# Define the following Parsers
# NOTE: Use the custom 'datestring' validator defined in 'WeatherAPI/validators.py' for validating input date string.
# 1. WeatherRequestParser : It parses the values of input fields-  'id', 'date', 'temperature', and 'location', present in a JSON entry
## The value of 'location' field is another json entry, whose values are parsed by LocationParser
WeatherRequestParser = reqparse.RequestParser()
WeatherRequestParser.add_argument('id', type=int)
WeatherRequestParser.add_argument('date',type=validators.datestring)
WeatherRequestParser.add_argument('temperature', type=float,action='append')
WeatherRequestParser.add_argument('location', type=dict)
#WeatherRequestParser_args = WeatherRequestParser.parse_args()

# 2. LocationParser : It parses the values of input fields - 'lat', 'lon', 'city', and 'state', passed to 'location' field of weather JSON input entry.
LocationParser = reqparse.RequestParser()
LocationParser.add_argument('lat', type=float,location=('location',))
LocationParser.add_argument('lon', type=float,location=('location',))
LocationParser.add_argument('city', type=str,location=('location',))
LocationParser.add_argument('state', type=str,location=('location',))
#LocationParser = LocationParser.parse_args(req=WeatherRequestParser_args)

# 3. WeatherGetParser : It parses the values of input fields - 'date', 'lat' and 'lon', present in a query string.
WeatherGetParser = reqparse.RequestParser()
WeatherGetParser.add_argument('date',type=validators.datestring)
WeatherGetParser.add_argument('lat', type=float)
WeatherGetParser.add_argument('lon', type=float)

# 4. WeatherEraseParser : It parses the values of input fields - 'start', 'end', 'lat' and 'lon', present in  a query string
WeatherEraseParser = reqparse.RequestParser()
WeatherEraseParser.add_argument('start',type=validators.datestring)
WeatherEraseParser.add_argument('end',type=validators.datestring)
WeatherEraseParser.add_argument('lat', type=float)
WeatherEraseParser.add_argument('lon', type=float)

# 5. TemperatureGetParser : It parses the values of input fields - 'start', 'end', present in  a query string
TemperatureGetParser = reqparse.RequestParser()
TemperatureGetParser.add_argument('start',type=validators.datestring)
TemperatureGetParser.add_argument('end',type=validators.datestring)

# 6. PreferredLocationsParser : It parses the values of input fields - 'date', 'lat' and 'lon', present in  a query string
PreferredLocationsParser = reqparse.RequestParser()
PreferredLocationsParser.add_argument('date',type=validators.datestring)
PreferredLocationsParser.add_argument('lat', type=float)
PreferredLocationsParser.add_argument('lon', type=float)
