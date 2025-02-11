#
# From the python3 standard library:
#
#   argparse: https://docs.python.org/3/library/argparse.html
#   json: https://docs.python.org/3/library/json.html
#   os: https://docs.python.org/3/library/os.html
#   sys: https://docs.python.org/3/library/sys.html
#
# Third-party Open Source:
#
#   requests: https://requests.readthedocs.io/en/latest/user/quickstart/
#
import argparse
import json
import os
import requests
import sys

SEARCH_ENDPOINT = "https://api.nyc.gov/geoclient/v2/search"

def geocode(key, location):
    headers ={ 'Cache-Control': 'no-cache', 'Ocp-Apim-Subscription-Key': key }
    query = { 'input': location }
    try:
        # response from requests lib
        resp = requests.get(SEARCH_ENDPOINT, params=query, headers=headers)
        # JSON object from json standard lib
        json_obj = resp.json()
        print()
        print(json.dumps(json_obj,indent=2))
        print()
    except Exception as e:
        print("ERROR")
        sys.exit(e)


def main():
    parser = argparse.ArgumentParser(description="Calling Geoclient v2 with Python3 demo..")

    # Positional argument (required)
    parser.add_argument("location", type=str, help="Location to geocode. Surround with quotes to escape special characters (e.g., spaces, ampersands, etc.)")

    # Optional arguments
    parser.add_argument("-k", "--key", type=str, help="API key for authentication. Required if -e is not given")
    parser.add_argument("-e", "--envkey", type=str, help="Name of the environment variable containing the API key. Required if -k is not given")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    # Set from required arguments
    subscription_key = None

    # Parse arguments
    args = parser.parse_args()
    print("Verbose mode is ON") if args.verbose else None
    print(f"Location: {args.location}") if args.verbose else None
    if args.key:
        print("Using subscription key provided with -k argument") if args.verbose else None
        subscription_key = args.key
    if args.envkey:
        print(f"Using subscription key from the value of environment variable '{args.envkey}'") if args.verbose else None
        subscription_key = os.environ.get(f"{args.envkey}")
    if not subscription_key:
        print("ERROR: either the -k or the -e argument is required.")
        print("")
        parser.print_help()
    else:
        geocode(subscription_key, args.location)

if __name__ == "__main__":
    main()

