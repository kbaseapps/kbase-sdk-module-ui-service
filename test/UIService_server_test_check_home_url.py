# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

from UIService.UIServiceValidation import Validation

class UIServiceTest_check_home_url(UIServiceTest):
    # TESTS
    def test_validation_home_url_good_param(self):
        try:
            param = {
                'url': 'https://kbase.us',
                'timeout': 1000
            }
            expected = {
                'url': 'https://kbase.us',
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
                'url': 'https://kbase.us',
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
  
    def test_validation_html_url_missing_url(self):
        try:
            param = {
                'url': 'https://kbase.us/xyz',
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
                'url': 'https://kbase.us/wp-content/themes/kbase-wordpress-theme/style.css',
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
