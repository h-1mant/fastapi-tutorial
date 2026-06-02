from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Postgres 
    conn_string: str

    # OAuth2
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 200
    