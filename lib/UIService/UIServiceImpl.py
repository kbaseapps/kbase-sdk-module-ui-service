# -*- coding: utf-8 -*-
#BEGIN_HEADER
from UIService.UIServiceValidation import Validation
import os
import string
import traceback
import re
import requests
#END_HEADER


class UIService:
    '''
    Module Name:
    UIService

    Module Description:
    A KBase module: UIService
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.1.0"
    GIT_URL = "https://github.com/kbaseapps/kbase-sdk-module-ui-service"
    GIT_COMMIT_HASH = "99ca5d12835dc68a8795bb75bbb21c26d4d5fd72"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        config = Validation.validate_config(config)

        self.auth_url = config['auth-url']
        #END_CONSTRUCTOR
        pass


    def check_html_url(self, ctx, param):
        """
        :param param: instance of type "CheckHTMLURLParams" (Check html url)
           -> structure: parameter "url" of String, parameter "timeout" of
           Long
        :returns: multiple set - (1) parameter "result" of type
           "CheckHTMLURLResult" -> structure: parameter "is_valid" of type
           "Boolean", parameter "error" of type "CheckError" -> structure:
           parameter "code" of String, parameter "info" of unspecified
           object, (2) parameter "error" of type "Error" -> structure:
           parameter "message" of String, parameter "type" of String,
           parameter "code" of String, parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: result, error
        #BEGIN check_html_url
        param, error = Validation.validate_check_html_url_param(param, ctx)
        if error:
            return [None, error]

        try:
            response = requests.head(url=param['url'], timeout=param['timeout']/1000)
            if response.status_code == 404:
                return [{
                    'is_valid': False,
                    'error': {
                        'code': 'not-found'
                    }
                    
                }, None]

            if response.status_code != 200:
                return [{
                    'is_valid': False,
                    'error': {
                        'code': 'unexpected-response-status-code',
                        'info': {
                            'status_code': response.status_code
                        }
                    }
                    
                }, None]

            if 'content-type' not in response.headers:
                return [{
                    'is_valid': False,
                    'error': {
                        'code': 'missing-content-type',
                        'info': {
                        }
                    }
                   
                }, None]

            content_type = response.headers['content-type']
            image_re = re.compile('^text/html')
            if not re.match(image_re, content_type):
                return [{
                    'is_valid': False,
                    'error': {
                        'code': 'invalid-content-type',
                        'info': {
                            'content_type': content_type
                        }
                    }
                }, None]

            return [{
                'is_valid': True,
            }, None]

        except Exception as ex:
            return [None, {
                'message': ('exception requesting html page'),
                'type': 'value',
                'code': 'error-response',
                'info': {
                    'exception': str(ex)
                }
            }]
        #END check_html_url

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method check_html_url return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method check_html_url return value ' +
                             'error is not type dict as required.')
        # return the results
        return [result, error]

    def check_image_url(self, ctx, param):
        """
        :param param: instance of type "CheckImageURLParams" (Check image
           url) -> structure: parameter "url" of String, parameter "timeout"
           of Long, parameter "verify_ssl" of type "Boolean"
        :returns: multiple set - (1) parameter "result" of type
           "CheckImageURLResult" -> structure: parameter "is_valid" of type
           "Boolean", parameter "error" of type "CheckError" -> structure:
           parameter "code" of String, parameter "info" of unspecified
           object, (2) parameter "error" of type "Error" -> structure:
           parameter "message" of String, parameter "type" of String,
           parameter "code" of String, parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: result, error
        #BEGIN check_image_url
        param, error = Validation.validate_check_image_url_param(param, ctx)
        if error:
            return [None, error]

        try:
            response = requests.head(url=param['url'], timeout=param['timeout']/1000, verify=param['verify_ssl'])
            if response.status_code == 404:
                return [{
                    'is_valid': False,
                    'error': {
                        'code': 'not-found'
                    }
                }, None]

            if response.status_code != 200:
                return [{
                    'is_valid': False,
                    'error': {
                        'code': 'unexpected-response-status-code',
                        'info': {
                            'status_code': response.status_code
                        }
                    }
                }, None]

            if 'content-type' not in response.headers:
                return [{
                    'is_valid': False,
                    'error': {
                        'code': 'missing-content-type',
                        'info': {
                        }
                    }
                }, None]

            content_type = response.headers['content-type']
            image_re = re.compile('^image/')
            if not re.match(image_re, content_type):
                return [{
                    'is_valid': False,
                    'error': {
                        'code': 'invalid-content-type',
                        'info': {
                            'content_type': content_type
                        }
                    }
                }, None]

            return [{
                'is_valid': True,
            }, None]

        except Exception as ex:
            return [None, {
                'message': ('exception requesting image'),
                'type': 'value',
                'code': 'error-response',
                'info': {
                    'exception': str(ex)
                }
            }]
        #END check_image_url

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method check_image_url return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method check_image_url return value ' +
                             'error is not type dict as required.')
        # return the results
        return [result, error]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
