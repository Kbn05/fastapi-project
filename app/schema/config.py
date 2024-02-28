from pydantic_settings import BaseSettings

class Config(BaseSettings):
    DB_HOSTNAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_TIME: int

    class Config:
        env_file = ".env"


setting = Config()