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


If get

```

Error while testing module: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target

```

this means you are using a local proxy for ci.kbase.us; just disable it in /etc/hosts

Need to fix this
```
