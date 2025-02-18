#!/usr/bin/env bash

#
# This example shows how to call Geoclient's /search resource from a
# bash script using the curl command.
#
# This script accepts a single location argument which will be used for the
# search. If no argument is passed, a default location is used instead.
#
# IMPORTANT: In order for this script to work, you must have a valid
# API key! See below for info on how to get one.
#
# USAGE: <path_to_this_dir>/auth-example.sh [location]
#
# 1. Configure your access key using one of the following methods:
#    a. Set an environment variable named GEOCLIENT_KEY with your key:
#       export GEOCLIENT_KEY=your_key
#    or
#    b. Edit this script and replace the text ${GEOCLIENT_KEY} with ${your_key}
#
# 2. Open a terminal and navigate to the directory this script is in.
#
# 3. Run the script
#    # Use the default location:
#    ./auth-example.sh
#    # Pass a location argument:
#    ./auth-example.sh 'w 42 St and 6 avenue'
#
# HOW TO GET AN API KEY:
# If you do not have a key, you can get one by creating an account on
# the NYC API Developers Portal:
# https://api-portal.nyc.gov/signup
#
# Once you've logged in with your account, subscribe to the Geoclient v2 
# service to receive an API key:
# https://api-portal.nyc.gov/product#product=geoclient-user
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
     -H "Cache-Control: no-cache" \
     -H "Ocp-Apim-Subscription-Key: ${GEOCLIENT_KEY}" \
     "${GEOCLIENT_URL}/search"
