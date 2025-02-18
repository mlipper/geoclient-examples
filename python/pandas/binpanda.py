import pandas as pd
import requests
import os

#
# The original version of this file was written by Edgar Alfonseca.
#
# This version has been modified to account for the release of Geoclient v2
# on NYC API Developer's Portal (https://api-portal.nyc.gov/). In addition to
# a new endpoint URL, this script provides authentication using an HTTP header
# instead of the query string.
#
# Different data is used to account for changes in the data returned by Geoclient.
# Usage of the Geoclient API itself has not changed between v1 and v2.
#

# Replace with your subscription key
GEOCLIENT_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
GEOCLIENT_URL = 'https://api.nyc.gov/geoclient/v2'

# Sample DataFrame
data = {
    'row_id': range(1,3),
    'bin_input': [
        '4538327',
        '3255603'
    ]
}

df = pd.DataFrame(data)

### Geoclient API 'bin' endpoint/function

# API details
url = f"{GEOCLIENT_URL}/bin" # bin endpoint request

# Function to send API request and return JSON response
def send_request(bin_input):
    headers = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': GEOCLIENT_KEY
    }
    params = {'bin': bin_input}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()  # Return JSON response
    else:
        return None

if GEOCLIENT_KEY == 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':
    GEOCLIENT_KEY = os.getenv('GEOCLIENT_KEY')
    if GEOCLIENT_KEY is None:
        raise Exception("GEOCLIENT_KEY is still set to the default and an environment variable of the same name has not been set.")

# List to store results
results = []

# Iterate over DataFrame rows, send requests, and store the results
for index, row in df.iterrows():
    result = send_request(row['bin_input'])
    bin_json = result.get('bin')
    if bin_json and bin_json['geosupportReturnCode']:
        #print(f"Row {row['row_id']} - API request successful.")
        results.append(bin_json)  # Store the response part of the JSON
    else:
        #print(f"Row {row['row_id']} - API request failed or no results found.")
        results.append({})  # Store an empty dict if the request fails or no results found


# Convert the list of responses to a DataFrame
response_df = pd.DataFrame(results)

# Add the 'row_id' from the original dataframe to the response_df
response_df['row_id'] = df['row_id']

# Join the original DataFrame with the response DataFrame on 'row_id'
input_geocoded_df = pd.merge(df, response_df, on='row_id', how='left')

# Output the resulting DataFrame
print(input_geocoded_df)

