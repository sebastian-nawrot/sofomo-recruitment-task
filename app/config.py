from pydantic import BaseSettings


class Settings(BaseSettings):
  mongo_username: str
  mongo_password: str
  mongo_host: str
  ip_stack_access_key: str


settings = Settings()
