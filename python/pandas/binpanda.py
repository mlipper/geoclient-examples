import pandas as pd
import requests


# Replace with your subscription key
GEOCLIENT_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
GEOCLIENT_URL = 'https://api.nyc.gov/geoclient/v2'

# Sample DataFrame
data = {
    'row_id': range(1,5),
    'bin_input': [
        '1001289',
        '4538327',
        '3002557',
        '5110428'
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

    request_url = requests.Request('GET', url, params=params, headers=headers).prepare().url
    # Print the full request URL for debugging
    print(f"Sending request to: {request_url}")

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()  # Return JSON response
    else:
        return None

# List to store results
results = []

# Iterate over DataFrame rows, send requests, and store the results
for index, row in df.iterrows():
    result = send_request(row['bin_input'])
    bin_json = result.get('bin')
    if bin_json and bin_json['geosupportReturnCode']:
        print(f"Row {row['row_id']} - API request successful.")
        results.append(bin_json)  # Store the response part of the JSON
    else:
        print(f"Row {row['row_id']} - API request failed or no results found.")
        results.append({})  # Store an empty dict if the request fails or no results found

# Convert the list of responses to a DataFrame
response_df = pd.DataFrame(results)

# Add the 'row_id' from the original dataframe to the response_df
response_df['row_id'] = df['row_id']

# Join the original DataFrame with the response DataFrame on 'row_id'
input_geocoded_df = pd.merge(df, response_df, on='row_id', how='left')

# Output the resulting DataFrame
print(input_geocoded_df)
