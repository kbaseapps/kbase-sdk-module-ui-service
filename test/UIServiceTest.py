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
    def generate_random_string(self):
        c = string.ascii_letters + string.digits
        r = ''.join([random.choice(c) for n in range(32)])
        return r

    