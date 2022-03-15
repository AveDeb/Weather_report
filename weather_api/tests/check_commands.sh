# ALL HTTP Requests to be run in order
# HTTP POST Requests
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request1_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request2_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request3_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request4_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request5_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request6_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request7_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request8_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request9_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request10_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request11_POST.json
http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request12_POST.json

http POST http://0.0.0.0:8000/weather < tests/TestData/JsonRequests/Request1_POST.json

# HTTP GET Requests
http 'http://0.0.0.0:8000/weather?lat=36.1189&lon=-86.6892'
http 'http://0.0.0.0:8000/weather?lat=39.0725&lon=-95.6261'

# HTTP DELETE Request
http DELETE 'http://0.0.0.0:8000/erase?start=1985-01-02&end=1985-01-03&lat=36.1189&lon=-86.6892'

# HTTP GET Requests
http 'http://0.0.0.0:8000/weather/temperature?start=1985-01-01&end=1985-01-04'
http 'http://0.0.0.0:8000/weather/locations?date=1985-01-01&lat=36.1189&lon=-86.6892'
http 'http://0.0.0.0:8000/weather'

# HTTP DELETE Request
http DELETE http://0.0.0.0:8000/erase

# HTTP GET Request
http http:0.0.0.0:8000/weather
