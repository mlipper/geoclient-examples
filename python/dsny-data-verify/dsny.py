import json
import petl as etl
import requests
import sys
from dataclasses import asdict, dataclass


# Replace with your subscription key
GEOCLIENT_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
GEOCLIENT_URL = 'https://api.nyc.gov/geoclient/v2'

ATTRIBUTES = [("sanitationBulkPickupSchedule", "bulk"),
              ("sanitationCollectionSchedulingSectionAndSubsection", "subsection"),
              ("sanitationDistrict", "district"),
              ("sanitationOrganicsCollectionSchedule", "organics"),
              ("sanitationRecyclingCollectionSchedule", "recycling"),
              ("sanitationRegularCollectionSchedule", "refuse")]

CSV = 'dsny-data.csv'

class StatusText:

    BLD = '1'
    REG = '0'
    GRN = '32'
    RED = '31'
    WHT = '37'
    YLW = '33'

    def ansi(self, effect, color, msg):
        return f'\033[{effect};{color}m{msg}\033[0;00m'

    def testtxt(self, msg):
        return self.ansi(self.REG, self.YLW, msg)

    def testpassed(self):
        return f'[{self.ansi(self.REG, self.GRN, "PASSED")}]'

    def testfail(self):
        return f'[{self.ansi(self.BLD, self.RED, "FAILED")}]'

    def testfailed(self):
        return f'[{self.ansi(self.REG, self.RED, "FAILED")}]'

    def teststatus(self, idx, failures):
        txt = self.testtxt(f'Completed {idx} tests:')
        numpass = idx - failures
        if numpass > 0:
            txt = f'{txt} {self.testpassed()} {self.ansi(self.BLD, self.WHT, numpass)}'
        if failures > 0:
            txt = f'{txt} {self.testfailed()} {self.ansi(self.BLD, self.WHT, failures)}'
        return txt


@dataclass
class Schedule:
    address: str = None
    district: str = None
    subsection: str = None
    refuse: str = None
    recycling: str = None
    organics: str = None
    bulk: str = None


@dataclass
class TestResult:
    rownum: int = 0
    address: str = None
    verified: bool = False
    message: str = None


def testdata(file):
    return list(etl.fromcsv(file))


def geocode(uri, endpoint, query):
    headers ={ 'Cache-Control': 'no-cache', 'Ocp-Apim-Subscription-Key': GEOCLIENT_KEY }
    payload = { **query }
    url = f'{uri}/{endpoint}'
    return requests.get(url, params=payload, headers=headers, verify=True)


def dsny_attrs(resp):
    j = resp.json()
    results = j['results']
    first_result = results[0]
    first_resp = first_result['response']
    data = dict()
    json_attrs = [a for a, _ in ATTRIBUTES]
    for attribute in json_attrs:
        data[attribute] = first_resp.get(attribute, "")
    return data


def verify(rownum, sched, resp):
    msg = ''
    verified = True
    for a, f in ATTRIBUTES:
        s = asdict(sched)
        expected = s[f]
        actual = resp[a]
        if expected == actual:
            verified = verified and True
        else:
            verified = verified and False
            msg = msg + f'expected {f}=="{expected}" actual=="{actual}" '
    return TestResult(rownum, sched.address, verified, msg.strip())


def getargs(argv, default_file, default_uri):
    file = default_file
    if len(argv[1:]) > 0:
        file = argv[1]
    uri = default_uri
    if len(argv[1:]) > 1:
        uri = argv[2]
    return (file, uri)
#
# To supress urllib3 certificate warnings, run with 'python -Wignore ...'
# For details, see:
#   https://urllib3.readthedocs.io/en/stable/advanced-usage.html#certificate-validation-and-macos
#   https://docs.python.org/3/using/cmdline.html#cmdoption-w
#
if __name__ == '__main__':
    file, uri = getargs(sys.argv, CSV, GEOCLIENT_URL)
    print(f'Loading text data from file {file}.')
    print(f'Using base URI {uri}.')
    rows = testdata(file)
    failures = 0
    status = StatusText()
    for idx, row in enumerate(rows):
        if idx == 0:
            continue
        s = Schedule(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        resp = geocode(uri, 'search', {'input': s.address})
        data = dsny_attrs(resp)
        test_result = verify(idx, s, data)
        if test_result.verified:
            pass
        else:
            failures = failures + 1
            print(f'{status.testfail()} test {test_result.rownum}: "{test_result.address}" -> {test_result.message}')
        if idx % 10 == 0:
            print(status.teststatus(idx, failures))
    print(f'{status.testtxt("Completed test suite.")}')
    print()
    print(f'>> {status.testtxt("Test Results:")}')
    print(f'>> {status.teststatus(idx, failures)}')
    print()
