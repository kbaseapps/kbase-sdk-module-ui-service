# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest
from UIService.UIServiceValidation import Validation

class UIServiceTest_test_validation(UIServiceTest):
    # TESTS
    def test_validation_missing_required_param(self):
        try:
            params = {
                'param1': 1
            }
            name = 'param2'
            required = True
            param_type = int
            expected = { 
                'message': 'the required parameter "' + name + '" was not provided', 
                'type': 'input', 
                'code': 'missing', 
                'info': { 
                    'key': name 
                } 
            }

            result, err = Validation.check_param(params, name, required, param_type)
            self.assertIsNone(result)
            self.assertIsNotNone(err)
            
            self.assertIsInstance(err, dict)
            self.assertDictEqual(err, expected)

        except Exception as ex:
            self.assertTrue(False)

    def test_validation_missing_optional_param(self):
        try:
            params = {
                'param1': 1
            }
            name = 'param2'
            required = False
            param_type = int

            result, err = Validation.check_param(params, name, required, param_type)
            self.assertIsNone(err)
            self.assertIsNone(result)

        except Exception as ex:
            self.assertTrue(False)

    def test_validation_url_should_be_secure_but_not(self):
        try:
            url = 'http://a.b.c'
            must_be_secure = True
            expected = { 
                'message': ('this url parameter must be secure'), 
                'type': 'input', 
                'code': 'wrong-format', 
                'info': { 
                } 
            } 

            result, err = Validation.check_url(url, must_be_secure)
            self.assertIsNone(result)
            self.assertIsNotNone(err)
            
            self.assertIsInstance(err, dict)
            self.assertDictEqual(err, expected)

        except Exception as ex:
            self.assertTrue(False)

    def test_validation_url_invalid_format(self):
        try:
            url = 'xhttp://a.b.c'
            must_be_secure = True
            expected = { 
                'message': ('does not match a valid url'), 
                'type': 'input', 
                'code': 'wrong-format', 
                'info': { 
                } 
            } 

            result, err = Validation.check_url(url, must_be_secure)
            self.assertIsNone(result)
            self.assertIsNotNone(err)
            
            self.assertIsInstance(err, dict)
            self.assertDictEqual(err, expected)

        except Exception as ex:
            self.assertTrue(False)

    def test_validation_url_should_be_secure_and_is(self):
        try:
            url = 'https://a.b.c'
            must_be_secure = True
            expected = 'https://a.b.c'

            result, err = Validation.check_url(url, must_be_secure)
            self.assertIsNotNone(result)
            self.assertIsNone(err)
            
            self.assertIsInstance(result, str)
            self.assertEqual(result, expected)

        except Exception as ex:
            self.assertTrue(False)

