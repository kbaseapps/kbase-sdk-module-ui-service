import requests
import json


class RESTClient(object):
    def __init__(self, url=None, token=None):
        if url is None:
            raise ValueError('The "url" argument is required')

        self.token = token
        self.url = url

    def post(self, data):
        header = {
            'Content-Type': 'application/json'
        }
        if self.token:
            header['Authorization'] = self.token

        r = requests.post(self.url, headers=header, data=json.dumps(data), timeout=60)
        if r.headers['content-type'].startswith('application/json'):
            result = r.json()
            return result.get('result'), result.get('error')

        r.raise_for_status()
        raise ValueError('Invalid response; not json, not an error status')
        
    def get(self, path=None):
        if path is None:
            raise ValueError('The "path" argument is required')

        header = dict()
        if self.token:
            header['Authorization'] = self.token
        url = self.url + '/' + path
        r = requests.get(url, headers=header, timeout=60)
        if r.headers['content-type'].startswith('application/json'):
            result = r.json()
            return result, None

        r.raise_for_status()
        raise ValueError('Invalid response; not json, not an error status')
