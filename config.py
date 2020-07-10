from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    LINE_CHANNEL_ACCESS_TOKEN: str
    LINE_CHANNEL_SECRET: str

    class Config:
        env_file = '.env'


settings = Settings()
