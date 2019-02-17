# -*- coding: utf-8 -*-
#BEGIN_HEADER
from UIService.UIServiceModel import UIServiceModel
from UIService.UIServiceValidation import Validation
import os
import string
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
    VERSION = "0.0.1"
    GIT_URL = "ssh://git@github.com/eapearson/kbase-sdk-module-ui-service"
    GIT_COMMIT_HASH = "9dfa12670ba51830c9e0dec892331480e9e81210"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        # self.admin_users = string.split(os.environ.get('ADMIN_USERS', ''), ' ')
        self.admin_users = config['admin-users'].split(' ')

        config = Validation.validate_config(config)

        self.db_config = config['mongo']

        self.auth_url = config['auth-url']

        #END_CONSTRUCTOR
        pass


    def get_alert(self, ctx, param):
        """
        :param param: instance of type "GetAlertParam" (get_alert) ->
           structure: parameter "id" of type "AlertID"
        :returns: multiple set - (1) parameter "alert" of type "Alert" ->
           structure: parameter "id" of type "AlertID", parameter "start_at"
           of type "Timestamp" (BASE Types), parameter "end_at" of type
           "Timestamp" (BASE Types), parameter "type" of type "AlertType",
           parameter "title" of String, parameter "message" of String,
           parameter "status" of type "AlertStatus", parameter "created_at"
           of type "Timestamp" (BASE Types), parameter "created_by" of
           String, parameter "updated_at" of type "Timestamp" (BASE Types),
           parameter "updated_by" of String, (2) parameter "error" of type
           "Error" -> structure: parameter "message" of String, parameter
           "type" of String, parameter "code" of String, parameter "info" of
           unspecified object
        """
        # ctx is the context object
        # return variables are: alert, error
        #BEGIN get_alert
        input, error = Validation.validate_get_alert_parameter(param, ctx)
        if error:
            return None, error
            
        model = UIServiceModel(
            auth_url=self.auth_url,
            admin_users=self.admin_users,
            token=ctx['token'], 
            username=ctx['user_id'],
            db_config=self.db_config)
        alert, error = model.get_alert(input['id'])
        return [alert, error]
        #END get_alert

        # At some point might do deeper type checking...
        if not isinstance(alert, dict):
            raise ValueError('Method get_alert return value ' +
                             'alert is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method get_alert return value ' +
                             'error is not type dict as required.')
        # return the results
        return [alert, error]

    def get_active_alerts(self, ctx):
        """
        get_active_alerts
        :returns: multiple set - (1) parameter "alerts" of list of type
           "Alert" -> structure: parameter "id" of type "AlertID", parameter
           "start_at" of type "Timestamp" (BASE Types), parameter "end_at" of
           type "Timestamp" (BASE Types), parameter "type" of type
           "AlertType", parameter "title" of String, parameter "message" of
           String, parameter "status" of type "AlertStatus", parameter
           "created_at" of type "Timestamp" (BASE Types), parameter
           "created_by" of String, parameter "updated_at" of type "Timestamp"
           (BASE Types), parameter "updated_by" of String, (2) parameter
           "error" of type "Error" -> structure: parameter "message" of
           String, parameter "type" of String, parameter "code" of String,
           parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: alerts, error
        #BEGIN get_active_alerts
        # print('getting active alerts... %s, %s, %s, %s, %s' % (self.auth_url, self.admin_users, ctx['token'], ctx['user_id'], self.db_config))
        model = UIServiceModel(
            auth_url=self.auth_url, 
            admin_users=self.admin_users,
            token=ctx['token'], 
            username=ctx['user_id'],
            db_config=self.db_config)
        # print('getting active alerts...')
        alerts, error = model.get_active_alerts()
        return [alerts, error]
        #END get_active_alerts

        # At some point might do deeper type checking...
        if not isinstance(alerts, list):
            raise ValueError('Method get_active_alerts return value ' +
                             'alerts is not type list as required.')
        if not isinstance(error, dict):
            raise ValueError('Method get_active_alerts return value ' +
                             'error is not type dict as required.')
        # return the results
        return [alerts, error]

    def search_alerts(self, ctx, query):
        """
        :param query: instance of type "AlertQuery" (typedef structure {
           string path; string op; string value; } SearchField; typedef
           structure { string op; list<SearchField> args; }
           SearchSubExpression; typedef structure { SearchField field;
           SearchSubExpression expression; } SearchArg; typedef structure {
           string op; list<SearchArg> args; } SearchExpression;) ->
           structure: parameter "query" of type "SearchExpression" (I give up
           ...) -> unspecified object, parameter "paging" of type
           "PagingSpec" (search_alerts) -> structure: parameter "start" of
           Long, parameter "limit" of Long, parameter "sorting" of list of
           type "SortSpec" -> structure: parameter "field" of String,
           parameter "is_descending" of type "Boolean"
        :returns: multiple set - (1) parameter "result" of type
           "SearchAlertsResult" -> structure: parameter "alerts" of list of
           type "Alert" -> structure: parameter "id" of type "AlertID",
           parameter "start_at" of type "Timestamp" (BASE Types), parameter
           "end_at" of type "Timestamp" (BASE Types), parameter "type" of
           type "AlertType", parameter "title" of String, parameter "message"
           of String, parameter "status" of type "AlertStatus", parameter
           "created_at" of type "Timestamp" (BASE Types), parameter
           "created_by" of String, parameter "updated_at" of type "Timestamp"
           (BASE Types), parameter "updated_by" of String, (2) parameter
           "error" of type "Error" -> structure: parameter "message" of
           String, parameter "type" of String, parameter "code" of String,
           parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: result, error
        #BEGIN search_alerts
        query2, error = Validation.validate_search_alerts_parameter(query, ctx)
        if error:
            return None, error

        model = UIServiceModel(
            auth_url=self.auth_url, 
            admin_users=self.admin_users,
            token=ctx['token'],
            username=ctx['user_id'],
            db_config=self.db_config)

        result, error = model.search_alerts(query2)
        if error:
            return None, error

        return [{
            'alerts': result
        }, None]

        #END search_alerts

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method search_alerts return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method search_alerts return value ' +
                             'error is not type dict as required.')
        # return the results
        return [result, error]

    def search_alerts_summary(self, ctx, query):
        """
        :param query: instance of type "SearchExpression" (I give up ...) ->
           unspecified object
        :returns: multiple set - (1) parameter "result" of type
           "SearchAlertsSummaryResult" -> structure: parameter "statuses" of
           mapping from String to Long, (2) parameter "error" of type "Error"
           -> structure: parameter "message" of String, parameter "type" of
           String, parameter "code" of String, parameter "info" of
           unspecified object
        """
        # ctx is the context object
        # return variables are: result, error
        #BEGIN search_alerts_summary
        query2, error = Validation.validate_search_alerts_summary_parameter(query, ctx)
        if error:
            return None, error

        model = UIServiceModel(
            auth_url=self.auth_url, 
            admin_users=self.admin_users,
            token=ctx['token'],
            username=ctx['user_id'],
            db_config=self.db_config)

        result, error = model.search_alerts_summary(query2)
        if error:
            return None, error

        return [{
            'alerts_summary': result
        }, None]
        #END search_alerts_summary

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method search_alerts_summary return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method search_alerts_summary return value ' +
                             'error is not type dict as required.')
        # return the results
        return [result, error]

    def am_admin_user(self, ctx):
        """
        am_admin_user
        :returns: multiple set - (1) parameter "is_admin" of type "Boolean",
           (2) parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: is_admin, error
        #BEGIN am_admin_user
        is_admin = ctx['user_id'] in self.admin_users
        return [is_admin, None]
        #END am_admin_user

        # At some point might do deeper type checking...
        if not isinstance(is_admin, int):
            raise ValueError('Method am_admin_user return value ' +
                             'is_admin is not type int as required.')
        if not isinstance(error, dict):
            raise ValueError('Method am_admin_user return value ' +
                             'error is not type dict as required.')
        # return the results
        return [is_admin, error]

    def add_alert(self, ctx, alert_param):
        """
        :param alert_param: instance of type "AddAlertParam" (add_alert) ->
           structure: parameter "alert" of type "Alert" -> structure:
           parameter "id" of type "AlertID", parameter "start_at" of type
           "Timestamp" (BASE Types), parameter "end_at" of type "Timestamp"
           (BASE Types), parameter "type" of type "AlertType", parameter
           "title" of String, parameter "message" of String, parameter
           "status" of type "AlertStatus", parameter "created_at" of type
           "Timestamp" (BASE Types), parameter "created_by" of String,
           parameter "updated_at" of type "Timestamp" (BASE Types), parameter
           "updated_by" of String
        :returns: multiple set - (1) parameter "result" of type
           "AddAlertResult" -> structure: parameter "id" of type "AlertID",
           (2) parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: result, error
        #BEGIN add_alert
        model = UIServiceModel(
            auth_url=self.auth_url, 
            admin_users=self.admin_users,
            token=ctx['token'], 
            username=ctx['user_id'],
            db_config=self.db_config)
        result = {
            'id': model.add_alert(alert_param['alert'])
        }
        return [result, None]
        #END add_alert

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method add_alert return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method add_alert return value ' +
                             'error is not type dict as required.')
        # return the results
        return [result, error]

    def delete_alert(self, ctx, id):
        """
        :param id: instance of type "AlertID"
        :returns: multiple set - (1) parameter "result" of type
           "DeleteAlertResult" -> structure: parameter "id" of type
           "AlertID", (2) parameter "error" of type "Error" -> structure:
           parameter "message" of String, parameter "type" of String,
           parameter "code" of String, parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: result, error
        #BEGIN delete_alert
        model = UIServiceModel(
            auth_url=self.auth_url, 
            admin_users=self.admin_users,
            token=ctx['token'],
            username=ctx['user_id'],
            db_config=self.db_config)
        model.delete_alert(id)
        result = {'id': id}
        return [result, None]
        #END delete_alert

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method delete_alert return value ' +
                             'result is not type dict as required.')
        if not isinstance(error, dict):
            raise ValueError('Method delete_alert return value ' +
                             'error is not type dict as required.')
        # return the results
        return [result, error]

    def is_admin_user(self, ctx, param):
        """
        :param param: instance of type "IsAdminUserParam" -> structure:
           parameter "username" of type "Username"
        :returns: multiple set - (1) parameter "is_admin" of type "Boolean",
           (2) parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: is_admin, error
        #BEGIN is_admin_user
        param, error = Validation.validate_is_admin_user(param, ctx)
        if error:
            return None, error

        # This uses the admin user stored in the model...   
        model = UIServiceModel(
            auth_url=self.auth_url, 
            admin_users=self.admin_users,
            token=ctx['token'],
            username=ctx['user_id'],
            db_config=self.db_config)
        is_admin = model.is_admin_user(param['username'])
        return [is_admin, None]
        #END is_admin_user

        # At some point might do deeper type checking...
        if not isinstance(is_admin, int):
            raise ValueError('Method is_admin_user return value ' +
                             'is_admin is not type int as required.')
        if not isinstance(error, dict):
            raise ValueError('Method is_admin_user return value ' +
                             'error is not type dict as required.')
        # return the results
        return [is_admin, error]

    def update_alert(self, ctx, alert_param):
        """
        :param alert_param: instance of type "UpdateAlertParams" (update
           alert) -> structure: parameter "alert" of type "Alert" ->
           structure: parameter "id" of type "AlertID", parameter "start_at"
           of type "Timestamp" (BASE Types), parameter "end_at" of type
           "Timestamp" (BASE Types), parameter "type" of type "AlertType",
           parameter "title" of String, parameter "message" of String,
           parameter "status" of type "AlertStatus", parameter "created_at"
           of type "Timestamp" (BASE Types), parameter "created_by" of
           String, parameter "updated_at" of type "Timestamp" (BASE Types),
           parameter "updated_by" of String
        :returns: multiple set - (1) parameter "success" of type "Boolean",
           (2) parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: success, error
        #BEGIN update_alert
        model = UIServiceModel(
            auth_url=self.auth_url, 
            admin_users=self.admin_users,
            token=ctx['token'], 
            username=ctx['user_id'],
            db_config=self.db_config)
        model.update_alert(alert_param['alert'])
        success = True
        return [success, None]
        #END update_alert

        # At some point might do deeper type checking...
        if not isinstance(success, int):
            raise ValueError('Method update_alert return value ' +
                             'success is not type int as required.')
        if not isinstance(error, dict):
            raise ValueError('Method update_alert return value ' +
                             'error is not type dict as required.')
        # return the results
        return [success, error]

    def set_alert(self, ctx, alert_param):
        """
        :param alert_param: instance of type "UpdateAlertParams" (update
           alert) -> structure: parameter "alert" of type "Alert" ->
           structure: parameter "id" of type "AlertID", parameter "start_at"
           of type "Timestamp" (BASE Types), parameter "end_at" of type
           "Timestamp" (BASE Types), parameter "type" of type "AlertType",
           parameter "title" of String, parameter "message" of String,
           parameter "status" of type "AlertStatus", parameter "created_at"
           of type "Timestamp" (BASE Types), parameter "created_by" of
           String, parameter "updated_at" of type "Timestamp" (BASE Types),
           parameter "updated_by" of String
        :returns: multiple set - (1) parameter "success" of type "Boolean",
           (2) parameter "error" of type "Error" -> structure: parameter
           "message" of String, parameter "type" of String, parameter "code"
           of String, parameter "info" of unspecified object
        """
        # ctx is the context object
        # return variables are: success, error
        #BEGIN set_alert
        model = UIServiceModel(
            auth_url=self.auth_url, 
            admin_users=self.admin_users,
            token=ctx['token'], 
            username=ctx['user_id'],
            db_config=self.db_config)
        model.set_alert(alert_param['alert'])
        success = True
        return [success, None]
        #END set_alert

        # At some point might do deeper type checking...
        if not isinstance(success, int):
            raise ValueError('Method set_alert return value ' +
                             'success is not type int as required.')
        if not isinstance(error, dict):
            raise ValueError('Method set_alert return value ' +
                             'error is not type dict as required.')
        # return the results
        return [success, error]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
