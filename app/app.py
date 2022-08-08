from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.errors import PyMongoError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
import logging


from app.database import client
from app.ip_stack_api import fetch_geolocation
from app.models import GeolocationBase, Geolocation


logging.basicConfig(
  level=logging.INFO, 
  format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
  datefmt='%H:%M:%S'
)


app = FastAPI()
collection = client.database.geolocation


@app.on_event("startup")
def startup_event():
  # Try database connection
  try:
    client.admin.command("ping")
  except Exception:
    raise RuntimeError("Unable to connect to the database")


@app.exception_handler(PyMongoError)
async def database_exception_handler(request: Request, exception: PyMongoError):
  logging.error(f"database error: {exception}")
  return JSONResponse(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content={ "detail": "The server encountered an internal error" }
  )


@app.get("/geolocation/{address}")
def geolocation_get(address: str):
  """ Returns geolocation data stored in our Mongo database

  HTTP response status codes:
    200 - OK
    404 - Resource not found
    500 - Internal server error
  """
  result = collection.find_one({ "address": address})
  if result is None:
    raise HTTPException(status.HTTP_404_NOT_FOUND,
      detail=f"Couldn't find geolocation with given address: '{address}'")
  return Geolocation(**result)


@app.delete("/geolocation/{address}")
def geolocation_delete(address: str):
  """ Deletes geolocation data stored in database

  HTTP response status codes:
    204 - No content
    404 - Resource not found
    500 - Internal server error
  """
  result = collection.delete_one({ "address": address})
  if result.deleted_count == 0:
    raise HTTPException(status.HTTP_404_NOT_FOUND,
      detail=f"Couldn't find geolocation with given address: '{address}'")
  return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/geolocation", response_model=Geolocation)
def geolocation_post(base: GeolocationBase):
  """ Creates new geolocation based on address passed in payload, it utilizes
  ipstack.com API.

  HTTP response status codes:
    201 - Created
    500 - Internal server error
  """
  address = base.address

  geolocation = fetch_geolocation(address)
  if geolocation is None:
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"The server encountered an internal error")

  # Insert or update geolocation
  data = jsonable_encoder(geolocation)
  collection.update_one({ "address": address }, { "$set": data }, upsert=True)
  return JSONResponse(data, status.HTTP_201_CREATED)
