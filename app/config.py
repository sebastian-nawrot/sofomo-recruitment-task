import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
  mongo_username: str
  mongo_password: str
  mongo_host: str
  ip_stack_access_key: str
  access_token_secret: str = secrets.token_hex(32)
  access_token_expire_minutes: int = 60


settings = Settings()
