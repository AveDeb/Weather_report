from flask import Flask, Response
import os
import json
from flask_restful import Resource, Api
from WeatherAPI.weather_api import weather_bp

def create_app(testing_config=None):

    app = Flask(__name__, instance_relative_config=True)

    #Setting default Settings to your application
    app.config.from_mapping(
        SECRET_KEY='dev'

        )
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

    if testing_config is None:
        # Overrides default settings based on settings defined in config.py file, present under application instance folder
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(testing_config)

    from WeatherAPI.models import db, migrate
    db.init_app(app)

    with app.app_context():
        from WeatherAPI.models import Location, Weather
        db.create_all()

    app.register_blueprint(weather_bp)
    @app.route('/home')
    def home():
        return Response(json.dumps({'message':'Successful in accessing RESTapi'}),
                        status=201, mimetype="application/json")

    return app
