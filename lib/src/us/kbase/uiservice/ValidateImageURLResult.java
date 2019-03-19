
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
 * <p>Original spec-file type: ValidateImageURLResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "is_valid",
    "result_code",
    "size"
})
public class ValidateImageURLResult {

    @JsonProperty("is_valid")
    private Long isValid;
    @JsonProperty("result_code")
    private Long resultCode;
    @JsonProperty("size")
    private Long size;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("is_valid")
    public Long getIsValid() {
        return isValid;
    }

    @JsonProperty("is_valid")
    public void setIsValid(Long isValid) {
        this.isValid = isValid;
    }

    public ValidateImageURLResult withIsValid(Long isValid) {
        this.isValid = isValid;
        return this;
    }

    @JsonProperty("result_code")
    public Long getResultCode() {
        return resultCode;
    }

    @JsonProperty("result_code")
    public void setResultCode(Long resultCode) {
        this.resultCode = resultCode;
    }

    public ValidateImageURLResult withResultCode(Long resultCode) {
        this.resultCode = resultCode;
        return this;
    }

    @JsonProperty("size")
    public Long getSize() {
        return size;
    }

    @JsonProperty("size")
    public void setSize(Long size) {
        this.size = size;
    }

    public ValidateImageURLResult withSize(Long size) {
        this.size = size;
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
        return ((((((((("ValidateImageURLResult"+" [isValid=")+ isValid)+", resultCode=")+ resultCode)+", size=")+ size)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
