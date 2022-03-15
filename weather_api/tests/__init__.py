from flask_testing import TestCase
import os
from WeatherAPI import create_app
from WeatherAPI.models import db, Location, Weather


class BaseTestCase(TestCase):


    def create_app(self):
        app = create_app({
            'TESTING':True,
            'SQLALCHEMY_DATABASE_URI':'sqlite:///' + os.path.join(os.getcwd(),'tests/test_app.db'),
            'SQLALCHEMY_TRACK_MODIFICATIONS':False,
            'SECRET_KEY':'test',
            'TEST_DATA_DIR':os.path.join(os.getcwd(), 'tests/TestData'),
        })

        return app  