
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
 * <p>Original spec-file type: ValidateImageURLParams</p>
 * <pre>
 * Validate image url
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "url",
    "max_size"
})
public class ValidateImageURLParams {

    @JsonProperty("url")
    private String url;
    @JsonProperty("max_size")
    private Long maxSize;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("url")
    public String getUrl() {
        return url;
    }

    @JsonProperty("url")
    public void setUrl(String url) {
        this.url = url;
    }

    public ValidateImageURLParams withUrl(String url) {
        this.url = url;
        return this;
    }

    @JsonProperty("max_size")
    public Long getMaxSize() {
        return maxSize;
    }

    @JsonProperty("max_size")
    public void setMaxSize(Long maxSize) {
        this.maxSize = maxSize;
    }

    public ValidateImageURLParams withMaxSize(Long maxSize) {
        this.maxSize = maxSize;
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
        return ((((((("ValidateImageURLParams"+" [url=")+ url)+", maxSize=")+ maxSize)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
