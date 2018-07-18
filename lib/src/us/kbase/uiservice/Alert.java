
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
    "status",
    "created_at",
    "created_by",
    "updated_at",
    "updated_by"
})
public class Alert {

    @JsonProperty("id")
    private String id;
    @JsonProperty("start_at")
    private Long startAt;
    @JsonProperty("end_at")
    private Long endAt;
    @JsonProperty("type")
    private String type;
    @JsonProperty("title")
    private String title;
    @JsonProperty("message")
    private String message;
    @JsonProperty("status")
    private String status;
    @JsonProperty("created_at")
    private Long createdAt;
    @JsonProperty("created_by")
    private String createdBy;
    @JsonProperty("updated_at")
    private Long updatedAt;
    @JsonProperty("updated_by")
    private String updatedBy;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public Alert withId(String id) {
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
    public String getType() {
        return type;
    }

    @JsonProperty("type")
    public void setType(String type) {
        this.type = type;
    }

    public Alert withType(String type) {
        this.type = type;
        return this;
    }

    @JsonProperty("title")
    public String getTitle() {
        return title;
    }

    @JsonProperty("title")
    public void setTitle(String title) {
        this.title = title;
    }

    public Alert withTitle(String title) {
        this.title = title;
        return this;
    }

    @JsonProperty("message")
    public String getMessage() {
        return message;
    }

    @JsonProperty("message")
    public void setMessage(String message) {
        this.message = message;
    }

    public Alert withMessage(String message) {
        this.message = message;
        return this;
    }

    @JsonProperty("status")
    public String getStatus() {
        return status;
    }

    @JsonProperty("status")
    public void setStatus(String status) {
        this.status = status;
    }

    public Alert withStatus(String status) {
        this.status = status;
        return this;
    }

    @JsonProperty("created_at")
    public Long getCreatedAt() {
        return createdAt;
    }

    @JsonProperty("created_at")
    public void setCreatedAt(Long createdAt) {
        this.createdAt = createdAt;
    }

    public Alert withCreatedAt(Long createdAt) {
        this.createdAt = createdAt;
        return this;
    }

    @JsonProperty("created_by")
    public String getCreatedBy() {
        return createdBy;
    }

    @JsonProperty("created_by")
    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public Alert withCreatedBy(String createdBy) {
        this.createdBy = createdBy;
        return this;
    }

    @JsonProperty("updated_at")
    public Long getUpdatedAt() {
        return updatedAt;
    }

    @JsonProperty("updated_at")
    public void setUpdatedAt(Long updatedAt) {
        this.updatedAt = updatedAt;
    }

    public Alert withUpdatedAt(Long updatedAt) {
        this.updatedAt = updatedAt;
        return this;
    }

    @JsonProperty("updated_by")
    public String getUpdatedBy() {
        return updatedBy;
    }

    @JsonProperty("updated_by")
    public void setUpdatedBy(String updatedBy) {
        this.updatedBy = updatedBy;
    }

    public Alert withUpdatedBy(String updatedBy) {
        this.updatedBy = updatedBy;
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
        return ((((((((((((((((((((((((("Alert"+" [id=")+ id)+", startAt=")+ startAt)+", endAt=")+ endAt)+", type=")+ type)+", title=")+ title)+", message=")+ message)+", status=")+ status)+", createdAt=")+ createdAt)+", createdBy=")+ createdBy)+", updatedAt=")+ updatedAt)+", updatedBy=")+ updatedBy)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
