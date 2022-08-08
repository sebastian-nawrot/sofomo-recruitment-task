from pydantic import ValidationError
import pytest

from app.models import Geolocation
from tests.fixtures.geolocation_fixtures import geolocation_data_fixture


def test_geolocation_correct_validation(geolocation_data_fixture):
  geolocation = Geolocation(**geolocation_data_fixture)

def test_geolocation_incorrect_validation():
  with pytest.raises(ValidationError):
    geolocation = Geolocation(**{
      "address": "172.152.31.241"
      # missing required fields
    })