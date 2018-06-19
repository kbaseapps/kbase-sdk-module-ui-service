/*
A KBase module: UIService
*/

module UIService {
    /* BASE Types */

    typedef int Timestamp;

    typedef string AlertStatus;

    typedef string AlertType;

    typedef int AlertID;

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
    } Alert;


    /* METHODS and their in/out types */

   
    /* 
        get_alert 
    */
    funcdef get_alert(AlertID id) 
        returns (Alert alert) authentication required;

    /*
        get_active_alerts
    */

    funcdef get_active_alerts()
        returns (list<Alert> alerts) authentication optional;

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
        string field;
        string operator;
    } SearchSpec;

    typedef structure {
        SearchSpec search;
        PagingSpec page;
        list<SortSpec> sorting;
    } AlertQuery;

    typedef structure {
        list<Alert> alerts;
    } SearchAlertsResult;

    funcdef search_alerts(AlertQuery query)
        returns (SearchAlertsResult result);

    typedef  structure {
        mapping<string,int> statuses;
    } AlertQueryResult;

    funcdef search_alerts_summary(AlertQuery query)
        returns (AlertQueryResult result);


    /*
        am_admin_user
    */

    funcdef am_admin_user()
        returns (Boolean is_admin) authentication required;


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
        returns (AddAlertResult result) authentication required;

    funcdef delete_alert(AlertID id)
        returns () authentication required;

    funcdef is_admin_user(Username username)
        returns (Boolean is_admin) authentication required;

     /* 
        update alert 
    */
    typedef structure {
        Alert alert;
    } UpdateAlertParams;

    funcdef update_alert(UpdateAlertParams alert_param)
        returns () authentication required;

    /*
        set_alert_status
    */

    funcdef set_alert_status(AlertID id, AlertStatus status)
        returns () authentication required;


};
