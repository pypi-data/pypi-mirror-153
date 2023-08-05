from .config import DashConfig
from .Exceptions import MissingBotToken
from requests import get
from typing import Optional


class Application:

    @staticmethod
    def get_bot_token() -> Optional[str]:
        _token = DashConfig["BOT_TOKEN"]
        if _token:
            return _token
        raise MissingBotToken

    @property
    def get_data(self) -> Optional[dict]:
        token = self.get_bot_token()
        response = get(f"https://discord.com/api/oauth2/applications/@me",
                            headers={"Authorization": f"Bot {token}"})
        return response.json()

    @property
    def get_guilds(self) -> Optional[list]:
        token = self.get_bot_token()
        response = get(f"https://discord.com/api/v6/users/@me/guilds",
                       headers={"Authorization": f"Bot {token}"})
        return response.json()
