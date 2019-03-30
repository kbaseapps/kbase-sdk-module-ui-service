import math
import json
import time
import calendar
import re

class Validation(object):

    min_timeout = 0
    max_timeout = 1000 * 60

    @staticmethod
    def check_param(params, name, required, param_type):
        if name not in params:
            if required:
                error = {
                    'message': 'the required parameter "' + name + '" was not provided',
                    'type': 'input',
                    'code': 'missing',
                    'info': {
                        'key': name
                    }
                }
                return [None, error]
            else:
                return [None, None]

        param_value = params[name]
        if not isinstance(param_value, param_type):
            error = {
                'message': ('the "' + name + '" parameter is expected to be a "' + param_type.__name__ + '" but is actually a "' + type(param_value).__name__),
                'type': 'input',
                'code': 'wrong-type',
                'info': {
                    'key': name,
                    'expected': param_type.__name__,
                    # TODO translate to json type name
                    'received': type(param_value).__name__
                }
            }
            return [None, error]
        return [param_value, None]

    @staticmethod
    def check_url(url, must_be_secure):
        secure_url = re.compile('^https://')
        nonsecure_url = re.compile('^http://')
        any_url = re.compile('^http[s]?://')
        if not re.match(any_url, url):
            error = {
                'message': ('does not match a valid url'),
                'type': 'input',
                'code': 'wrong-format',
                'info': {
                }
            }
            return [None, error]

        if must_be_secure:
            if not re.match(secure_url, url):
                error = {
                    'message': ('this url parameter must be secure'),
                    'type': 'input',
                    'code': 'wrong-format',
                    'info': {
                    }
                }
                return [None, error]
        
        return [url, None]

    @classmethod
    def validate_check_html_url_param(cls, parameter, ctx):
        url, error = cls.check_param(parameter, 'url', True, str)
        if error is not None:
            return None, error

        url, error = cls.check_url(url, False)
        if error is not None:
            error['info']['key'] = 'url'
            return None, error

        timeout, error = cls.check_param(parameter, 'timeout', True, int)
        if error is not None:
            return None, error

        

        if (timeout < cls.min_timeout):
            error = {
                    'message': ('the timeout parameter must be greater than 0'),
                    'type': 'input',
                    'code': 'out-of-range',
                    'info': {
                        'min': cls.min_timeout,
                        'max': cls.max_timeout
                    }
            }
            return [None, error]

        if (timeout > cls.max_timeout):
            error = {
                    'message': ('the timeout parameter must be less than one minute'),
                    'type': 'input',
                    'code': 'out-of-range',
                    'info': {
                        'min': cls.min_timeout,
                        'max': cls.max_timeout
                    }
            }
            return [None, error]

        return [{
            'url': url,
            'timeout': timeout
        }, None]

    @classmethod
    def validate_check_image_url_param(cls, parameter, ctx):
        url, error = cls.check_param(parameter, 'url', True, str)
        if error is not None:
            return None, error

        verify_ssl, error = cls.check_param(parameter, 'verify_ssl', False, int)
        if error is not None:
            return None, error
        if verify_ssl is None:
            verify_ssl = True
        elif verify_ssl == 0:
            verify_ssl = False
        else:
            verify_ssl = True

        url, error = cls.check_url(url, True)
        if error is not None:
            error['info']['key'] = 'url'
            return None, error

        timeout, error = cls.check_param(parameter, 'timeout', True, int)
        if error is not None:
            return None, error

        if (timeout < cls.min_timeout):
            error = {
                    'message': ('the timeout parameter must be greater than 0'),
                    'type': 'input',
                    'code': 'out-of-range',
                    'info': {
                        'min': cls.min_timeout,
                        'max': cls.max_timeout
                    }
            }
            return [None, error]

        if (timeout > cls.max_timeout):
            error = {
                    'message': ('the timeout parameter must be less than one minute'),
                    'type': 'input',
                    'code': 'out-of-range',
                    'info': {
                        'min': cls.min_timeout,
                        'max': cls.max_timeout
                    }
            }
            return [None, error]

        # try to fetch it with HEAD
       

        return [{
            'url': url,
            'timeout': timeout,
            'verify_ssl': verify_ssl
        }, None]

    @classmethod
    def validate_config(cls, config):
        if 'auth-url' not in config:
            raise(ValueError('"auth-url" configuration property not provided'))
        auth_url = config['auth-url']

        return {
            'auth-url': auth_url
        }