# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_test_is_admin_user(UIServiceTest):
    # TESTS
    def test_is_admin_user(self):
        test_table = [
            {
                'input': {
                    'username': 'eapearson'
                },
                'expected': True
            },
            {
                'input': {
                    'username': 'not_admin_user'
                },
                'expected': False
            }
        ]
        for test in test_table:
            ret, err = self.getImpl().is_admin_user(self.getContext(), test['input'])
            self.assertIsNone(err)
            self.assertIsInstance(ret, bool)
            self.assertEquals(ret, test['expected'])

    def test_is_admin_user_bad_input(self):
        test_table = [
            {
                'input': {
                    'username': 123
                }
            },
            {
                'input': {
                    'usernamex': 123
                }
            }
        ]
        for test in test_table:
            ret, err = self.getImpl().is_admin_user(self.getContext(), test['input'])
            self.assertIsNone(ret)
            self.assertIsInstance(err, dict)

    
