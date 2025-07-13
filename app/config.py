# from pydantic_settings import BaseSettings, SettingsConfigDict
# from functools import lru_cache

# class Settings(BaseSettings):
#     PROJECT_NAME: str
#     MONGO_URI: str
#     MONGO_DB_NAME: str
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int

#     model_config = SettingsConfigDict(
#         env_file="users_service/.env", # Ruta desde la raíz del proyecto
#         env_file_encoding='utf-8'
#     )

# @lru_cache()
# def get_settings():
#     return Settings()

# settings = get_settings()


from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str
    MONGO_URI: str
    MONGO_DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",  # Ruta relativa desde users_service
        env_file_encoding="utf-8"
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
