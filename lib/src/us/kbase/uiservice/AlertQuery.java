
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


/**
 * <p>Original spec-file type: AlertQuery</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "query",
    "page",
    "sorting"
})
public class AlertQuery {

    /**
     * <p>Original spec-file type: SearchExpression</p>
     * <pre>
     * typedef structure {
     *     SearchField field;
     *     SearchSubExpression expression;
     * } SearchArg;
     * </pre>
     * 
     */
    @JsonProperty("query")
    private SearchExpression query;
    /**
     * <p>Original spec-file type: PagingSpec</p>
     * <pre>
     * typedef UnspecifiedObject Query;
     * </pre>
     * 
     */
    @JsonProperty("page")
    private PagingSpec page;
    @JsonProperty("sorting")
    private List<SortSpec> sorting;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: SearchExpression</p>
     * <pre>
     * typedef structure {
     *     SearchField field;
     *     SearchSubExpression expression;
     * } SearchArg;
     * </pre>
     * 
     */
    @JsonProperty("query")
    public SearchExpression getQuery() {
        return query;
    }

    /**
     * <p>Original spec-file type: SearchExpression</p>
     * <pre>
     * typedef structure {
     *     SearchField field;
     *     SearchSubExpression expression;
     * } SearchArg;
     * </pre>
     * 
     */
    @JsonProperty("query")
    public void setQuery(SearchExpression query) {
        this.query = query;
    }

    public AlertQuery withQuery(SearchExpression query) {
        this.query = query;
        return this;
    }

    /**
     * <p>Original spec-file type: PagingSpec</p>
     * <pre>
     * typedef UnspecifiedObject Query;
     * </pre>
     * 
     */
    @JsonProperty("page")
    public PagingSpec getPage() {
        return page;
    }

    /**
     * <p>Original spec-file type: PagingSpec</p>
     * <pre>
     * typedef UnspecifiedObject Query;
     * </pre>
     * 
     */
    @JsonProperty("page")
    public void setPage(PagingSpec page) {
        this.page = page;
    }

    public AlertQuery withPage(PagingSpec page) {
        this.page = page;
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
        return ((((((((("AlertQuery"+" [query=")+ query)+", page=")+ page)+", sorting=")+ sorting)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
