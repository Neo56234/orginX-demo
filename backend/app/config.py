from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    environment: str = "development"
    data_dir: str = "/data"

    # Database
    database_url: str = "postgresql://originx:dev@localhost:5432/originx"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # AI APIs
    anthropic_api_key: str = ""
    groq_api_key: str = ""
    youtube_api_key: str = ""
    invid_api_key: str = ""

    # Maps
    mapbox_token: str = ""

    # Twilio (WhatsApp bot)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_from: str = ""

    @property
    def videos_dir(self) -> str:
        return f"{self.data_dir}/videos"

    @property
    def frames_dir(self) -> str:
        return f"{self.data_dir}/frames"

    @property
    def cards_dir(self) -> str:
        return f"{self.data_dir}/cards"


@lru_cache
def get_settings() -> Settings:
    return Settings()
