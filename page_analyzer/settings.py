from pydantic import BaseSettings, PostgresDsn, Field


class PostgresSettings(BaseSettings):
    scheme: str = Field(env='SCHEME_DB')
    user: str = Field(env='USER_DB')
    password: str = Field(env='PASS_DB')
    host: str = Field(env='HOST_DB')
    port: str = Field(env='PORT_DB')
    path: str = Field(env='NAME_DB')

    class Config:
        env_file = 'page_analyzer/.env'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    postgres_settings = PostgresSettings()

    postgres_dsn: PostgresDsn = PostgresDsn.build(**postgres_settings.dict())


settings = Settings()
