from typing import Any
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class EnvConfigSettings(BaseSettings):
    """
        Settings for the app. Reads from environment variables.
    """
    DEBUG: bool
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str
    REFRESH_KEY: str
    PROFILING: bool = False
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # 3 days
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # MySQL
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_DATABASE_URI: str | None
    MYSQL_SSL: str

    @validator('MYSQL_DATABASE_URI', pre=True)
    def assemble_mysql_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return (f"mysql+pymysql://{values.get('MYSQL_USER')}:{values.get('MYSQL_PASSWORD')}"
                f"@{values.get('MYSQL_HOST')}/{values.get('MYSQL_DATABASE')}")

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = EnvConfigSettings()  # type: ignore
