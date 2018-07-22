
package us.kbase.uiservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: AlertQuery</p>
 * <pre>
 * typedef structure {
 *     string path;        
 *     string op; 
 *     string value;
 * } SearchField;
 * typedef structure {
 *     string op;
 *     list<SearchField> args;
 * } SearchSubExpression;
 * typedef structure {
 *     SearchField field;
 *     SearchSubExpression expression;
 * } SearchArg;
 * typedef structure {
 *     string op;
 *     list<SearchArg> args;
 * } SearchExpression;
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "query",
    "paging",
    "sorting"
})
public class AlertQuery {

    @JsonProperty("query")
    private UObject query;
    /**
     * <p>Original spec-file type: PagingSpec</p>
     * <pre>
     * search_alerts
     * </pre>
     * 
     */
    @JsonProperty("paging")
    private PagingSpec paging;
    @JsonProperty("sorting")
    private List<SortSpec> sorting;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("query")
    public UObject getQuery() {
        return query;
    }

    @JsonProperty("query")
    public void setQuery(UObject query) {
        this.query = query;
    }

    public AlertQuery withQuery(UObject query) {
        this.query = query;
        return this;
    }

    /**
     * <p>Original spec-file type: PagingSpec</p>
     * <pre>
     * search_alerts
     * </pre>
     * 
     */
    @JsonProperty("paging")
    public PagingSpec getPaging() {
        return paging;
    }

    /**
     * <p>Original spec-file type: PagingSpec</p>
     * <pre>
     * search_alerts
     * </pre>
     * 
     */
    @JsonProperty("paging")
    public void setPaging(PagingSpec paging) {
        this.paging = paging;
    }

    public AlertQuery withPaging(PagingSpec paging) {
        this.paging = paging;
        return this;
    }

    @JsonProperty("sorting")
    public List<SortSpec> getSorting() {
        return sorting;
    }

    @JsonProperty("sorting")
    public void setSorting(List<SortSpec> sorting) {
        this.sorting = sorting;
    }

    public AlertQuery withSorting(List<SortSpec> sorting) {
        this.sorting = sorting;
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
        return ((((((((("AlertQuery"+" [query=")+ query)+", paging=")+ paging)+", sorting=")+ sorting)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
