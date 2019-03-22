# -*- coding: utf-8 -*-

from UIServiceTest import UIServiceTest

from UIService.UIServiceValidation import Validation
from TestWebServer import TestWebServer

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urlBase = 'https://localhost:8002'


class UIServiceTest_check_image_url(UIServiceTest):
    def setUp(self):
        routes = {
            '/test1.png': {
                'status': {
                    'code': 200,
                    'message': 'OK'
                },
                'header': {
                    'Content-Type': 'image/png',
                    'Content-Length': 100
                }
            },
            '/test1.css': {
                'status': {
                    'code': 200,
                    'message': 'OK'
                },
                'header': {
                    'Content-Type': 'text/css',
                    'Content-Length': 100
                }
            },
            '/respond-400':  {
                'status': {
                    'code': 400,
                    'message': 'Client Error'
                },
                'header': {
                    'Content-Type': 'text/plain',
                    'Content-Length': 100
                }
            },
            '/respond-404':  {
                'status': {
                    'code': 404,
                    'message': 'Not Found'
                },
                'header': {
                    'Content-Type': 'text/plain',
                    'Content-Length': 100
                }
            },
        }
        w = TestWebServer(routes, ssl_cert_file='/kb/module/work/test-ssl.crt', ssl_key_file='/kb/module/work/test-ssl.key')
        w.start()
        self.web_server = w

    def tearDown(self):
        self.web_server.stop()

    # TESTS
    def test_validation_image_url_good_url(self):
        try:
            param1 = {
                'url': urlBase + '/test1.png',
                'timeout': 1000,
                'verify_ssl': 0
            }
            expected1 = {
                'url': urlBase + '/test1.png',
                'timeout': 1000,
                'verify_ssl': False
            }
            result1, err = Validation.validate_check_image_url_param(param1, None)
            self.assertIsNone(err, 'Good url failed: %s' % (str(err)))
            self.assertIsNotNone(result1)
            
            self.assertIsInstance(result1, dict)
            self.assertDictEqual(result1, expected1)


        except Exception as ex:
            self.assertTrue(False)

    def test_check_image_url_good_url(self):
        try:
            param = {
                'url': urlBase + '/test1.png',
                'timeout': 1000,
                'verify_ssl': 0
            }
            expected = {
                'is_valid': True
            }
            ret, err = self.getImpl().check_image_url(self.getContext(), param)
            self.assertIsNone(err, 'Good url failed: %s' % (str(err)))
            self.assertIsNotNone(ret)
            
            self.assertIsInstance(ret, dict)
            self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_check_image_url_not_found(self):
        try:
            param = {
                'url': urlBase + '/respond-404',
                'timeout': 1000,
                'verify_ssl': 0
            }

            expected = {
                'is_valid': False,
                'error': {
                    'code': 'not-found'
                }
            }

            ret, err = self.getImpl().check_image_url(self.getContext(), param)

            self.assertIsNone(err)

            # and error should be properly formed
            self.assertIsNotNone(ret)
            self.assertIsInstance(ret, dict) 
            self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_check_image_url_not_image_type(self):
        try:
            param = {
                'url': urlBase + '/test1.css',
                'timeout': 1000,
                'verify_ssl': 0
            }

            expected = {
                'is_valid': False,
                'error': {
                    'code': 'invalid-content-type',
                    'info': {
                        'content_type': 'text/css'
                    }
                }
            }

            ret, err = self.getImpl().check_image_url(self.getContext(), param)

            self.assertIsNone(err)
            self.assertIsNotNone(ret)
            self.assertIsInstance(ret, dict) 
            self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    # Home url

    
