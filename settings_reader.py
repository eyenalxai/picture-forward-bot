from enum import Enum

from pydantic import BaseSettings, Field, validator


class PollType(Enum):
    WEBHOOK = "WEBHOOK"
    POLLING = "POLLING"


class Settings(BaseSettings):
    api_token: str = Field(env="API_TOKEN")
    channel_name: str = Field(env="CHANNEL_NAME")
    domain: str = Field(env="DOMAIN")
    port: int = Field(env="PORT")
    poll_type: PollType = Field(env="POLL_TYPE")
    description: str = Field(env="DESCRIPTION")
    chat_id: int = Field(env="CHAT_ID")
    main_bot_path: str = "/webhook/main"

    @property
    def webhook_url(self) -> str:
        return f"https://{self.domain}{self.main_bot_path}"

    @validator("domain")
    def domain_must_not_end_with_slash(cls, v: str) -> str:
        assert not v.endswith("/"), "DOMAIN must not end with slash"
        assert not v.startswith("http"), "DOMAIN must not start with http or https"
        return v


settings = Settings()
