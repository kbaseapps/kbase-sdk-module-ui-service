
package us.kbase.uiservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: CheckError</p>
 * <pre>
 * Validations
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "code",
    "info"
})
public class CheckError {

    @JsonProperty("code")
    private String code;
    @JsonProperty("info")
    private UObject info;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("code")
    public String getCode() {
        return code;
    }

    @JsonProperty("code")
    public void setCode(String code) {
        this.code = code;
    }

    public CheckError withCode(String code) {
        this.code = code;
        return this;
    }

    @JsonProperty("info")
    public UObject getInfo() {
        return info;
    }

    @JsonProperty("info")
    public void setInfo(UObject info) {
        this.info = info;
    }

    public CheckError withInfo(UObject info) {
        this.info = info;
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
        return ((((((("CheckError"+" [code=")+ code)+", info=")+ info)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
