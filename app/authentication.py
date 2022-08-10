
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from jwt import encode, decode, PyJWTError
from starlette import status

from app.config import settings


def generate_access_token():
  expiration = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
  encoded_jwt = encode({ "expiration": expiration.isoformat()}, settings.access_token_secret)
  return encoded_jwt


def verify_access_token(access_token = Header()):
  try:
    payload = decode(access_token, settings.access_token_secret, ["HS256"])
  except PyJWTError:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED,
      detail="Invalid access token")
