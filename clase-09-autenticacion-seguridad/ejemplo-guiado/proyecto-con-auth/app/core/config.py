from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"
    secret_key: str = "supersecretkey1234567890"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
