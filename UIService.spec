/*
A KBase module: UIService
*/

module UIService {
    /* BASE Types */

    typedef int Timestamp;

    typedef string Username;

    typedef int Boolean;

    typedef structure {
        string message;
        string type;
        string code;
        UnspecifiedObject info;
    } Error;

    typedef structure {
        string code;    
        UnspecifiedObject info;
    } CheckError;

    /*
        Check html url
    */
    typedef structure {
        string url;
        int timeout;
    } CheckHTMLURLParams;

    typedef structure {
        Boolean is_valid;
        CheckError error;
    } CheckHTMLURLResult;

    funcdef check_html_url(CheckHTMLURLParams param) 
        returns (CheckHTMLURLResult result, Error error) authentication required;

    /*
        Check image url
    */
    typedef structure {
        string url;
        int timeout;
        Boolean verify_ssl;
        /* int max_size; */
        /* todo: image types */
    } CheckImageURLParams;

    typedef structure {
        Boolean is_valid;
        CheckError error;
    } CheckImageURLResult;

    funcdef check_image_url(CheckImageURLParams param)
        returns (CheckImageURLResult result, Error error) authentication required;

};
