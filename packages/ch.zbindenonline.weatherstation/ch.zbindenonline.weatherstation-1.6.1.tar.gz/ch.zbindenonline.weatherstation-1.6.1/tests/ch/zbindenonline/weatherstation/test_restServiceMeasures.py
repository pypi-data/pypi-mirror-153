import json
import unittest

import pytest
import requests
from mockito import unstub, when, arg_that
from requests import HTTPError, RequestException

from ch.zbindenonline.weatherstation.restServiceMeasures import RestServiceMeasures
from .mocks import MockResponse


class RestServiceMeasuresShould(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_login_fails(self):
        when(requests).post('http://testurl/login', data=any, headers=any, timeout=any).thenReturn(
            MockResponse(status_code=404))

        with pytest.raises(HTTPError):
            RestServiceMeasures('http://testurl', 'testuser', 'testpwd')

    def test_login_ok(self):
        when(requests).post('http://testurl/login', data=any, headers=any, timeout=any).thenReturn(
            MockResponse(json_data={"access_jwt": "access_token"}))

        service = RestServiceMeasures('http://testurl', 'testuser', 'testpwd')

        self.assertEquals('Bearer access_token', service.headers['Authorization'])

    def test_loginRequestException(self):
        when(requests).post('http://testurl/login', data=any, headers=any, timeout=any).thenRaise(
            RequestException('testmessage'))

        with self.assertRaises(SystemExit) as se:
            RestServiceMeasures('http://testurl', 'testuser', 'testpwd')

        self.assertEquals(1, se.exception.code)

    def test_get_sensors(self):
        service = login()
        service_sensors = [{'id': 1, 'name': 'sensor_1'}, {'id': 2, 'name': 'sensor_2'}]
        when(requests).get('http://testurl/sensors', headers=any, timeout=10).thenReturn(
            MockResponse(json_data=service_sensors))

        sensors = service.get_sensors()

        self.assertEquals(service_sensors, sensors)

    def test_get_sensors_raise_for_status(self):
        service = login()
        when(requests).get('http://testurl/sensors', headers=any, timeout=10).thenReturn(
            MockResponse(status_code=400))

        with pytest.raises(HTTPError):
            service.get_sensors()

    def test_get_last_timestamp(self):
        service_timestamp = '2021-12-20 14:59'
        when(requests).get('http://testurl/measures/last?sensor=17', headers=any, timeout=10).thenReturn(
            MockResponse(json_data={'measured_at': service_timestamp}))
        service = login()

        timestamp = service.get_last_timestamp('17')

        self.assertEquals(service_timestamp, timestamp)

    def test_get_last_timestamp_defaults_to_1970(self):
        when(requests).get('http://testurl/measures/last?sensor=17', headers=any, timeout=10).thenReturn(
            MockResponse(json_data=None))
        service = login()

        timestamp = service.get_last_timestamp('17')

        self.assertEquals('1970-01-01 00:00', timestamp)

    def test_get_last_timestamp_raise_for_status(self):
        when(requests).get('http://testurl/measures/last?sensor=17', headers=any, timeout=10).thenReturn(
            MockResponse(status_code=400))
        service = login()

        with pytest.raises(HTTPError):
            service.get_last_timestamp('17')

    def test_post_measures(self):
        measures = [{'measured_at': '2021-12-20 08:00', 'temperature': '19.7', 'humidity': '67.3'}]
        service = login()
        when(requests) \
            .post('http://testurl/measures',
                  data=arg_that(lambda posted: self.verify_measures('23', measures, json.loads(posted))),
                  headers={'User-Agent': 'python', 'Authorization': 'Bearer access_token'}, timeout=120) \
            .thenReturn(MockResponse(status_code=200))

        service.post_measures('23', measures)

    def test_post_measures_raise_for_status(self):
        measures = [{'measured_at': '2021-12-20 08:00', 'temperature': '19.7', 'humidity': '67.3'}]
        service = login()
        when(requests) \
            .post('http://testurl/measures',
                  data=arg_that(lambda posted: self.verify_measures('23', measures, json.loads(posted))),
                  headers={'User-Agent': 'python', 'Authorization': 'Bearer access_token'}, timeout=120) \
            .thenReturn(MockResponse(status_code=400))

        with pytest.raises(HTTPError):
            service.post_measures('23', measures)

    def verify_measures(self, sensor_id, expected, posted):
        return len(expected) == len(posted) and \
               sensor_id == posted[0]['sensor'] and \
               expected[0]['measured_at'] == posted[0]['measured_at'] and \
               expected[0]['temperature'] == posted[0]['temperature'] and \
               expected[0]['humidity'] == posted[0]['humidity']


def login() -> RestServiceMeasures:
    when(requests).post('http://testurl/login', data=any, headers=any, timeout=any).thenReturn(
        MockResponse(json_data={"access_jwt": "access_token"}))
    return RestServiceMeasures('http://testurl', 'testuser', 'testpwd')


if __name__ == '__main__':
    unittest.main()
