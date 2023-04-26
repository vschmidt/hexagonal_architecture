from pydantic import BaseSettings, Field


class Environment(BaseSettings):
    DATABASE_CONNECTION_STRING: str = Field(
        "postgresql+psycopg2://postgres:postgres@postgres/postgres",
        env="DATABASE_CONNECTION_STRING",
    )
    SECRET_KEY: str = Field(
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        env="SECRET_KEY",
    )
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    AUTO_APPROVED_CPFS: list = Field(["15350946056"], env="AUTO_APPROVED_CPFS")
