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
        # cls.wsURL = cls.cfg['workspace-url']
        # cls.wsClient = workspaceService(cls.wsURL)
        # print(cls.cfg)
        cls.serviceImpl = UIService(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        # # Start a little web server for testing against for the url methods.
        # http_server_port = 8002
        # # handler = http.server
        # cls.inst_id = uuid.uuid4()
        # class TestServer(socketserver.TCPServer):
        #     allow_reuse_address = True
        # print("STARTING", cls.inst_id)
        # test_content = os.path.dirname(__file__) + "/test_content"
        # print("TEST CONTENT", test_content, "\n")
        # class MyHandler(http.server.SimpleHTTPRequestHandler):
        #     directory = test_content
        #     def do_HEAD(self): 
        #         print('HEAD???', self.path, "\n")
        #         if self.path == '/test1.html':
        #             self.send_response(200, 'OK')
        #             self.send_header('Content-Type', 'text/html')
        #             self.send_header('Content-Length', 100)
        #             self.end_headers()
        #         if self.path == '/test1.css':
        #             self.send_response(200, 'OK')
        #             self.send_header('Content-Type', 'text/css')
        #             self.send_header('Content-Length', 100)
        #             self.end_headers()
        #         if self.path == '/respond-400':
        #             self.send_response(400, 'OK')
        #             self.send_header('Content-Type', 'text/plain')
        #             self.send_header('Content-Length', 100)
        #             self.end_headers()
        #         else:
        #             self.send_response(404, 'Not Found')
        #             self.send_header('Content-Type', 'text/plain')
        #             self.end_headers()
                


            # def translate_path(self, path):
            #     path = http.server.SimpleHTTPRequestHandler.translate_path(self, path)
            #     relpath = os.path.relpath(path, os.getcwd())
            #     fullpath = os.path.join(test_content, relpath)
            #     print("FULL PATH", fullpath)
            #     return fullpath

        # handler = http.server.SimpleHTTPRequestHandler(directory="test_content")
        # cls.httpd = TestServer(("localhost", http_server_port), MyHandler)
        # cls.httpd_thread = threading.Thread(target=cls.httpd.serve_forever)
        # cls.httpd_thread.setDaemon(True)
        # cls.httpd_thread.start()
        
        # print('STARTED', cls.inst_id)

    @classmethod
    def tearDownClass(cls):
        # print('SHUTTING DOWN??', cls.inst_id)
        # cls.httpd.shutdown()
        # cls.httpd.server_close()
        # print('FINISHING THREAD?', cls.inst_id)
        # cls.httpd_thread.join()
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

    def get_alert(self, id):
        param = {
            'id': id
        }
        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)
        return ret

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

    