
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
 * <p>Original spec-file type: SearchArg</p>
 * <pre>
 * union type: either field or field_set
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "field",
    "expression"
})
public class SearchArg {

    /**
     * <p>Original spec-file type: SearchField</p>
     * 
     * 
     */
    @JsonProperty("field")
    private SearchField field;
    /**
     * <p>Original spec-file type: SearchSubExpression</p>
     * 
     * 
     */
    @JsonProperty("expression")
    private SearchSubExpression expression;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: SearchField</p>
     * 
     * 
     */
    @JsonProperty("field")
    public SearchField getField() {
        return field;
    }

    /**
     * <p>Original spec-file type: SearchField</p>
     * 
     * 
     */
    @JsonProperty("field")
    public void setField(SearchField field) {
        this.field = field;
    }

    public SearchArg withField(SearchField field) {
        this.field = field;
        return this;
    }

    /**
     * <p>Original spec-file type: SearchSubExpression</p>
     * 
     * 
     */
    @JsonProperty("expression")
    public SearchSubExpression getExpression() {
        return expression;
    }

    /**
     * <p>Original spec-file type: SearchSubExpression</p>
     * 
     * 
     */
    @JsonProperty("expression")
    public void setExpression(SearchSubExpression expression) {
        this.expression = expression;
    }

    public SearchArg withExpression(SearchSubExpression expression) {
        this.expression = expression;
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
        return ((((((("SearchArg"+" [field=")+ field)+", expression=")+ expression)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
