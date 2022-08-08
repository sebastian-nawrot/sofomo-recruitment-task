import pytest


@pytest.fixture
def geolocation_data_fixture():
  return {
    "address": "172.152.31.241",
    "continent_name": "North America",
    "country_name": "United States",
    "region_name": "California",
    "city": "Los Angeles",
    "zip": "90012",
    "latitude": 34.0655517578125,
    "longitude": -118.24053955078125
  }
