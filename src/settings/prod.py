from pydantic_settings import SettingsConfigDict

from src.settings.base import AppBaseSettings

class ProdAppSettings(AppBaseSettings):
    model_config = SettingsConfigDict(env_file="src/settings/env/.env.prod")
