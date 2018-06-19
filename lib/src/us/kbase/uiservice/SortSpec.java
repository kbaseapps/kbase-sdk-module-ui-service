
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
 * <p>Original spec-file type: SortSpec</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "field",
    "is_descending"
})
public class SortSpec {

    @JsonProperty("field")
    private String field;
    @JsonProperty("is_descending")
    private Long isDescending;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("field")
    public String getField() {
        return field;
    }

    @JsonProperty("field")
    public void setField(String field) {
        this.field = field;
    }

    public SortSpec withField(String field) {
        this.field = field;
        return this;
    }

    @JsonProperty("is_descending")
    public Long getIsDescending() {
        return isDescending;
    }

    @JsonProperty("is_descending")
    public void setIsDescending(Long isDescending) {
        this.isDescending = isDescending;
    }

    public SortSpec withIsDescending(Long isDescending) {
        this.isDescending = isDescending;
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
        return ((((((("SortSpec"+" [field=")+ field)+", isDescending=")+ isDescending)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
