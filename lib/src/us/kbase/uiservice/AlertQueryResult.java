
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
 * <p>Original spec-file type: AlertQueryResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "statuses"
})
public class AlertQueryResult {

    @JsonProperty("statuses")
    private Map<String, Long> statuses;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("statuses")
    public Map<String, Long> getStatuses() {
        return statuses;
    }

    @JsonProperty("statuses")
    public void setStatuses(Map<String, Long> statuses) {
        this.statuses = statuses;
    }

    public AlertQueryResult withStatuses(Map<String, Long> statuses) {
        this.statuses = statuses;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((("AlertQueryResult"+" [statuses=")+ statuses)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
