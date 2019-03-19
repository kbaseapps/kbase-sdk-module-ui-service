# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_test_search_alerts(UIServiceTest):
    # TESTS
    def test_search_alerts(self):
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
            },
            {
                'input': {
                    'query': {
                        'op': 'and',
                        'args': [                    
                            {
                                'op': 'or',
                                'args': [
                                    {
                                        'path': 'created_by',
                                        'op': 'eq',
                                        'value': 'eapearson'
                                    },
                                    {
                                        'path': 'created_by',
                                        'op': 'eq',
                                        'value': 'm_mouse'
                                    },
                                ]
                            }
                        ]
                    }
                }
            }
        ]
        for test in test_table:
            ret, err = self.getImpl().search_alerts(self.getContext(), test['input'])
            self.assertIsNotNone(ret)
            self.assertIsNone(err)
            self.assertIsInstance(ret, dict)
            self.assertIn('alerts', ret)

        ret, err = self.getImpl().search_alerts(self.getContext(), {'query': 123})
        self.assertIsNone(ret)
        self.assertIsNotNone(err)
        self.assertIsInstance(err, dict)
        self.assertIn('type', err)
        self.assertEquals(err['type'], 'input')
        self.assertIn('code', err)
        self.assertEquals(err['code'], 'wrong-type')

    def test_search_alerts_bad_query(self):
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
                },
                'expected': {
                    'error': {
                        'code': 'invalid'
                    }
                }
            },
            {
                'input': {
                    'query': {
                        'op': 'and',
                        'args': [
                            {
                                'path': 'created_by',
                                'op': 'eqx',
                                'value': 'eapearson'
                            }
                        ]
                    }
                },
                'expected': {
                    'error': {
                        'code': 'invalid'
                    }
                }
            },
            {
                'input': {
                    'query': {
                        'op': 'and',
                        'args': [
                            {
                                'path': 'created_by',
                                'op': 'eqx',
                                'value': 'eapearson'
                            }
                        ]
                    },
                    'paging': 123
                },
                'expected': {
                    'error': {
                        'code': 'wrong-type'
                    }
                }
            },
            {
                'input': {
                    'query': {
                        'op': 'and',
                        'args': [
                            {
                                'path': 'created_by',
                                'op': 'eqx',
                                'value': 'eapearson'
                            }
                        ]
                    },
                    'sorting': 123
                },
                'expected': {
                    'error': {
                        'code': 'wrong-type'
                    }
                }
            },
        ]
        for test in test_table:
            ret, err = self.getImpl().search_alerts(self.getContext(), test['input'])
            self.assertIsNone(ret)
            self.assertIsNotNone(err)
            self.assertIsInstance(err, dict)
            self.assertIn('type', err)
            self.assertEquals(err['type'], 'input')
            self.assertIn('code', err)
            self.assertEquals(err['code'], test['expected']['error']['code'])
   