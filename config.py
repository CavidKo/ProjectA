from decouple import config

class Settings:
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
    POSTGRES_USER = config("POSTGRES_USER=")
    POSTGRES_DB = config("POSTGRES_DB")

settings = Settings()