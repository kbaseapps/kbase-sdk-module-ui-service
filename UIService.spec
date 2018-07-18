/*
A KBase module: UIService
*/

module UIService {
    /* BASE Types */

    typedef int Timestamp;

    typedef string AlertStatus;

    typedef string AlertType;

    typedef string AlertID;

    typedef string Username;

    typedef int Boolean;

    typedef structure {
        AlertID id;
        Timestamp start_at;
        Timestamp end_at;
        AlertType type;
        string title;
        string message;
        AlertStatus status;
        Timestamp created_at;
        string created_by;
        Timestamp updated_at;
        string updated_by;
    } Alert;

    typedef structure {
        string message;
        string type;
        string code;
        UnspecifiedObject info;
    } Error;


    /* METHODS and their in/out types */

   
    /* 
        get_alert 
    */
    funcdef get_alert(AlertID id) 
        returns (Alert alert, Error error) authentication required;

    /*
        get_active_alerts
    */

    funcdef get_active_alerts()
        returns (list<Alert> alerts, Error error) authentication optional;

    /*
        search_alerts
    */

    /* typedef UnspecifiedObject Query; */

    typedef structure {
        int start;
        int limit;
    } PagingSpec;

    typedef structure {
        string field;
        Boolean is_descending;
    } SortSpec;

    typedef structure {
        string path;        
        string op; 
        string value;
    } SearchField;


    /*
    typedef structure {
        string op;
        list<SearchArg> args;
    } SearchSubExpression;
    */

    /* union type: either field or field_set */
    /*
    typedef structure {
        SearchField field;
        SearchSubExpression expression;
    } SearchArg;
    */

    typedef structure {
        string op;
        list<SearchField> args;
    } SearchExpression;

    typedef structure {
        SearchExpression query;
        PagingSpec page;
        list<SortSpec> sorting;
    } AlertQuery;

    typedef structure {
        list<Alert> alerts;
    } SearchAlertsResult;

    funcdef search_alerts(AlertQuery query)
        returns (SearchAlertsResult result, Error error);

    typedef  structure {
        mapping<string,int> statuses;
    } AlertQueryResult;

    funcdef search_alerts_summary(AlertQuery query)
        returns (AlertQueryResult result, Error error);


    /*
        am_admin_user
    */

    funcdef am_admin_user()
        returns (Boolean is_admin, Error error) authentication required;


    /* ADMIN */

    /* 
        add_alert 
    */

    typedef structure {
        Alert alert;
    } AddAlertParams;

    typedef structure {
        AlertID id;
    } AddAlertResult;

    funcdef add_alert(AddAlertParams alert_param)
        returns (AddAlertResult result, Error error) authentication required;

    typedef structure {
        AlertID id;
    } DeleteAlertResult;

    funcdef delete_alert(AlertID id)
        returns (DeleteAlertResult result, Error error) authentication required;

    funcdef is_admin_user(Username username)
        returns (Boolean is_admin, Error error) authentication required;

     /* 
        update alert 
    */
    typedef structure {
        Alert alert;
    } UpdateAlertParams;

    funcdef update_alert(UpdateAlertParams alert_param)
        returns (Boolean success, Error error) authentication required;

    /*
        set_alert_status
    */

    funcdef set_alert_status(AlertID id, AlertStatus status)
        returns (Boolean success, Error error) authentication required;


};
