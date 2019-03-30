# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

from UIService.UIServiceValidation import Validation
from TestWebServer import TestWebServer

urlBase = 'http://localhost:8002'
bad_url_base = 'http://fakehost'

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
                    'Content-Length': 0
                }
            },
             '/respond-301':  {
                'status': {
                    'code': 301,
                    'message': 'Redirect'
                },
                'header': {
                    'Content-Length': 0,
                    'Location': '/test1.html'
                }
            },
             '/respond-302':  {
                'status': {
                    'code': 302,
                    'message': 'Redirect'
                },
                'header': {
                    'Content-Length': 0,
                    'Location': '/test1.html'
                }
            },
            '/missing-content-type': {
                'status': {
                    'code': 200,
                    'message': 'OK'
                },
                'header': {
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

    def test_validation_home_url_missing_timeout_param(self):
        try:
            param = {
                'url': urlBase + '/test1.html'
            }
            expected =  { 
                'message': 'the required parameter "timeout" was not provided', 
                'type': 'input', 
                'code': 'missing', 
                'info': { 
                    'key': 'timeout' 
                } 
            } 
            result, err = Validation.validate_check_html_url_param(param, None)
            self.assertIsNone(result)
            self.assertIsNotNone(err)
            
            self.assertIsInstance(err, dict)
            self.assertDictEqual(err, expected)

        except Exception as ex:
            self.assertTrue(False)

    def test_validation_home_url_missing_url_param(self):
        try:
            param = {
                'timeout': 1000
            }
            expected =  { 
                'message': 'the required parameter "url" was not provided', 
                'type': 'input', 
                'code': 'missing', 
                'info': { 
                    'key': 'url' 
                } 
            } 
            result, err = Validation.validate_check_html_url_param(param, None)
            self.assertIsNone(result)
            self.assertIsNotNone(err)
            
            self.assertIsInstance(err, dict)
            self.assertDictEqual(err, expected)

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

    def test_validation_home_url_301_is_fine(self):
        try:
            param = {
                'url': urlBase + '/respond-301',
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

    def test_validation_home_url_302_is_fine(self):
        try:
            param = {
                'url': urlBase + '/respond-302',
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
            },
            {
                'input': {
                    'url': 'x',
                    'timeout': 1000
                    }, 
                'expected': {
                    'error': True
                }
            },
            {
                'input': {
                    'url': urlBase + '/test1.html',
                    'timeout': 60000 + 1
                }, 
                'expected': { 
                    'message': ('the timeout parameter must be less than one minute'), 
                    'type': 'input', 
                    'code': 'out-of-range', 
                    'info': { 
                        'min': 0, 
                        'max': 60000 
                    } 
                } 
            },
            {
                'input': {
                    'url': urlBase + '/test1.html',
                    'timeout': -1
                }, 
                'expected': { 
                    'message': ('the timeout parameter must be greater than 0'), 
                    'type': 'input', 
                    'code': 'out-of-range', 
                    'info': { 
                        'min': 0, 
                        'max': 60000 
                    } 
                } 
            }]

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

    def test_validation_html_url_missing_content_type(self):
        try:
            param = {
                'url': urlBase + '/missing-content-type',
                'timeout': 1000
            }

            expected = {
                'is_valid': False,
                'error': {
                    'code': 'missing-content-type',
                    'info': {
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

    def test_validation_html_url_bad_url(self):
        try:
            param = {
                'url': bad_url_base,
                'timeout': 1000
            }

            expected = { 
                'message': ('exception requesting html page'), 
                'type': 'value', 
                'code': 'error-response'
            }

            ret, err = self.getImpl().check_html_url(self.getContext(), param)

            self.assertIsNone(ret)
            self.assertIsNotNone(err)
            self.assertIsInstance(err, dict) 
            for field in ['message', 'type', 'code']:
                self.assertEqual(expected[field], err[field])
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))
