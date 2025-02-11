#
# For more info on module usage see:
#
# requests:
# https://requests.readthedocs.io/en/latest/user/quickstart/
#
# json:
# https://docs.python.org/3/library/json.html
#
import json
import requests

try:
    query = {
        'houseNumber': '2820',
        'street': 'broadway',
        'zip': '10025'
    }

    header ={
        'Cache-Control': 'no-cache',
        # Replace with your subscription key
        'Ocp-Apim-Subscription-Key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
    # response from requests lib
    resp = requests.get("https://api.nyc.gov/geoclient/v2/address", params=query, headers=header)
    # JSON object from json standard lib
    json_obj = resp.json()

    print()
    print('----------------------')
    print(f"HTTP status code: {resp.status_code}")
    print('----------------------')
    print()
    print('---------------------')
    print("JSON response object:")
    print('---------------------')
    print(json_obj)
    print()
    print('--------------------------------------')
    print("Pretty print JSON response as a string:")
    print('--------------------------------------')
    print(json.dumps(json_obj,indent=2))
    print()
    if resp.status_code == 200:
        addr = json_obj.get('address')
        print()
        print("---------------------------------------------------------")
        print("Geosupport Function 1E (range-based address) call status:")
        print("---------------------------------------------------------")
        print(f"return code: {addr.get('geosupportReturnCode')}")
        print(f"    message: {addr.get('message')}")
        print()
        print("-----------------------------------------------------------")
        print("Geosupport Function 1A (real property address) call status:")
        print("-----------------------------------------------------------")
        print(f"return code: {addr.get('geosupportReturnCode2')}")
        print(f"    message: {addr.get('message2')}")
        print()
        print("-----------------------------")
        print("<Drum roll>....and finally...")
        print("-----------------------------")
        print(f"BBL: {addr.get('bbl')}")
        print()
except Exception as e:
    print(e)


