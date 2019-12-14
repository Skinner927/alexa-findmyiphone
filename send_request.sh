#!/bin/bash
# Specify name as first argument: ./sample_request.sh John

payload=$(printf '{"request": { "type": "IntentRequest", "intent": { "slots": { "User": { "name": "User", "value": "%s" } }, "name": "FindIphone" } } }' "${1}")
curl -X POST --header 'Content-type: application/json' --data "$payload" http://127.0.0.1:8080
