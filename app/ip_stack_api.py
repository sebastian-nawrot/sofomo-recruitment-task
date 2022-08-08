from pydantic import ValidationError
import requests
import logging

from app.config import settings
from app.models import Geolocation


def fetch_geolocation(address: str) -> Geolocation | None:
  url = f"http://api.ipstack.com/{address}?access_key={settings.ip_stack_access_key}"
  response = requests.get(url)
  if response.status_code != requests.codes.ok:
    logging.error(f"api.ipstack.com error, invalid response status code: {response.status_code}")
    return None

  data = response.json()
  if not data or data.get("success") == False:
    logging.error(f"api.ipstack.com error, invalid response data: {data}")
    return None

  try:
    geolocation = Geolocation(address=address, **data)
  except ValidationError as error:
    logging.error(f"geolocation validation error: {error.errors()}")
    return None

  return geolocation
