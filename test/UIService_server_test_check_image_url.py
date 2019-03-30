# -*- coding: utf-8 -*-

from UIServiceTest import UIServiceTest

from UIService.UIServiceValidation import Validation
from TestWebServer import TestWebServer

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urlBase = 'https://localhost:8002'
non_secure_url_base = 'http://localhost:8002'
bad_url_base = 'https://fakehost:8002'

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

    def test_validation_home_url_bad_params(self):
        try:
            bad_params = [{
                'input': {
                    'url': 123,
                    'timeout': 1000
                }, 
                'expected': {
                    'message': 'the "url" parameter is expected to be a "str" but is actually a "int', 
                    'type': 'input', 
                    'code': 'wrong-type', 
                    'info': {
                        'key': 'url', 
                        'expected': 'str', 
                        'received': 'int'
                    }
                }
            },
            {
                'input': {
                    'url': urlBase + '/test1.html',
                    'timeout': 'abc'
                }, 
                'expected': {
                    'message': 'the "timeout" parameter is expected to be a "int" but is actually a "str', 
                    'type': 'input', 
                    'code': 'wrong-type', 
                    'info': {
                        'key': 'timeout', 
                        'expected': 'int', 
                        'received': 'str'
                        }
                    }
            },
            {
                'input': {
                    'url': urlBase + '/test1.html',
                    'timeout': 1000,
                    'verify_ssl': 'x'
                }, 
                'expected': {
                    'message': 'the "verify_ssl" parameter is expected to be a "int" but is actually a "str', 
                    'type': 'input', 
                    'code': 'wrong-type', 
                    'info': {
                        'key': 'verify_ssl', 
                        'expected': 'int', 
                        'received': 'str'
                    }
                }
            },
            {
                'input': {
                    'url': non_secure_url_base + '/test1.html',
                    'timeout': 1000,
                    'verify_ssl': True
                }, 
                'expected': {
                    'message': 'this url parameter must be secure', 
                    'type': 'input', 
                    'code': 'wrong-format', 
                    'info': {
                        'key': 'url'
                    }
                }
            },
            {
                'input': {
                    'url': 'x',
                    'timeout': 1000
                }, 
                'expected': {
                    'message': 'does not match a valid url', 
                    'type': 'input', 
                    'code': 'wrong-format', 
                    'info': {'key': 'url'}
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
                ret, err = self.getImpl().check_image_url(self.getContext(), bad_param['input'])
                self.assertIsNone(ret)
                self.assertIsNotNone(err)
                # print(err)
                self.assertIsInstance(err, dict) 
                self.assertDictEqual(err, bad_param['expected'])
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

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

    def test_check_image_url_unexpected_code(self):
        try:
            param = {
                'url': urlBase + '/respond-400',
                'timeout': 1000,
                'verify_ssl': 0
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

    def test_validation_image_url_missing_content_type(self):
        try:
            param = {
                'url': urlBase + '/missing-content-type',
                'timeout': 1000,
                'verify_ssl': 0
            }

            expected = {
                'is_valid': False,
                'error': {
                    'code': 'missing-content-type',
                    'info': {
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

    def test_validation_image_url_bad_url(self):
        try:
            param = {
                'url': bad_url_base,
                'timeout': 1000
            }

            expected = { 
                'message': ('exception requesting image'), 
                'type': 'value', 
                'code': 'error-response'
            }

            ret, err = self.getImpl().check_image_url(self.getContext(), param)

            self.assertIsNone(ret)
            self.assertIsNotNone(err)
            self.assertIsInstance(err, dict) 
            for field in ['message', 'type', 'code']:
                self.assertEqual(expected[field], err[field])
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))


    
