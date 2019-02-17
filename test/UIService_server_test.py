# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import string
import random

from os import environ
try:
    from configparser import ConfigParser as _ConfigParser  # py 3
except ImportError:
    from ConfigParser import ConfigParser as _ConfigParser  # py 2
import time

from pprint import pprint  # noqa: F401

from UIService.UIServiceImpl import UIService
from UIService.UIServiceServer import MethodContext
from UIService.authclient import KBaseAuth as _KBaseAuth
from UIService.UIServiceModel import UIServiceModel
from UIService.UIServiceValidation import Validation


class UIServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = _ConfigParser()
        config.read(config_file)

        for nameval in config.items('UIService'):
            cls.cfg[nameval[0]] = nameval[1]

        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'UIService',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        # print(cls.cfg)
        cls.serviceImpl = UIService(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        pass
        
    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def assert_error(self, ret, err, type_value, code_value):
        self.assertIsNone(ret)
        self.assertIsNotNone(err)
        self.assertIsInstance(err, dict)
        self.assertIn('type', err) 
        self.assertEquals(err['type'], type_value)
        self.assertEquals(err['code'], code_value)

    # TESTS

    def test_config(self):
        config = {
            'mongo-host': 'mongo', 
            'handle-service-url': 'https://ci.kbase.us/services/handle_service', 
            'mongo-db': 'ui_service', 
            'mongo-user': 'ui_service', 
            'auth-url': 'https://ci.kbase.us/services/auth', 
            'auth-service-url': 'https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login', 
            'srv-wiz-url': 'https://ci.kbase.us/services/service_wizard', 
            'job-service-url': 'https://ci.kbase.us/services/userandjobstate', 
            'auth-service-url-allow-insecure': 'false', 
            'njsw-url': 'https://ci.kbase.us/services/njs_wrapper', 
            'shock-url': 'https://ci.kbase.us/services/shock-api', 
            'workspace-url': 'https://ci.kbase.us/services/ws', 
            'scratch': '/kb/module/work/tmp', 
            'data-root': '/kb/module/work/data', 
            'admin-users': 'eapearson', 
            'mongo-pwd': 'ui_service', 
            'kbase-endpoint': 'https://ci.kbase.us/services', 
            'mongo-port': '27017'
        }
        try:
            uis = UIService(config)
            self.assertIsNotNone(uis)
        except Exception as ex:
            self.assertTrue(False)
    
    def test_config_bad_input(self):
        config = {
            'mongo-host': 'mongo', 
            'handle-service-url': 'https://ci.kbase.us/services/handle_service', 
            'mongo-db': 'ui_service', 
            'mongo-user': 'ui_service', 
            'auth-url': 'https://ci.kbase.us/services/auth', 
            'auth-service-url': 'https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login', 
            'srv-wiz-url': 'https://ci.kbase.us/services/service_wizard', 
            'job-service-url': 'https://ci.kbase.us/services/userandjobstate', 
            'auth-service-url-allow-insecure': 'false', 
            'njsw-url': 'https://ci.kbase.us/services/njs_wrapper', 
            'shock-url': 'https://ci.kbase.us/services/shock-api', 
            'workspace-url': 'https://ci.kbase.us/services/ws', 
            'scratch': '/kb/module/work/tmp', 
            'data-root': '/kb/module/work/data', 
            'admin-users': 'eapearson', 
            'mongo-pwd': 'ui_service', 
            'kbase-endpoint': 'https://ci.kbase.us/services', 
            'mongo-port': '27017'
        }
        for name in ['auth-url', 'mongo-host', 'mongo-port', 'mongo-db', 'mongo-user', 'mongo-pwd']:
            cfg = dict(config)
            del cfg[name]
            try:
                uis = UIService(cfg)
                self.assertTrue(False)
            except ValueError:
                self.assertTrue(True)
        

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_get_alert(self):
        param = {
            'idx': 'should_not_exist'
        }

        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assert_error(ret, err, 'input', 'missing')
        self.assertEquals(err['info']['key'], 'id')

        param = {
            'id': 1
        }
        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assert_error(ret, err, 'input', 'wrong-type')
        self.assertEquals(err['info']['key'], 'id')

        param = {
            'id': 'abc123'
        }
        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assertIsNone(ret)
        self.assertIsNone(err)
        # self.assert_error(ret, err, 'data', 'notfound')
        # self.assertEquals(err['info']['id'], 'abc123')

        # presumes this alert is already present.
        param = {
            'id': '4952c5bc-528e-4403-9981-6f00279fce86'
        }
        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)

    def test_get_active_alert(self):
        # TODO: we need to populate the db with different cases of 
        #       active and inactive alerts.
        ret, err = self.getImpl().get_active_alerts(self.getContext())
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, list)

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

    def test_am_admin_user(self):
        ret, err = self.getImpl().am_admin_user(self.getContext())
        self.assertIsNone(err)
        self.assertIsInstance(ret, bool)
        self.assertEquals(ret, True)

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

    def generate_random_string(self):
        c = string.ascii_letters + string.digits
        r = ''.join([random.choice(c) for n in range(32)])
        return r

    def add_random_alert(self, include_end_at=True):
        a_random_string = self.generate_random_string()
        if include_end_at:
            end_at = UIServiceModel.iso_to_iso('2018-01-02T00:00:00Z')
        else:
            end_at = None
        input = {
            'alert': {
                'title': 'title_' + a_random_string,
                'message': 'message_' + a_random_string,
                'start_at': UIServiceModel.iso_to_iso('2018-01-01T00:00:00Z'),
                'end_at': end_at,
                'status': 'published'
            }
        }

        ret, err = self.getImpl().add_alert(self.getContext(), input)
        self.assertIsNone(err)
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, dict)
        self.assertIn('id', ret)
        return a_random_string, ret['id']

    def get_alert_by_title(self, a_random_string):
        input = {
            'query': {
                'op': 'and',
                'args': [
                    {
                        'path': 'title',
                        'op': 'eq',
                        'value': 'title_' + a_random_string
                    }
                ]
            }
        }
        ret, err = self.getImpl().search_alerts(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)
        self.assertIn('alerts', ret)
        return ret['alerts']

    def get_alert(self, id):
        param = {
            'id': id
        }
        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)
        return ret

    def test_add_alert(self):
        a_random_string, _id = self.add_random_alert()
        alert = self.get_alert_by_title(a_random_string)
        self.assertEquals(alert[0]['title'], 'title_' + a_random_string)

        a_random_string, _id = self.add_random_alert(False)
        alert = self.get_alert_by_title(a_random_string)
        self.assertEquals(alert[0]['title'], 'title_' + a_random_string)

    def test_delete_alert(self):
        a_random_string, _id = self.add_random_alert()
        alerts = self.get_alert_by_title(a_random_string)
        alert_id = alerts[0]['id']
        ret, err = self.getImpl().delete_alert(self.getContext(), alert_id)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)

    def test_update_alert(self):
        a_random_string, alert_id = self.add_random_alert()
        alert = self.get_alert(alert_id)
        alert_id = alert['id']

        another_random_string = self.generate_random_string()
        test_table = [
            {
                'field': 'title',
                'value': 'title_' + another_random_string
            },
            {
                'field': 'message',
                'value': 'message_' + another_random_string
            },
            {
                'field': 'start_at',
                'value': UIServiceModel.iso_to_iso('2019-01-02T00:00:00Z')
            },
            {
                'field': 'end_at',
                'value': UIServiceModel.iso_to_iso('2019-01-03T00:00:00Z')
            }
        ]

        for test in test_table:
            field_name = test['field']
            input = {
                'alert': {
                    'id': alert_id
                }
            }
            input['alert'][field_name] = test['value']

            ret, err = self.getImpl().update_alert(self.getContext(), input)
            self.assertIsNotNone(ret)
            self.assertIsNone(err)

            alert2 = self.get_alert(alert_id)
            self.assertEquals(alert2[field_name], input['alert'][field_name])

    def test_set_alert(self):
        a_random_string, alert_id = self.add_random_alert()
        alert = self.get_alert(alert_id)
        alert_id = alert['id']
        another_random_string = self.generate_random_string()
        input = {
            'alert': {
                'id': alert_id,
                'title': 'title_' + another_random_string,
                'message': 'message_' + another_random_string,
                'status': 'status_' + another_random_string,
                'start_at': UIServiceModel.iso_to_iso('2019-01-01T00:00:00Z'),
                'end_at': UIServiceModel.iso_to_iso('2019-01-02T00:00:00Z'),
            }
        }
        ret, err = self.getImpl().set_alert(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)

        alert2 = self.get_alert(alert_id)
        self.assertEquals(alert2['title'], input['alert']['title'])
        self.assertEquals(alert2['message'], input['alert']['message'])

        self.assertNotEquals(alert2['title'], alert['title'])
        self.assertNotEquals(alert2['message'], alert['message'])

    def test_status(self):
        ret = self.getImpl().status(self.getContext())
        ret = ret[0]
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, dict)
        self.assertIn('state', ret)
        self.assertEquals(ret['state'], 'OK')

    def test_model_no_token(self):
        auth_url = self.cfg['auth-url']
        admin_users = self.cfg['admin-users']
        token = self.ctx['token']
        username = self.ctx['user_id']
        config = Validation.validate_config(self.cfg)
        db_config = config['mongo']

        try:
            uis = UIServiceModel(auth_url, None, username, admin_users, db_config)
            uis.delete_alert('abc')
            self.assertTrue(False)
        except Exception as ex:
            self.assertTrue(True)

        try:
            uis = UIServiceModel(auth_url, token, 'not_an_admin', admin_users, db_config)
            uis.delete_alert('abc')
            self.assertTrue(False)
        except Exception as ex:
            self.assertTrue(True)
        
