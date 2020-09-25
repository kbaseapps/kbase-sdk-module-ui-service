# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest
from UIService.UIServiceValidation import Validation
from TestWebServer import TestWebServer
import requests

urlBase = 'http://localhost:8002'
bad_url_base = 'http://fakehost'
timeout = 5

class UIServiceTest_check_http(UIServiceTest):
    def setUp(self):
        routes = {
            '/with-user-agent.html': {
                'status': {
                    'code': 200,
                    'message': 'OK'
                },
                'header': {
                    'Content-Type': 'text/html',
                    'Content-Length': 100
                }
            },
            '/without-user-agent.html':  {
                'status': {
                    'code': 403,
                    'message': 'Forbidden'
                },
                'header': {
                    'Content-Type': 'text/plain',
                    'Content-Length': 0
                }
            },
            '/with-bad-user-agent.html':  {
                'status': {
                    'code': 403,
                    'message': 'Forbidden'
                },
                'header': {
                    'Content-Type': 'text/plain',
                    'Content-Length': 0
                }
            }
        }
        w = TestWebServer(routes)
        w.start()
        self.web_server = w

    def tearDown(self):
        self.web_server.stop()

    # TESTS
    def test_validation_http_with_user_agent(self):
        try:
            header = {
                'User-Agent': 'kbase-ui-module-ui-service (https://github.com/kbaseapps/kbase-ui-module-ui-service) requests/2.24.0 Python/3.8.5 Linux/4.19.76-linuxkit'
            }
            
            url = urlBase + '/with-user-agent.html'
            response = requests.head(url=url, allow_redirects=True, timeout=timeout, 
                                     headers=header)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.reason, 'OK')
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_validation_http_without_user_agent(self):
        try:
            header = {}
            
            url = urlBase + '/without-user-agent.html'
            response = requests.head(url=url, allow_redirects=True, timeout=timeout, 
                                     headers=header)

            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.reason, 'Forbidden')
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_validation_http_with_bad_user_agent(self):
        try:
            header = {
                'User-Agent': 'foo'
            }
            
            url = urlBase + '/with-bad-user-agent.html'
            response = requests.head(url=url, allow_redirects=True, timeout=timeout, 
                                     headers=header)

            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.reason, 'Forbidden')
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_validation_http_missing_no_user_agent(self):
        try:
            header = {}
            
            url = urlBase + '/missing.html'
            response = requests.head(url=url, allow_redirects=True, timeout=timeout, 
                                     headers=header)

            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.reason, 'Forbidden')
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_validation_http_missing(self):
        try:
            header = {
                'User-Agent': 'kbase-ui-module-ui-service (https://github.com/kbaseapps/kbase-ui-module-ui-service) requests/2.24.0 Python/3.8.5 Linux/4.19.76-linuxkit'
            }
            
            url = urlBase + '/missing.html'
            response = requests.head(url=url, allow_redirects=True, timeout=timeout, 
                                     headers=header)

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.reason, 'Not Found')
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))
