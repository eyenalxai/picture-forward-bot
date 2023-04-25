from typing import Literal

from pydantic import BaseSettings, Field, validator


class BotSettings(BaseSettings):
    api_token: str = Field(env="API_TOKEN")

    channel_name: str = Field(env="CHANNEL_NAME")
    chat_id: int = Field(env="CHAT_ID")

    domain: str = Field(env="DOMAIN")
    port: int = Field(env="PORT")
    poll_type: Literal["WEBHOOK", "POLLING"] = Field(..., env="POLL_TYPE")
    host: str | None = Field(env="HOST", default="0.0.0.0")

    main_bot_path: str = "/webhook/main"

    @property
    def webhook_url(self: "BotSettings") -> str:
        return "https://{domain}{main_bot_path}".format(
            domain=self.domain,
            main_bot_path=self.main_bot_path,
        )

    @validator("domain")
    def domain_must_not_end_with_slash(
        cls: "BotSettings",  # noqa: N805
        domain: str,
    ) -> str:
        if domain.endswith("/"):
            raise ValueError("DOMAIN must not end with slash")

        if domain.startswith("https://"):
            raise ValueError("DOMAIN must not start with http or https")

        return domain


bot_settings = BotSettings()  # type: ignore
