from sqlalchemy import URL
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
      env_file=".env", 
      env_prefix="DB_",
      env_file_encoding="utf-8", 
      extra="ignore"
  )
  HOST: str
  PORT: int
  NAME: str
  USER: str
  PASSWORD: str
  DRIVER: str

  @property
  def database_url(self) -> URL:
    return URL.create(
      drivername=self.DRIVER,
      username=self.USER,
      password=self.PASSWORD,
      host=self.HOST,
      port=self.PORT,
      database=self.NAME
    )

settings = Settings()