import datetime
import json
import petl as etl
import requests
import sys
from dataclasses import asdict, astuple, dataclass


# Replace with your subscription key
GEOCLIENT_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
GEOCLIENT_URL = 'https://api.nyc.gov/geoclient/v2'

ATTRIBUTES = [("buildingIdentificationNumber", "bin"),
              ("censusTract2010", "census_tract"),
              ("cityCouncilDistrict", "city_council_district"),
              ("firstBoroughName", "borough"),
              ("firstStreetNameNormalized", "street"),
              ("geosupportReturnCode", "return_code_1"),
              ("geosupportReturnCode2", "return_code_2"),
              ("houseNumber", "house_number"),
              ("interimAssistanceEligibilityIndicator", "eligibility"),
              ("latitude", "latitude"),
              ("longitude", "longitude"),
              ("message", "message_1"),
              ("message2", "message_2")]

CSV = 'omb-data.csv'

LIMIT = 0

OUT_CSV = 'omb-results.csv'

OUT_CSV_HEADER = ('building_id',
                  'return_code_1',
                  'message_1',
                  'return_code_2',
                  'message_2',
                  'house_number',
                  'street',
                  'borough',
                  'bin',
                  'latitude',
                  'longitude',
                  'census_tract',
                  'city_council_district',
                  'eligibility')

TIMESTAMP_FMT = "%Y%m%d%H%M%S"

@dataclass
class Building:
    building_id: str = None
    borough: str = None
    house_number: str = None
    street: str = None


@dataclass
class Address:
    building_id: str
    return_code_1: str
    message_1: str
    return_code_2: str
    message_2: str
    house_number: str
    street: str
    borough: str
    bin: str
    latitude: float
    longitude: float
    census_tract: str
    city_council_district: str
    eligibility: str


def geocode(uri, endpoint, query):
    headers = { 'Cache-Control': 'no-cache', 'Ocp-Apim-Subscription-Key': GEOCLIENT_KEY }
    payload = { **query }
    url = f'{uri}/{endpoint}'
    return requests.get(url, params=payload, headers=headers, verify=True)


def getargs(argv, default_file, default_uri, default_outfile):
    file = default_file
    if len(argv[1:]) > 0:
        file = argv[1]
    uri = default_uri
    if len(argv[1:]) > 1:
        uri = argv[2]
    ts = datetime.datetime.now()
    outfile = ts.strftime(TIMESTAMP_FMT) + '_' + default_outfile
    if len(argv[1:]) > 2:
        outfile = argv[3]
    return (file, uri, outfile)


def getdata(file):
    return list(etl.fromcsv(file))


def omb_attrs(building_id, resp):
    j = resp.json()
    results = j['address']
    data = dict()
    data['building_id'] = building_id
    for i in range(len(ATTRIBUTES)):
        attribute = ATTRIBUTES[i][0]
        field_name = ATTRIBUTES[i][1]
        if attribute in ['latitude', 'longitude']:
            data[field_name] = float(results.get(attribute, 0.0))
        else:
            data[field_name] = results.get(attribute, "")
    return data


if __name__ == '__main__':
    file, uri, outfile = getargs(sys.argv, CSV, GEOCLIENT_URL, OUT_CSV)
    print(f'Loading text data from file {file}.')
    print(f'Using base URI {uri}.')
    rows = getdata(file)
    table = [OUT_CSV_HEADER]
    etl.tocsv(table, outfile, encoding='ascii', write_header=True, lineterminator='\n')
    for idx, row in enumerate(rows):
        if idx == 0:
            continue
        b = Building(row[0], row[1], row[2], row[3])
        resp = geocode(uri, 'address', {'houseNumber': b.house_number, 'street': b.street, 'borough': b.borough})
        data = omb_attrs(b.building_id, resp)
        address = Address(**data)
        table.append(astuple(address))
        if idx % 10 == 0:
            etl.appendcsv(table, outfile, encoding='ascii', lineterminator='\n')
            table = [OUT_CSV_HEADER]
            print(f'Processed {idx} rows...')
        if idx == LIMIT:
            break
    print(f'Done. {idx} rows processed.')
    print()
