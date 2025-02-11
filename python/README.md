# Geoclient Python Examples

**WARNING:** The samples in this directory may not work! They are copied from various micro projects written for older Python and Geoclient versions. They will be fixed soon...

## Usage

```python

pip3 install petl
...

python3 <file>.py

```

If python3/pip3 has been aliased to python/pip, then this will also work:

```python

pip install petl
...
python <file>.py

```

## Assumptions

* Python 3.10 or greater (3.8, 3.9 will probably work).
* The `petl` library has been installed (`pip3 install petl`).
* The `*.py` files are in the same directory as the `*.csv` files.

Only applies to the DSNY example:

* The code is run from a terminal that supports 8-bit ANSI color codes. It
  has been tested with `sh` and `bash`, but `cmd.exe` should work.

## OMB Building Geocoder

This example demonstrates geocoding addresses assembled from multiple columns
and writing results to an output file. Both input (UTF-8 encoded, exported by
Excel) and output (ASCII) files are in `CSV` format.

The code also shows how to preserve row identifiers from the input data so
that the geocoded attributes in output rows can be correlated with input data.

## DSNY Data Verification

This code was originally written to verify that a particular DCP Geosupport
release was using updated DSNY district values for certain locations.

At this time, some of those values have changed so it is **expected** that
some tests will fail.

## NYC Developer Portal

This example demonstrates using the popular python `requests` project and
`json` built-in module to call `geoclient v1` through NYC Developer Portal's
API Gateway.
