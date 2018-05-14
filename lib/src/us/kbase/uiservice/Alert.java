
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
 * <p>Original spec-file type: Alert</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "start_at",
    "end_at",
    "type",
    "title",
    "message",
    "status"
})
public class Alert {

    @JsonProperty("id")
    private Long id;
    @JsonProperty("start_at")
    private Long startAt;
    @JsonProperty("end_at")
    private Long endAt;
    @JsonProperty("type")
    private java.lang.String type;
    @JsonProperty("title")
    private java.lang.String title;
    @JsonProperty("message")
    private List<String> message;
    @JsonProperty("status")
    private java.lang.String status;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("id")
    public Long getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(Long id) {
        this.id = id;
    }

    public Alert withId(Long id) {
        this.id = id;
        return this;
    }

    @JsonProperty("start_at")
    public Long getStartAt() {
        return startAt;
    }

    @JsonProperty("start_at")
    public void setStartAt(Long startAt) {
        this.startAt = startAt;
    }

    public Alert withStartAt(Long startAt) {
        this.startAt = startAt;
        return this;
    }

    @JsonProperty("end_at")
    public Long getEndAt() {
        return endAt;
    }

    @JsonProperty("end_at")
    public void setEndAt(Long endAt) {
        this.endAt = endAt;
    }

    public Alert withEndAt(Long endAt) {
        this.endAt = endAt;
        return this;
    }

    @JsonProperty("type")
    public java.lang.String getType() {
        return type;
    }

    @JsonProperty("type")
    public void setType(java.lang.String type) {
        this.type = type;
    }

    public Alert withType(java.lang.String type) {
        this.type = type;
        return this;
    }

    @JsonProperty("title")
    public java.lang.String getTitle() {
        return title;
    }

    @JsonProperty("title")
    public void setTitle(java.lang.String title) {
        this.title = title;
    }

    public Alert withTitle(java.lang.String title) {
        this.title = title;
        return this;
    }

    @JsonProperty("message")
    public List<String> getMessage() {
        return message;
    }

    @JsonProperty("message")
    public void setMessage(List<String> message) {
        this.message = message;
    }

    public Alert withMessage(List<String> message) {
        this.message = message;
        return this;
    }

    @JsonProperty("status")
    public java.lang.String getStatus() {
        return status;
    }

    @JsonProperty("status")
    public void setStatus(java.lang.String status) {
        this.status = status;
    }

    public Alert withStatus(java.lang.String status) {
        this.status = status;
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
        return ((((((((((((((((("Alert"+" [id=")+ id)+", startAt=")+ startAt)+", endAt=")+ endAt)+", type=")+ type)+", title=")+ title)+", message=")+ message)+", status=")+ status)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
