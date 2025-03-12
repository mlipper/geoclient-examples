#!/usr/bin/env bash

#
# This example is the same as the auth-example.sh except it provides
# the subscription key on the HTTP query string instead of an HTTP
# header.
#
# See auth-example.sh for additional information in the comments.
# 

set -eu

GEOCLIENT_URL="${GEOCLIENT_URL:-https://api.nyc.gov/geoclient/v2}"
DEFAULT_LOCATION='2 Metrotech'

location="${DEFAULT_LOCATION}"

if [ $# -gt 0 ]; then
  location="$@"
fi

curl -k -s --get \
     --data-urlencode "input=${location:-${DEFAULT_LOCATION}}" \
     --data-urlencode "key=${GEOCLIENT_KEY}" \
     -H "Cache-Control: no-cache" \
     "${GEOCLIENT_URL}/search"
