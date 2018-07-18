import sqlite3
from dateutil.parser import parse
# import datetime
import pytz
import json
from UIService.RESTClient import RESTClient


def iso_to_sqlite_datetime(datetime_string):
    d = parse(datetime_string)
    t = d.astimezone(pytz.timezone('UTC'))
    return t.strftime('%Y-%m-%d %H:%M:%S')


def sqlite_to_iso_datetime(sqlite_datetime):
    d = parse(sqlite_datetime)
    return d.isoformat() + 'Z'


class UIServiceModel(object):
    def __init__(self, path=None, auth_url=None, token=None, username=None, admin_users=None, db_config=None):
        if path is None:
            raise ValueError('The "path" argument is required')
        if not isinstance(path, basestring):
            raise ValueError('The "path" argument must be a string')
        self.path = path

        self.token = token
        self.username = username
        self.admin_users = admin_users

        # Mongo boilerplate
        if db_config is None:
            raise ValueError('The database configuration was not provided')

  
        # print("auth,token: %s, %s" % (auth_url, token))
        # if auth_url is not None and token is not None:
        #     client = RESTClient(url=auth_url, token=token)
        #     result, error = client.get(path='api/V2/me')
        #     if result is None:
        #         raise ValueError('Token invalid')
        #     # print("got auth! %s %s" % (result, error))
        #     self.username = result.get('user')
        # else:
        #     self.username = None

    def connect(self):
        self.conn = sqlite3.connect(self.path, isolation_level=None)
        self.conn.execute('pragma journal_mode=wal;')

    def disconnect(self):
        self.conn.execute('pragma optimize')
        self.conn.close()

    def initialize(self):
        self.connect()
        self.create_schema()
        self.disconnect()
 
    def create_schema(self):
        alerts_schema = '''
        drop table if exists admin_users;
        drop table if exists alerts;
        drop table if exists alert_status;
        create table if not exists alert_status (
            status text not null primary key,

            description text null
        );
        insert into alert_status(status, description)
          values ('pending', 'Pending release');
        insert into alert_status(status, description)
          values ('published', 'Alert is published to users');
        insert into alert_status(status, description)
          values ('canceled', 'Alert has been canceled');
        create table if not exists alerts (
            alert_id integer not null primary key autoincrement,

            status text not null,
            start_at timestamp null,
            end_at timestamp null,
            title text null,
            message text null,

            foreign key (status)
              references alert_status(status)
        );
        create table admin_users (
            username text not null primary key,
            created_at timestamp not null
        );
        '''
        # insert into admin_users
        # (username, created_at)
        # values
        # ('kbase_ui_service_admin', CURRENT_TIMESTAMP)
        cursor = self.conn.cursor()
        cursor.executescript(alerts_schema)
        cursor.close()

    def add_alert(self, alert):
        self.ensure_admin_authorization()

        fields = ['status', 'start_at', 'end_at', 'title', 'message']
        placeholders = ','.join(['?' for _ in fields])
        columns = ','.join(fields)
        sql = '''
        insert into alerts
          ({})
        values
          ({})
        '''.format(columns, placeholders)
        params = [
            alert['status'],
            iso_to_sqlite_datetime(alert['start_at']),
            iso_to_sqlite_datetime(alert['end_at']),
            alert['title'],
            alert['message']
            # json.dumps(alert['message'])
        ]

        # params = [alert.get(field) for field in fields]
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(params))
        alert_id = cursor.lastrowid
        cursor.close()
        self.disconnect()
        return alert_id

    def update_alert(self, alert):
        self.ensure_admin_authorization()

        fields = ['status', 'start_at', 'end_at', 'title', 'message']
        updates = ','.join(list(map(lambda field: '%s = ?' % (field), fields)))
        # for now we do a full update, not partial
        sql = '''
        update alerts
        set {}
        where alert_id = ?
        '''.format(updates)
        params = [
            alert['status'],
            iso_to_sqlite_datetime(alert['start_at']),
            iso_to_sqlite_datetime(alert['end_at']),
            alert['title'],
            alert['message'],
            alert['id']
        ]

        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql, tuple(params))
        alert_id = cursor.lastrowid
        cursor.close()
        self.disconnect()
        return alert_id

    def get_active_alerts(self):
        # todo add time comparison too
        sql = '''
        select alert_id, status, start_at, end_at, title, message
        from alerts
        where status = 'published'
        '''
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = []
        for (alert_id, status, start_at, end_at, title, message) in cursor:
            result.append({
                'id': alert_id,
                'status': status,
                'startAt': sqlite_to_iso_datetime(start_at),
                'endAt': sqlite_to_iso_datetime(end_at),
                'title': title,
                'message': message
                # 'message': json.loads(message)
            })
        cursor.close()
        self.disconnect()
        return result

    def search_alerts(self, query):
        # todo add time comparison too
        sql = '''
        select alert_id, status, start_at, end_at, title, message
        from alerts
        '''
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = []
        for (alert_id, status, start_at, end_at, title, message) in cursor:
            result.append({
                'id': alert_id,
                'status': status,
                'startAt': sqlite_to_iso_datetime(start_at),
                'endAt': sqlite_to_iso_datetime(end_at),
                'title': title,
                'message': message
                # 'message': json.loads(message)
            })
        cursor.close()
        self.disconnect()
        return result

    def get_alert(self, alert_id):
        # todo add time comparison too
        sql = '''
        select alert_id, status, start_at, end_at, title, message
        from alerts
        where alert_id = ?
        '''
        params = [alert_id]
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        result = []
        for (alert_id, status, start_at, end_at, title, message) in cursor:
            result.append({
                'id': alert_id,
                'status': status,
                'startAt': sqlite_to_iso_datetime(start_at),
                'endAt': sqlite_to_iso_datetime(end_at),
                'title': title,
                'message': message
                # 'message': json.loads(message)
            })
        cursor.disconnect()
        self.disconnect()
        if len(result) > 1:
            raise ValueError('Too manu results for get_alert for %s' % (alert_id))
        return result[0]

    def delete_alert(self, alert_id):
        self.ensure_admin_authorization()

        # todo add time comparison too
        sql = '''
        delete
        from alerts
        where alert_id = ?
        '''
        params = [alert_id]
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        cursor.close()
        self.disconnect()

    def ensure_admin_authorization(self):
        if self.token is None:
            raise ValueError('No authorization token')

        if not self.username in self.admin_users:
            raise ValueError('Not admin user')

        pass

    def is_admin_user(self, username):
        self.ensure_admin_authorization()
        return username in self.admin_users
        # sql = '''
        # select exists(select 1 from admin_users where username = ?)
        # '''
        # params = [username]
        # self.connect()
        # cursor = self.conn.cursor()
        # cursor.execute(sql, params)
        # is_admin = cursor.fetchone()[0]
        # cursor.close()
        # self.disconnect()
        # if is_admin:
        #     return True
        # else:
        #     return False

    def authorized_user_is_admin(self):
        if self.token is None:
            raise ValueError('No authorization token')

        if self.username is None:
            raise ValueError('No authorized user')

        return self.is_admin_user(self.username)
