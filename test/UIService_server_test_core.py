# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

from UIService.UIServiceValidation import Validation 
from UIService.UIServiceImpl import UIService

class UIServiceTest_test_core(UIServiceTest):
    # TESTS
    def test_config(self):
        config = {
            'handle-service-url': 'https://ci.kbase.us/services/handle_service', 
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
            'kbase-endpoint': 'https://ci.kbase.us/services'
        }
        try:
            uis = UIService(config)
            self.assertIsNotNone(uis)
        except Exception as ex:
            self.assertTrue(False)
    
    def test_config_bad_input(self):
        config = {
            'handle-service-url': 'https://ci.kbase.us/services/handle_service', 
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
            'kbase-endpoint': 'https://ci.kbase.us/services'
        }
        for name in ['auth-url']:
            cfg = dict(config)
            del cfg[name]
            try:
                uis = UIService(cfg)
                self.assertTrue(False)
            except ValueError:
                self.assertTrue(True)
