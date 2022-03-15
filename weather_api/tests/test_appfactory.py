from tests import BaseTestCase
from WeatherAPI.models import db, Location, Weather

class TestAppFactory(BaseTestCase):

    def test_config(self):
        self.assertTrue(self.app.testing)

    def test_appfactory_home(self):
        response = self.client.get('/home')
        self.assertEqual(response.json, {'message': 'Successful in accessing RESTapi'})
        #self.assertEqual(self.app, self.app) # <Flask 'myflaskproject'>
        #self.assertEqual(self.app, self.app)

    