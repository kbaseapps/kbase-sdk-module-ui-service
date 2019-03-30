
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
 * <p>Original spec-file type: CheckImageURLResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "is_valid",
    "error"
})
public class CheckImageURLResult {

    @JsonProperty("is_valid")
    private Long isValid;
    /**
     * <p>Original spec-file type: CheckError</p>
     * 
     * 
     */
    @JsonProperty("error")
    private CheckError error;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("is_valid")
    public Long getIsValid() {
        return isValid;
    }

    @JsonProperty("is_valid")
    public void setIsValid(Long isValid) {
        this.isValid = isValid;
    }

    public CheckImageURLResult withIsValid(Long isValid) {
        this.isValid = isValid;
        return this;
    }

    /**
     * <p>Original spec-file type: CheckError</p>
     * 
     * 
     */
    @JsonProperty("error")
    public CheckError getError() {
        return error;
    }

    /**
     * <p>Original spec-file type: CheckError</p>
     * 
     * 
     */
    @JsonProperty("error")
    public void setError(CheckError error) {
        this.error = error;
    }

    public CheckImageURLResult withError(CheckError error) {
        this.error = error;
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
        return ((((((("CheckImageURLResult"+" [isValid=")+ isValid)+", error=")+ error)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
