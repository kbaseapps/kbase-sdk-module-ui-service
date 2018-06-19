#!/bin/bash
curl --insecure -H "Authorization: ${KB_TOKEN}" --data "@${1}.json" https://ci.kbase.us/services/UIService 
# curl --insecure -H "Authorization: ${KB_TOKEN}" --data "@${1}.json" https://ci.kbase.us/dynserv/030e6dc9f298be637b6763a334612455a15c5b8f.UIService