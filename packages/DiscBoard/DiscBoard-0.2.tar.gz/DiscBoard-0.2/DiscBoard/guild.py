from requests import get, put, delete
from .config import DashConfig
from .Exceptions import MissingBotToken
from typing import Optional


class Guild:

    def __init__(self, guild_id: int) -> None:
        self.guild_id: int = guild_id

    @staticmethod
    def _get_bot_token() -> Optional[str]:
        _token = DashConfig["BOT_TOKEN"]
        if _token:
            return _token
        raise MissingBotToken

    @property
    def get_data(self) -> Optional[dict]:
        bot_token = self._get_bot_token()
        if not bot_token:
            raise MissingBotToken
        response = get(f"https://discord.com/api/v8/guilds/{self.guild_id}",
                       headers={"Authorization": f"Bot {bot_token}"})
        return response.json()

    @property
    def get_banned_members(self) -> Optional[list]:
        token = self._get_bot_token()
        response = get(f"https://discord.com/api/v8/guilds/{self.guild_id}/bans",
                       headers={"Authorization": f"Bot {token}"})
        return response.json()

    @property
    def get_members(self) -> Optional[list]:
        token = self._get_bot_token()
        response = get(f"https://discord.com/api/v8/guilds/{self.guild_id}/members",
                       headers={"Authorization": f"Bot {token}"})
        return response.json()

    @property
    def get_roles(self) -> Optional[list]:
        token = self._get_bot_token()
        response = get(f"https://discord.com/api/v8/guilds/{self.guild_id}/roles",
                       headers={"Authorization": f"Bot {token}"})
        return response.json()

    @property
    def get_channels(self) -> Optional[list]:
        token = self._get_bot_token()
        response = get(f"https://discord.com/api/v8/guilds/{self.guild_id}/channels",
                       headers={"Authorization": f"Bot {token}"})
        return response.json()

    def get_user_ban(self, member_id: int) -> Optional[dict]:
        token = self._get_bot_token()
        response = get(f"https://discord.com/api/v8/guilds/{self.guild_id}/bans/{member_id}",
                       headers={"Authorization": f"Bot {token}"})
        return response.json()

    def ban_member(self, member_id: int, delete_message_days=0, reason="None") -> int:
        token = self._get_bot_token()
        response = put(f"https://discord.com/api/v8/guilds/{self.guild_id}/bans/{member_id}",
                       headers={"Authorization": f"Bot {token}"}, json={"delete_message_days": delete_message_days,
                                                                        "reason": reason})
        return response.status_code

    def unban_member(self, member_id: int) -> int:
        token = self._get_bot_token()
        response = delete(f"https://discord.com/api/v8/guilds/{self.guild_id}/bans/{member_id}",
                       headers={"Authorization": f"Bot {token}"})
        return response.status_code

    def get_user_data(self, member_id: int) -> Optional[dict]:
        token = self._get_bot_token()
        response = get(f"https://discord.com/api/v8/guilds/{self.guild_id}/members/{member_id}",
                       headers={"Authorization": f"Bot {token}"})
        return response.json()
