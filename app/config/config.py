from pydantic import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017/darqube"
    db_name: str = "darqube"
    api_v1: str = "/api/v1"

    token_expire_minutes: int = 30


settings = Settings()
