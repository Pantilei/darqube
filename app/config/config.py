from pydantic import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017/darqube"
    db_name: str = "darqube"
    api_v1: str = "/api/v1"

    jwt_token_expire_minutes: int = 30
    jwt_token_secret: str = "my_super_secret"
    jwt_token_algo: str = "HS256"

    admin_user_first_name: str = "admin"
    admin_user_last_name: str = "admin"
    admin_user_last_password: str = "admin"


settings = Settings()
