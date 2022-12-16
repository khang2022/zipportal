import secrets

import dotenv
from pydantic import BaseSettings

# Load Enviroment Variables
dotenv.load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 60 second = 1 days
    ACCESS_TOKEN_EXPIRE_SECOND: int = 60 * 24 * 60

    ACCOUNT_NAME: str
    ACCOUNT_SHARED_KEY: str
    CONTAINER_NAME: str
    FILE_LIMIT: int
    TIME_LIMIT: int
    ALGORITHM: str
    ACCESS_TOKEN_SECRET: str

    MAX_CONCURRENCY: int
    FILE_SERVICE_BLOB_SIGNED_URL_EXPIRY_TIME: int
    BLOB_STORAGE_HOST: str

    LOG_INFO_FILE: str = "logs/info/infos.log"
    LOG_ERROR_FILE: str = "logs/error/errors.log"
    LOG_CUSTOM_FILE: str = "logs/custom/customs.log"
    LOG_SQL_FILE: str = "logs/sql/sql.log"
    LOG_ROTATION: str = "1 days"
    LOG_RETENTION: str = "20 days"
    LOG_FORMAT: str = (
        "[<level>{level}</level>] | "
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS} </green> | "
        "<cyan>{name}</cyan>:<cyan>{module}</cyan> | "
        "{line} | "
        "<level>{message}</level>"
    )

    LOG_DIAGNOSE: bool = True

    class Config:
        case_sensitive = True


settings = Settings()
