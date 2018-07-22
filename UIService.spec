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
    typedef structure {
        AlertID id;
    } GetAlertParam;

    funcdef get_alert(GetAlertParam param) 
        returns (Alert alert, Error error) authentication required;

    /*
        get_active_alerts
    */

    funcdef get_active_alerts()
        returns (list<Alert> alerts, Error error) authentication optional;

    /*
        search_alerts
    */

  

    typedef structure {
        int start;
        int limit;
    } PagingSpec;

    typedef structure {
        string field;
        Boolean is_descending;
    } SortSpec;

    /* union type: either field or field_set */

    /* I give up ... */

    typedef UnspecifiedObject SearchExpression;

    /*
    typedef structure {
        string path;        
        string op; 
        string value;
    } SearchField;


    typedef structure {
        string op;
        list<SearchField> args;
    } SearchSubExpression;


    typedef structure {
        SearchField field;
        SearchSubExpression expression;
    } SearchArg;

    typedef structure {
        string op;
        list<SearchArg> args;
    } SearchExpression;
    */

    typedef structure {
        SearchExpression query;
        PagingSpec paging;
        list<SortSpec> sorting;
    } AlertQuery;

    typedef structure {
        list<Alert> alerts;
    } SearchAlertsResult;

    funcdef search_alerts(AlertQuery query)
        returns (SearchAlertsResult result, Error error);



    typedef  structure {
        mapping<string,int> statuses;
    } SearchAlertsSummaryResult;

    funcdef search_alerts_summary(SearchExpression query)
        returns (SearchAlertsSummaryResult result, Error error);


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
    } AddAlertParam;

    typedef structure {
        AlertID id;
    } AddAlertResult;

    funcdef add_alert(AddAlertParam alert_param)
        returns (AddAlertResult result, Error error) authentication required;

    typedef structure {
        AlertID id;
    } DeleteAlertResult;

    funcdef delete_alert(AlertID id)
        returns (DeleteAlertResult result, Error error) authentication required;

    typedef structure {
        Username username;
    } IsAdminUserParam;

    funcdef is_admin_user(IsAdminUserParam param)
        returns (Boolean is_admin, Error error) authentication required;

     /* 
        update alert 
    */
    typedef structure {
        Alert alert;
    } UpdateAlertParams;

    funcdef update_alert(UpdateAlertParams alert_param)
        returns (Boolean success, Error error) authentication required;

    funcdef set_alert(UpdateAlertParams alert_param)
        returns (Boolean success, Error error) authentication required;

};
