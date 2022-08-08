from pydantic import BaseModel


class GeolocationBase(BaseModel):
  address: str


class Geolocation(GeolocationBase):
  continent_name: str
  country_name: str
  region_name: str
  city: str
  zip: str
  latitude: float
  longitude: float
