package us.kbase.uiservice;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.Tuple2;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: UIService</p>
 * <pre>
 * A KBase module: UIService
 * </pre>
 */
public class UIServiceClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public UIServiceClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public UIServiceClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public UIServiceClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public UIServiceClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: get_alert</p>
     * <pre>
     * get_alert
     * </pre>
     * @param   id   instance of original type "AlertID"
     * @return   multiple set: (1) parameter "alert" of type {@link us.kbase.uiservice.Alert Alert}, (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<Alert, Error> getAlert(String id, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(id);
        TypeReference<Tuple2<Alert, Error>> retType = new TypeReference<Tuple2<Alert, Error>>() {};
        Tuple2<Alert, Error> res = caller.jsonrpcCall("UIService.get_alert", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: get_active_alerts</p>
     * <pre>
     * get_active_alerts
     * </pre>
     * @return   multiple set: (1) parameter "alerts" of list of type {@link us.kbase.uiservice.Alert Alert}, (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<List<Alert>, Error> getActiveAlerts(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<Tuple2<List<Alert>, Error>> retType = new TypeReference<Tuple2<List<Alert>, Error>>() {};
        Tuple2<List<Alert>, Error> res = caller.jsonrpcCall("UIService.get_active_alerts", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: search_alerts</p>
     * <pre>
     * </pre>
     * @param   query   instance of type {@link us.kbase.uiservice.AlertQuery AlertQuery}
     * @return   multiple set: (1) parameter "result" of type {@link us.kbase.uiservice.SearchAlertsResult SearchAlertsResult}, (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<SearchAlertsResult, Error> searchAlerts(AlertQuery query, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(query);
        TypeReference<Tuple2<SearchAlertsResult, Error>> retType = new TypeReference<Tuple2<SearchAlertsResult, Error>>() {};
        Tuple2<SearchAlertsResult, Error> res = caller.jsonrpcCall("UIService.search_alerts", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: search_alerts_summary</p>
     * <pre>
     * </pre>
     * @param   query   instance of type {@link us.kbase.uiservice.AlertQuery AlertQuery}
     * @return   multiple set: (1) parameter "result" of type {@link us.kbase.uiservice.AlertQueryResult AlertQueryResult}, (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<AlertQueryResult, Error> searchAlertsSummary(AlertQuery query, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(query);
        TypeReference<Tuple2<AlertQueryResult, Error>> retType = new TypeReference<Tuple2<AlertQueryResult, Error>>() {};
        Tuple2<AlertQueryResult, Error> res = caller.jsonrpcCall("UIService.search_alerts_summary", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: am_admin_user</p>
     * <pre>
     * am_admin_user
     * </pre>
     * @return   multiple set: (1) parameter "is_admin" of original type "Boolean", (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<Long, Error> amAdminUser(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<Tuple2<Long, Error>> retType = new TypeReference<Tuple2<Long, Error>>() {};
        Tuple2<Long, Error> res = caller.jsonrpcCall("UIService.am_admin_user", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: add_alert</p>
     * <pre>
     * </pre>
     * @param   alertParam   instance of type {@link us.kbase.uiservice.AddAlertParams AddAlertParams}
     * @return   multiple set: (1) parameter "result" of type {@link us.kbase.uiservice.AddAlertResult AddAlertResult}, (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<AddAlertResult, Error> addAlert(AddAlertParams alertParam, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(alertParam);
        TypeReference<Tuple2<AddAlertResult, Error>> retType = new TypeReference<Tuple2<AddAlertResult, Error>>() {};
        Tuple2<AddAlertResult, Error> res = caller.jsonrpcCall("UIService.add_alert", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: delete_alert</p>
     * <pre>
     * </pre>
     * @param   id   instance of original type "AlertID"
     * @return   multiple set: (1) parameter "result" of type {@link us.kbase.uiservice.DeleteAlertResult DeleteAlertResult}, (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<DeleteAlertResult, Error> deleteAlert(String id, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(id);
        TypeReference<Tuple2<DeleteAlertResult, Error>> retType = new TypeReference<Tuple2<DeleteAlertResult, Error>>() {};
        Tuple2<DeleteAlertResult, Error> res = caller.jsonrpcCall("UIService.delete_alert", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: is_admin_user</p>
     * <pre>
     * </pre>
     * @param   username   instance of original type "Username"
     * @return   multiple set: (1) parameter "is_admin" of original type "Boolean", (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<Long, Error> isAdminUser(String username, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(username);
        TypeReference<Tuple2<Long, Error>> retType = new TypeReference<Tuple2<Long, Error>>() {};
        Tuple2<Long, Error> res = caller.jsonrpcCall("UIService.is_admin_user", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: update_alert</p>
     * <pre>
     * </pre>
     * @param   alertParam   instance of type {@link us.kbase.uiservice.UpdateAlertParams UpdateAlertParams}
     * @return   multiple set: (1) parameter "success" of original type "Boolean", (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<Long, Error> updateAlert(UpdateAlertParams alertParam, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(alertParam);
        TypeReference<Tuple2<Long, Error>> retType = new TypeReference<Tuple2<Long, Error>>() {};
        Tuple2<Long, Error> res = caller.jsonrpcCall("UIService.update_alert", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    /**
     * <p>Original spec-file function name: set_alert_status</p>
     * <pre>
     * set_alert_status
     * </pre>
     * @param   id   instance of original type "AlertID"
     * @param   status   instance of original type "AlertStatus"
     * @return   multiple set: (1) parameter "success" of original type "Boolean", (2) parameter "error" of type {@link us.kbase.uiservice.Error Error}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Tuple2<Long, Error> setAlertStatus(String id, String status, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(id);
        args.add(status);
        TypeReference<Tuple2<Long, Error>> retType = new TypeReference<Tuple2<Long, Error>>() {};
        Tuple2<Long, Error> res = caller.jsonrpcCall("UIService.set_alert_status", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res;
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("UIService.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
