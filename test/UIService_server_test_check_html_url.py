# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

from UIService.UIServiceValidation import Validation
from TestWebServer import TestWebServer

urlBase = 'http://localhost:8002'

class UIServiceTest_check_home_url(UIServiceTest):
    def setUp(self):
        routes = {
            '/test1.html': {
                'status': {
                    'code': 200,
                    'message': 'OK'
                },
                'header': {
                    'Content-Type': 'text/html',
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
        }
        w = TestWebServer(routes)
        w.start()
        self.web_server = w

    def tearDown(self):
        self.web_server.stop()

    # TESTS
    def test_validation_home_url_good_param(self):
        try:
            param = {
                'url': urlBase + '/test1.html',
                'timeout': 1000
            }
            expected = {
                'url': urlBase + '/test1.html',
                'timeout': 1000
            }
            result, err = Validation.validate_check_html_url_param(param, None)
            self.assertIsNone(err, 'Good param failed: %s' % (str(err)))
            self.assertIsNotNone(result)
            
            self.assertIsInstance(result, dict)
            self.assertDictEqual(result, expected)


        except Exception as ex:
            self.assertTrue(False)

    def test_validation_home_url_good_url(self):
        try:
            param = {
                'url': urlBase + '/test1.html',
                'timeout': 1000
            }

            expected = {
                'is_valid': True
            }

            ret, err = self.getImpl().check_html_url(self.getContext(), param)

            self.assertIsNone(err)
            self.assertIsNotNone(ret)
            self.assertIsInstance(ret, dict) 
            self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_validation_home_url_bad_params(self):
        try:
            bad_params = [{
                'input': {
                    'url': 123,
                    'timeout': 1000
                    }, 
                'expected': {
                    'error': True
                }
            },
            {
                'input': {
                    'url': urlBase + '/test1.html',
                    'timeout': 'abc'
                    }, 
                'expected': {
                    'error': True
                }
            }
           ]
           

            expected = {
                'is_valid': True
            }

            for bad_param in bad_params: 
                ret, err = self.getImpl().check_html_url(self.getContext(), bad_param['input'])

                self.assertIsNone(ret)
                self.assertIsNotNone(err)
                # self.assertIsInstance(ret, dict) 
                # self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))
  
    def test_validation_html_url_missing_url(self):
        try:
            param = {
                'url': urlBase + '/abc',
                'timeout': 1000
            }

            expected = {
                'is_valid': False,
                'error': {
                    'code': 'not-found'
                }
            }

            ret, err = self.getImpl().check_html_url(self.getContext(), param)

            self.assertIsNone(err)
            self.assertIsNotNone(ret)
            self.assertIsInstance(ret, dict) 
            self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_validation_html_not_html(self):
        try:
            param = {
                'url': urlBase + '/test1.css',
                'timeout': 1000
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

            ret, err = self.getImpl().check_html_url(self.getContext(), param)

            self.assertIsNone(err)
            self.assertIsNotNone(ret)
            self.assertIsInstance(ret, dict) 
            self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    def test_validation_html_url_invalid_status(self):
        try:
            param = {
                'url': urlBase + '/respond-400',
                'timeout': 1000
            }

            expected = {
                'is_valid': False,
                'error': {
                    'code': 'unexpected-response-status-code',
                    'info': {
                      'status_code': 400
                    }
                }
            }

            ret, err = self.getImpl().check_html_url(self.getContext(), param)

            self.assertIsNone(err)
            self.assertIsNotNone(ret)
            self.assertIsInstance(ret, dict) 
            self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))
