from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "API academica"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = "sqlite:///./cursos.db"
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    allowed_hosts: list[str] = [
        "localhost",
        "127.0.0.1",
        ".onrender.com",
        "testserver",
    ]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
