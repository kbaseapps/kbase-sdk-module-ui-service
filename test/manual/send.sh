#!/bin/bash
curl --insecure -H "Authorization: ${KB_TOKEN}" --data "@${1}.json" https://ci.kbase.us/services/UIServicee 