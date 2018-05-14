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
        list<string> message;
        AlertStatus status;
    } Alert;


    /* METHODS and their in/out types */

    /* 
        add_alert 
    */
    typedef structure {
        Alert alert;
    } AddAlertParams;

    typedef structure {
        AlertID id;
    } AddAlertResultl;

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

    typedef UnspecifiedObject Query;

    funcdef search_alerts(Query query)
        returns (list<Alert> alerts) authentication required;


    /*
        am_admin_user
    */

    funcdef am_admin_user()
        returns (Boolean is_admin) authentication required;


    /* ADMIN */

    funcdef add_alert(AddAlertParams alert)
        returns (AlertID alert_id) authentication required;

    funcdef delete_alert(AlertID id)
        returns () authentication required;

    funcdef is_admin_user(Username username)
        returns (Boolean is_admin) authentication required;

    funcdef update_alert(AddAlertParams alert)
        returns () authentication required;

    /*
        set_alert_status
    */

    funcdef set_alert_status(AlertID id, AlertStatus status)
        returns () authentication required;


};
