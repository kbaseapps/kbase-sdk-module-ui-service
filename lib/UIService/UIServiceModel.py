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

class UIServiceModel(object):
    def __init__(self, auth_url=None, token=None, username=None, admin_users=None, db_config=None):

        self.token = token
        self.username = username
        self.admin_users = admin_users

        self.mongo_host = db_config['host']
        self.mongo_port = int(db_config['port'])
        self.mongo_db = db_config['db']
        self.mongo_user = db_config['user']
        self.mongo_pwd = db_config['password']
        # print('mongo: creating mongo client')
        self.mongo = pymongo.MongoClient(self.mongo_host, self.mongo_port, serverSelectionTimeoutMS=1000)
        # print('mongo: authenticating')
        self.db = self.mongo[self.mongo_db]
        self.db.authenticate(self.mongo_user, urllib.parse.quote_plus(self.mongo_pwd))
        # print('mongo: authenticated')

    @staticmethod
    def iso_to_iso(datetime_string):
        if datetime_string is None:
            return None;
        d = parse(datetime_string, ignoretz=False)
        d_utc = d.astimezone(pytz.timezone('UTC'))
        return d_utc.replace(microsecond=0).isoformat()

    @staticmethod
    def now_to_iso():
        d = datetime.datetime.utcnow()
        tz = pytz.timezone('UTC')
        return d.replace(microsecond=0).replace(tzinfo=tz).isoformat()

    def add_alert(self, alert):
        admin_user = self.ensure_admin_authorization()

        collection = self.db.alerts

        # TODO: validate alert
        alert_id = str(uuid.uuid4())

        alert_doc = {
            'id': alert_id,
            'title': alert.get('title', None),
            'message': alert.get('message', None),
            'start_at': self.iso_to_iso(alert.get('start_at', None)),
            'end_at': self.iso_to_iso(alert.get('end_at', None)),
            'status': alert.get('status'),
            'created_at': self.now_to_iso(),
            'created_by': admin_user
        }

        collection.insert(alert_doc)

        return alert_id

    def update_alert(self, alert):
        admin_user = self.ensure_admin_authorization()

        collection = self.db.alerts

        updates = {}

        for field_name in ['title', 'message', 'status']:
            if field_name in alert:
                updates[field_name] = alert[field_name]

        for field_name in ['start_at', 'end_at']:
            if field_name in alert:
                updates[field_name] =  self.iso_to_iso(alert[field_name])

        updates['updated_at'] = self.now_to_iso()
        updates['updated_by'] = admin_user

        collection.update(
            {
                'id': {'$eq': alert['id']}
            },
            {'$set': updates}
        )

        return alert['id']

    def set_alert(self, alert):
        admin_user = self.ensure_admin_authorization()

        collection = self.db.alerts

        collection.update(
            {
                'id': {'$eq': alert['id']}
            },
            {'$set': {
                'title': alert.get('title', None),
                'message': alert.get('message', None),
                'start_at': self.iso_to_iso(alert.get('start_at', None)),
                'end_at': self.iso_to_iso(alert.get('end_at', None)),
                'status': alert.get('status'),
                'updated_at': self.now_to_iso(),
                'updated_by': admin_user
            }}
        )

        return alert['id']

    def get_active_alerts(self):
        collection = self.db.alerts
        now = self.now_to_iso()
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

        return alerts_json, None

    def search_query_to_mongo(self, query):
        find_expression = {}
        exprs = []

        for arg in query['args']:
            expr = {}

            if arg['op'] in ['and', 'or', 'nor', 'not']:
                # subexpression
                expr = self.search_query_to_mongo(arg)
            elif arg['op'] in ['eq', 'gt', 'lt', 'gte', 'lte', 'ne']:
                # field expression
                op = '$' + arg['op']
                expr_value = {}
                expr_value[op] = arg['value']
                expr[arg['path']] = expr_value
            else:
                raise ValueError('Invalid search argument operator: ' + arg['op'])

            exprs.append(expr)

        if query['op'] in ['and', 'or', 'nor', 'not']:
            query_op = '$' + query['op']
        else:
            raise ValueError('Invalid query operator: ' + query['op'])

        find_expression[query_op] = exprs
        return find_expression


    def search_alerts(self, search_query):
        # todo: support query!
        collection = self.db.alerts

        # if search_query['query'] and len(search_query['query']['args']) > 0:
        # print(str(find_expression))
        try:
            find_expression = self.search_query_to_mongo(search_query['query'])
        except ValueError as ex:
            return None, {
                'message': ex.message,
                'type': 'input',
                'code': 'invalid',
                'info': {}
            }

        alerts = collection.find(find_expression)
        alerts_json = []
        for alert in alerts:
            alert_json = json.loads(json_util.dumps(alert))
            alerts_json.append(alert_json)
        return alerts_json, None

    def search_alerts_summary(self, search_query):
        # todo: support query!
        collection = self.db.alerts

        # if search_query['query'] and len(search_query['query']['args']) > 0:
        # print(str(find_expression))
        try:
            find_expression = self.search_query_to_mongo(search_query['query'])
        except ValueError as ex:
            return None, {
                'message': ex.message,
                'type': 'input',
                'code': 'invalid',
                'info': {}
            }

        group_expression = {
            '_id': '$status',
            'count': {
                '$sum': 1
            }
        }

        pipeline_expression = [
            {'$match': find_expression},
            {'$group': group_expression}
        ]

        cursor = collection.aggregate(pipeline_expression, cursor={})

        alerts_summary = {}
        for doc in cursor:
            alerts_summary[doc['_id']] = doc['count']

        return alerts_summary, None

    def get_alert(self, alert_id):
        collection = self.db.alerts

        alert = collection.find_one({
            'id': {'$eq': alert_id}
        })

        if alert is None:
            return None, None
            # return None, {
            #     'message': 'An alert was not found',
            #     'type': 'data',
            #     'code': 'notfound',
            #     'info': {
            #         'id': alert_id
            #     }
            # }

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
            print('admin users? %s' % (self.admin_users))
            raise ValueError('Not admin user')

        return self.username

    def is_admin_user(self, username):
        self.ensure_admin_authorization()
        return username in self.admin_users
