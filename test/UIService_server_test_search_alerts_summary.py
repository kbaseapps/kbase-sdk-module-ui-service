# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_test_search_alerts_summary(UIServiceTest):
    # TESTS
    def test_search_alerts_summary(self):
        # TODO: we need to populate the db with different cases of 
        #       active and inactive alerts.
        test_table = [
            {
                'input': {
                    'query': {
                        'op': 'and',
                        'args': [
                            {
                                'path': 'created_by',
                                'op': 'eq',
                                'value': 'eapearson'
                            }
                        ]
                    }
                }
            }
        ]
        for test in test_table:
            ret, err = self.getImpl().search_alerts_summary(self.getContext(), test['input'])
            self.assertIsNotNone(ret)
            self.assertIsNone(err)
            self.assertIsInstance(ret, dict)
            self.assertIn('alerts_summary', ret)

    def test_search_alerts_summary_bad_input(self):
        # TODO: we need to populate the db with different cases of 
        #       active and inactive alerts.
        test_table = [
            {
                'input': {
                    'query': {
                        'op': 'what?',
                        'args': [
                            {
                                'path': 'created_by',
                                'op': 'eq',
                                'value': 'eapearson'
                            }
                        ]
                    }
                }
            },
            {
                'input': {
                    'query': 123
                }
            }
        ]
        for test in test_table:
            ret, err = self.getImpl().search_alerts_summary(self.getContext(), test['input'])
            self.assertIsNone(ret)
            self.assertIsNotNone(err)
            self.assertIsInstance(err, dict)

    