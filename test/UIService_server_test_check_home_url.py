# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_check_home_url(UIServiceTest):
    # TESTS
    def test_validation_home_url_good_url(self):
        try:
            param = {
                'url': 'https://kbase.us'
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
                'url': 'https://kbase.us/xyz'
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
                'url': 'https://kbase.us/wp-content/themes/kbase-wordpress-theme/style.css'
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
