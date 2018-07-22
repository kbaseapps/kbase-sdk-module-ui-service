
package us.kbase.uiservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: AddAlertParam</p>
 * <pre>
 * add_alert
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "alert"
})
public class AddAlertParam {

    /**
     * <p>Original spec-file type: Alert</p>
     * 
     * 
     */
    @JsonProperty("alert")
    private Alert alert;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: Alert</p>
     * 
     * 
     */
    @JsonProperty("alert")
    public Alert getAlert() {
        return alert;
    }

    /**
     * <p>Original spec-file type: Alert</p>
     * 
     * 
     */
    @JsonProperty("alert")
    public void setAlert(Alert alert) {
        this.alert = alert;
    }

    public AddAlertParam withAlert(Alert alert) {
        this.alert = alert;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("AddAlertParam"+" [alert=")+ alert)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
