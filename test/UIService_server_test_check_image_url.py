# -*- coding: utf-8 -*-

from UIServiceTest import UIServiceTest

from UIService.UIServiceValidation import Validation

class UIServiceTest_check_image_url(UIServiceTest):
    # TESTS
    def test_validation_image_url_good_url(self):
        try:
            param1 = {
                'url': 'https://kbase.us/wp-content/uploads/2014/11/kbase-logo-web.png',
                'timeout': 1000
            }
            expected1 = {
                'url': 'https://kbase.us/wp-content/uploads/2014/11/kbase-logo-web.png',
                'timeout': 1000
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
                'url': 'https://kbase.us/wp-content/uploads/2014/11/kbase-logo-web.png',
                'timeout': 1000
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
                'url': 'https://kbase.us/wp-content/uploads/2014/11/kbase-logo-web.pngx',
                'timeout': 1000
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

            ret, err = self.getImpl().check_image_url(self.getContext(), param)

            self.assertIsNone(err)
            self.assertIsNotNone(ret)
            self.assertIsInstance(ret, dict) 
            self.assertDictEqual(ret, expected)
        except Exception as ex:
            self.assertTrue(False, 'Unexpected exception: %s' % str(ex))

    # Home url

    
