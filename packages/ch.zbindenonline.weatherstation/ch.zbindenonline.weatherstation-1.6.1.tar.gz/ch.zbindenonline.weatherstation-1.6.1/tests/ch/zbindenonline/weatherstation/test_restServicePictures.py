import os
import shutil
import tempfile
import unittest
import re
from unittest import mock

import pytest
import requests
from mockito import verify, when
from requests.exceptions import RequestException
from requests.models import Response as HttpResponse, HTTPError

from ch.zbindenonline.weatherstation.restServicePictures import RestServicePictures, Response
from tests.ch.zbindenonline.weatherstation.mocks import MockResponse


def mocked_login_not_ok(*args, **kwargs):
    return MockResponse({"access_token": "accessTokenToTest"}, 500)


def mocked_requests_post(*args, **kwargs):
    if args[0] == 'http://testurl/oauth/token':
        return MockResponse({"access_token": "accessTokenToTest"}, 200)
    elif args[0] == 'http://testurl/cameras/3/pictures':
        return MockResponse({"key2": "value2"}, 200)
    elif args[0] == 'http://testurl/cameras/4/pictures':
        return MockResponse({"key2": "value2"}, 409)
    elif args[0] == 'http://testurl/cameras/5/pictures':
        return MockResponse({"key2": "value2"}, 422)
    elif args[0] == 'http://testurl/cameras/6/pictures':
        the_response = HttpResponse()
        the_response.status_code = 404
        the_response._content = b'{ "error" : "error text" }'
        return the_response
    elif args[0] == 'http://testurl/cameras/7/pictures?from=2022-03-30T19:11:00&to=2022-03-30T19:11:00':
        the_response = HttpResponse()
        the_response.status_code = 200
        the_response._content = b'{ "data" : [{"id" : 1}] }'
        return the_response
    elif re.search("^http://testurl/cameras/*/pictures?from=*&to=*$", args[0]):
        the_response = HttpResponse()
        the_response.status_code = 200
        the_response._content = b'{ "data" : [] }'
        return the_response
    return MockResponse({"error": "error"}, 404)


def mocked_requests_get(*args, **kwargs):
    if args[0] == 'http://testurl/cameras/7/pictures?from=2022-03-30T19:11:00&to=2022-03-30T19:11:00':
        the_response = HttpResponse()
        the_response.status_code = 200
        the_response._content = b'{ "data" : [{"id" : 1}] }'
        return the_response
    if re.search("^http://testurl/cameras/.*/pictures\?from=.*&to=.*$", args[0]):
        the_response = HttpResponse()
        the_response.status_code = 200
        the_response._content = b'{ "data" : [] }'
        return the_response
    return MockResponse({"error": "error"}, 404)

class RestServiceShould(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_answerOk(self, mock_post, mock_get):
        picture = os.path.join(self.test_dir, '2021-04-11_112400.jpg')
        f = open(picture, 'w')
        f.write('The owls are not what they seem')
        f.close()
        service = RestServicePictures('http://testurl',
                                      '3',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')

        service.login()
        self.assertRegex(service.headers['Authorization'], "Bearer accessTokenToTest")

        result = service.post_picture(picture)
        self.assertEqual(Response.OK, result)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_answerRaisesErrorWhenInvalidFile(self, mock_post):
        picture = os.path.join(self.test_dir, '2021-04-11.jpg')
        f = open(picture, 'w')
        f.write('The owls are not what they seem')
        f.close()
        service = RestServicePictures('http://testurl',
                                      '3',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')

        service.login()
        with pytest.raises(Exception) as error_info:
            service.post_picture(picture)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_answerOkWithoutSeconds(self, mock_post, mock_get):
        picture = os.path.join(self.test_dir, '2021-04-11_1124.jpg')
        f = open(picture, 'w')
        f.write('The owls are not what they seem')
        f.close()
        service = RestServicePictures('http://testurl',
                                      '3',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')

        service.login()
        self.assertRegex(service.headers['Authorization'], "Bearer accessTokenToTest")

        result = service.post_picture(picture)
        self.assertEqual(Response.OK, result)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_answerDuplicate(self, mock_post, mock_get):
        picture = os.path.join(self.test_dir, '2021-04-11_112400.jpg')
        f = open(picture, 'w')
        f.write('The owls are not what they seem')
        f.close()
        service = RestServicePictures('http://testurl',
                                      '4',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')

        result = service.post_picture(picture)

        self.assertEqual(Response.DUPLICATE, result)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_answerDuplicateByQuery(self, mock_post, mock_get):
        picture = os.path.join(self.test_dir, '2022-03-30_191102.jpg')
        f = open(picture, 'w')
        f.write('The owls are not what they seem')
        f.close()
        service = RestServicePictures('http://testurl',
                                      '7',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')

        result = service.post_picture(picture)

        self.assertEqual(Response.DUPLICATE, result)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_answerUnprocessable(self, mock_post, mock_get):
        picture = os.path.join(self.test_dir, '2021-04-11_112400.jpg')
        f = open(picture, 'w')
        f.write('The owls are not what they seem')
        f.close()
        service = RestServicePictures('http://testurl',
                                      '5',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')

        result = service.post_picture(picture)

        self.assertEqual(Response.UNPROCESSABLE_ENTITY, result)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_answerResponseRaiseForStatus(self, mock_post, mock_get):
        picture = os.path.join(self.test_dir, '2021-04-11_112400.jpg')
        f = open(picture, 'w')
        f.write('The owls are not what they seem')
        f.close()
        service = RestServicePictures('http://testurl',
                                      '6',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')
        with pytest.raises(HTTPError) as error_info:
            service.post_picture(picture)

    def test_loginRaiseForStatus(self):
        when(requests).post('http://testurl/oauth/token', data=any, headers=any, timeout=any).thenReturn(
            MockResponse('', 404, 'LoginFailedError'))
        service = RestServicePictures('http://testurl',
                                      '6',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')
        with pytest.raises(HTTPError) as error_info:
            service.login()

    def test_loginRequestException(self):
        when(requests).post('http://testurl/oauth/token', data=any, headers=any, timeout=any).thenRaise(
            RequestException('testmessage'))
        service = RestServicePictures('http://testurl',
                                      '6',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')
        with self.assertRaises(SystemExit) as se:
            service.login()
        self.assertEquals(1, se.exception.code)

    def test_logout_ok(self):
        when(requests).delete('http://testurl/oauth/token',
                              headers={'User-Agent': 'python', 'Accept': 'application/json'}, timeout=15).thenReturn(
            MockResponse('', 200, True))
        service = RestServicePictures('http://testurl',
                                      '6',
                                      'client_id',
                                      'client_secret',
                                      'testuser',
                                      'testpwd')
        service.logout()

        verify(requests).delete('http://testurl/oauth/token',
                                headers={'User-Agent': 'python', 'Accept': 'application/json'}, timeout=15)


if __name__ == '__main__':
    unittest.main()
