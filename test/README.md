# Testing

## Setup

### test.cfg

## Running Tests

## Manual Integration Tests
 

```
# common 
test_token=<your kbase token here>
kbase_endpoint=https://ci.kbase.us/services
auth_service_url=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login
auth_service_url_allow_insecure=true

# ui service
secure.mongo_db=ui_service
secure.mongo_host=mongo
secure.mongo_port=27017
secure.mongo_user=ui_service
secure.mongo_pwd=ui_service
```

