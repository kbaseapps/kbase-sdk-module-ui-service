# import sqlite3
from dateutil.parser import parse
import datetime
import pytz
import json
# mongodb
import pymongo
import urllib
import uuid
import calendar
import time
from bson import json_util
from UIService.RESTClient import RESTClient

def now_to_iso():
    d = datetime.datetime.utcnow()
    tz = pytz.timezone('UTC')
    return d.replace(microsecond=0).replace(tzinfo=tz).isoformat()

def iso_to_iso(datetime_string):
    if datetime_string is None:
        return None;
    d = parse(datetime_string, ignoretz=False)
    d_utc = d.astimezone(pytz.timezone('UTC'))
    return d_utc.replace(microsecond=0).isoformat()

class UIServiceModel(object):
    def __init__(self, auth_url=None, token=None, username=None, admin_users=None, db_config=None):

        self.token = token
        self.username = username
        self.admin_users = admin_users

        # Mongo boilerplate
        if db_config is None:
            raise ValueError('The database configuration was not provided')
    
        self.mongo_host = db_config['host']
        self.mongo_port = int(db_config['port'])
        self.mongo_db = db_config['db']
        self.mongo_user = db_config['user']
        self.mongo_pwd = db_config['password']
        self.mongo = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.db = self.mongo[self.mongo_db]
        self.db.authenticate(self.mongo_user, urllib.quote_plus(self.mongo_pwd))

    def add_alert(self, alert):
        admin_user = self.ensure_admin_authorization()

        collection = self.db.alerts

        # TODO: validate alert
        alert_id = str(uuid.uuid4())

        alert_doc = {
            'id': alert_id,
            'title': alert['title'],
            'message': alert['message'],
            'start_at': iso_to_iso(alert['start_at']),
            'end_at': iso_to_iso(alert['end_at']),
            'status': alert['status'],
            'created_at': now_to_iso(),
            'created_by': admin_user
        }

        collection.insert(alert_doc)

        return alert_id

    def update_alert(self, alert):
        admin_user = self.ensure_admin_authorization()

        collection = self.db.alerts

        collection.update(
            {
                'id': {'$eq': alert['id']}
            },
            {'$set': {
                'title': alert['title'],
                'message': alert['message'],
                'start_at': iso_to_iso(alert['start_at']),
                'end_at': iso_to_iso(alert['end_at']),
                'status': alert['status'],
                'updated_at': now_to_iso(),
                'updated_by': admin_user
            }}
        )

        return alert['id']

    def get_active_alerts(self):
        collection = self.db.alerts
        now = now_to_iso()
        alerts = collection.find({
            '$and': [
                {'status': {'$eq': 'published'}},
                {'$or': [
                    {'end_at': {'$gte': now}},
                    {'$and': [
                        {'start_at': {'$lte': now}},
                        {'end_at': {'$eq': None}}
                    ]}
                ]}
            ]
        })

        alerts_json = []
        for alert in alerts:
            alert_json = json.loads(json_util.dumps(alert))
            alerts_json.append(alert_json)

        return alerts_json

    def search_alerts(self, search_query):
        # todo: support query!
        collection = self.db.alerts

        find_expression = {}

        if search_query['query'] and len(search_query['query']['args']) > 0:
            exprs = []
            query = search_query['query']
            for arg in query['args']:
                expr = {}

                if arg['op'] in ['eq', 'gt', 'lt', 'gte', 'lte', 'ne']:
                    op = '$' + arg['op']
                else:
                    raise ValueError('Invalid search argument comparison operator: ' + arg['op'])

                expr_value = {}
                expr_value[op] = arg['value']
                expr[arg['path']] = expr_value
                exprs.append(expr)


            if query['op'] in ['and', 'or', 'nor', 'not']:
                query_op = '$' + query['op']
            else:
                raise ValueError('Invalid query operator: ' + query['op'])

            find_expression[query_op] = exprs

        # print(str(find_expression))

        alerts = collection.find(find_expression)
        alerts_json = []
        for alert in alerts:
            alert_json = json.loads(json_util.dumps(alert))
            alerts_json.append(alert_json)
        return alerts_json

    def get_alert(self, alert_id):
        collection = self.db.alerts

        alert = collection.find_one({
            'id': {'$eq': alert_id}
        })

        if alert is None:
            return None, {
                'message': 'An alert was not found',
                'type': 'data',
                'code': 'notfound',
                'info': {
                    'id': alert_id
                }
            }

        alert_json = json.loads(json_util.dumps(alert))
        return alert_json, None

    def delete_alert(self, alert_id):
        self.ensure_admin_authorization()

        collection = self.db.alerts

        collection.remove({
            'id': {'$eq': alert_id}
        })

    def ensure_admin_authorization(self):
        if self.token is None:
            raise ValueError('No authorization token')

        if not self.username in self.admin_users:
            raise ValueError('Not admin user')

        return self.username

    def is_admin_user(self, username):
        self.ensure_admin_authorization()
        return username in self.admin_users
