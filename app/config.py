from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Reads configuration from environment variables / the .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 5
    db_echo: bool = False


settings = Settings()