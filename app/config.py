import os
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings
from functools import lru_cache

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"

class Settings(BaseSettings):
    astradb_keyspace: str = Field(..., env='ASTRADB_KEYSPACE')
    astra_client_id: str = Field(..., env='ASTRA_CLIENT_ID')
    astra_client_secret: str = Field(..., env='ASTRA_CLIENT_SECRET')


    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    try:
        return Settings()
    except ValidationError as e:
        # Handle the validation error, e.g., provide default values
        print(f"Validation error: {e}")
        return Settings(keyspace='default_value')