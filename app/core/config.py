import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str # tipul trebuie să fie specificat
    class Config:
        env_file = ".env"

settings = Settings()

class HistoryItem(BaseModel):
    ...

    class Config:
        from_attributes = True
