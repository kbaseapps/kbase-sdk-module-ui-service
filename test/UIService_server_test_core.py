# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

from UIService.UIServiceModel import UIServiceModel
from UIService.UIServiceValidation import Validation 
from UIService.UIServiceImpl import UIService

class UIServiceTest_test_core(UIServiceTest):
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