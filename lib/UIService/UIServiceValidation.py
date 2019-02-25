import math
import json
import time
import calendar
import re

class Validation(object):

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
        if not re.match(any_url, url):
            error = {
                'message': ('does not match a valid url'),
                'type': 'input',
                'code': 'wrong-format',
                'info': {
                }
            }
            return [None, error]
        return [url, None]

    @classmethod
    def validate_get_alert_parameter(cls, parameter, ctx):
        id, error = cls.check_param(parameter, 'id', True, str)
        if error is not None:
            return None, error

        return [{
            'id': id
        }, None]

    @classmethod
    def validate_search_alerts_parameter(cls, parameter, ctx):
        query, error = cls.check_param(parameter, 'query', True, dict)
        if error is not None:
            return None, error

        paging, error = cls.check_param(parameter, 'paging', False, dict)
        if error is not None:
            return None, error

        sorting, error = cls.check_param(parameter, 'sorting', False, dict)
        if error is not None:
            return None, error

        return [{
            'query': query,
            'paging': paging,
            'sorting': sorting
        }, None]

    @classmethod
    def validate_search_alerts_summary_parameter(cls, parameter, ctx):
        query, error = cls.check_param(parameter, 'query', True, dict)
        if error is not None:
            return None, error

        return [{
            'query': query
        }, None]

    @classmethod
    def validate_is_admin_user(cls, parameter, ctx):
        username, error = cls.check_param(parameter, 'username', True, str)
        if error is not None:
            return None, error

        return [{
            'username': username
        }, None]

    @classmethod
    def validate_validate_html_url_param(cls, parameter, ctx):
        url, error = cls.check_param(parameter, 'url', True, str)
        if error is not None:
            return None, error

        url, error = cls.check_url(url, False)
        if error is not None:
            error['info']['key'] = 'url'
            return None, error

        return [{
            'url': url
        }, None]

    @classmethod
    def validate_validate_image_url_param(cls, parameter, ctx):
        username, error = cls.check_param(parameter, 'url', True, str)
        if error is not None:
            return None, error

        url, error = cls.check_param(parameter, 'url', True, str)
        if error is not None:
            return None, error

        url, error = cls.check_url(url, True)
        if error is not None:
            error['info']['key'] = 'url'
            return None, error

        # try to fetch it with HEAD
       

        return [{
            'url': url
        }, None]

    @classmethod
    def validate_config(cls, config):
        if 'auth-url' not in config:
            raise(ValueError('"auth-url" configuration property not provided'))
        auth_url = config['auth-url']

        # Import and validate the connection timeout
        # if 'jgi-connection-timeout' not in config:
        #     raise(ValueError('"jgi-connection-timeout" configuration property not provided'))
        # try:
        #     connection_timeout = int(config['jgi-connection-timeout'])
        # except ValueError as ex:
        #     raise(ValueError('"jgi-connection-timeout" configuration property is not a float: ' + str(ex)))
        # if not (config['jgi-connection-timeout'] > 0):
        #     raise(ValueError('"jgi-connection-timeout" configuration property must be > 0'))

        # connection_timeout = float(connection_timeout) /float(1000)
        # print('connection timeout %f sec' % (connection_timeout) )

        # Import and validate the mongo db settings
        if 'mongo-host' not in config:
            raise(ValueError('"mongo-host" configuration property not provided')) 
        mongo_host = config['mongo-host']

        if 'mongo-port' not in config:
            raise(ValueError('"mongo-port" configuration property not provided')) 
        mongo_port = int(config['mongo-port'])

        if 'mongo-db' not in config:
            raise(ValueError('"mongo-db" configuration property not provided'))
        mongo_db = config['mongo-db']

        if 'mongo-user' not in config:
            raise(ValueError('"mongo-user" configuration property not provided'))
        mongo_user = config['mongo-user']

        if 'mongo-pwd' not in config:
            raise(ValueError('"mongo-pwd" configuration property not provided'))
        mongo_pwd = config['mongo-pwd']

        return {
            'mongo': {
                'host': mongo_host,
                'port': mongo_port,
                'db': mongo_db,
                'user': mongo_user,
                'password': mongo_pwd
            },
            'auth-url': auth_url
        }