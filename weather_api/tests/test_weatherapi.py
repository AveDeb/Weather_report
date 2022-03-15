from tests import BaseTestCase
from WeatherAPI.models import db, Location, Weather
from flask import current_app
import os
import json


#import unittest
#import json

#from app import app

class TestWeatherAPI(BaseTestCase):

    def setUp(self):
        self.maxDiff = None
        self.test_1 = []
        self.test_2 = []
        self.test_3 = []
        self.test_4 = []
        self.test_5 = []
        with open(os.path.join(current_app.config['TEST_DATA_DIR'],'http1.json')) as f:
            for line in f:
                self.test_1.append(line)
        with open(os.path.join(current_app.config['TEST_DATA_DIR'],'http2.json')) as f:
            for line in f:
                self.test_2.append(line)
        with open(os.path.join(current_app.config['TEST_DATA_DIR'],'http3.json')) as f:
            for line in f:
                self.test_3.append(line)
        with open(os.path.join(current_app.config['TEST_DATA_DIR'],'http4.json')) as f:
            for line in f:
                self.test_4.append(line)
        with open(os.path.join(current_app.config['TEST_DATA_DIR'],'http5.json')) as f:
            for line in f:
                self.test_5.append(line)

    def test_set1(self):
        for i,ro in enumerate(self.test_1):
            row = json.loads(ro)
            res = {}
            #print(i," response mrthod:----> ",row['request']['method'])
            if row['request']['method'] == "GET":
                res = self.client.get('http://localhost:5000' + row['request']['url'])# + '/')
            if row['request']['method'] == "POST":
                res = self.client.post(
                    'http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
                #print("response out:----> ",res)
            elif row['request']['method'] == "DELETE":
                res = self.client.delete(
                    'http://localhost:5000' + row['request']['url'])# + '/')
            #print('RES:', res)
            self.assertEqual(res.status_code, row['response']['status_code'])
            if row['response']['headers'] != {}:
                self.assertEqual(
                    res.headers['Content-Type'], row['response']['headers']['Content-Type'])
            if row['request']['url'] == '/actors' and row['request']['method'] == 'GET':
                self.assertEqual(sorted(json.loads(res.text)), sorted(row['response']['body']))
            elif row['response']['body'] != {}:
                #print('DIR:', dir(res))
                #print('JSON:', res.json)
                response = res.json #json.loads(res.text)
                #print('SORTED BODY', sorted(row['response']['body']))
                self.assertEqual(response, row['response']['body'])


    def test_set_2(self):
        for i,ro in enumerate(self.test_2):
            row = json.loads(ro)
            res = {}
            #print(i," response mrthod:----> ",row['request']['method'])
            if row['request']['method'] == "GET":
                res = self.client.get('http://localhost:5000' +
                                 row['request']['url']) # + '/')
            elif row['request']['method'] == "POST":
                res = self.client.post(
                    'http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
            elif row['request']['method'] == "DELETE":
                res = self.client.delete(
                    'http://localhost:5000' + row['request']['url'])# + '/')
            elif row['request']['method'] == "PUT":
                res = self.client.put('http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
            self.assertEqual(res.status_code, row['response']['status_code'])
            if row['response']['headers'] != {}:
                self.assertEqual(
                    res.headers['Content-Type'], row['response']['headers']['Content-Type'])
            if row['request']['url'] == '/actors' and row['request']['method'] == 'GET':
                self.assertEqual(sorted(json.loads(res.text)), sorted(row['response']['body']))
            elif row['response']['body'] != {}:
                response = res.json #json.loads(res.text)
                self.assertEqual(response, row['response']['body'])


    def test_set_3(self):
        for ro in self.test_3:
            row = json.loads(ro)
            res = {}
            if row['request']['method'] == "GET":
                res = self.client.get('http://localhost:5000' +
                                 row['request']['url'])# + '/')
            elif row['request']['method'] == "POST":
                res = self.client.post(
                    'http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
            elif row['request']['method'] == "DELETE":
                res = self.client.delete(
                    'http://localhost:5000' + row['request']['url'])# + '/')
            elif row['request']['method'] == "PUT":
                res = self.client.put('http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
            self.assertEqual(res.status_code, row['response']['status_code'])
            if row['response']['headers'] != {}:
                self.assertEqual(
                    res.headers['Content-Type'], row['response']['headers']['Content-Type'])
            if row['request']['url'] == '/actors' and row['request']['method'] == 'GET':
                self.assertEqual(sorted(json.loads(res.text)), sorted(row['response']['body']))
            elif row['response']['body'] != {}:
                response = res.json #json.loads(res.text)
                self.assertEqual(response, row['response']['body'])

    def test_set_4(self):
        for ro in self.test_4:
            row = json.loads(ro)
            res = {}
            if row['request']['method'] == "GET":
                res = self.client.get('http://localhost:5000' +
                                 row['request']['url'])# + '/')
            elif row['request']['method'] == "POST":
                res = self.client.post(
                    'http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
            elif row['request']['method'] == "DELETE":
                res = self.client.delete(
                    'http://localhost:5000' + row['request']['url'])# + '/')
            elif row['request']['method'] == "PUT":
                res = self.client.put('http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
            self.assertEqual(res.status_code, row['response']['status_code'])
            if row['response']['headers'] != {}:
                self.assertEqual(
                    res.headers['Content-Type'], row['response']['headers']['Content-Type'])
            if row['request']['url'] == '/actors' and row['request']['method'] == 'GET':
                self.assertEqual(sorted(json.loads(res.text)), sorted(row['response']['body']))
            elif row['response']['body'] != {}:
                response = res.json #json.loads(res.text)
                self.assertEqual(response, row['response']['body'])

    def test_set_5(self):
        for ro in self.test_5:
            row = json.loads(ro)
            res = {}
            if row['request']['method'] == "GET":
                res = self.client.get('http://localhost:5000' +
                                 row['request']['url'])# + '/')
            elif row['request']['method'] == "POST":
                res = self.client.post(
                    'http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
            elif row['request']['method'] == "DELETE":
                res = self.client.delete(
                    'http://localhost:5000' + row['request']['url'])# + '/')
            elif row['request']['method'] == "PUT":
                res = self.client.put('http://localhost:5000' + row['request']['url'] + '/', json=row['request']['body'])
            self.assertEqual(res.status_code, row['response']['status_code'])
            if row['response']['headers'] != {}:
                self.assertEqual(
                    res.headers['Content-Type'], row['response']['headers']['Content-Type'])
            if row['request']['url'] == '/actors' and row['request']['method'] == 'GET':
                self.assertEqual(sorted(json.loads(res.text)), sorted(row['response']['body']))
            elif row['response']['body'] != {}:
                response = res.json #json.loads(res.text)
                self.assertEqual(response, row['response']['body'])
