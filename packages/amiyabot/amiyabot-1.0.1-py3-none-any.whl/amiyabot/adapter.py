import qqbot
import asyncio

from typing import Optional
from qqbot.api import User
from amiyabot import log


class BotInstance:
    def __init__(self, appid: str, token: str):
        self.token = qqbot.Token(appid, token)
        self.user_api = qqbot.AsyncUserAPI(self.token, False)
        self.guild_api = qqbot.AsyncGuildAPI(self.token, False)
        self.channel_api = qqbot.AsyncChannelAPI(self.token, False)
        self.message_api = qqbot.AsyncMessageAPI(self.token, False)

        self.bot: Optional[User] = None

    async def get_me(self) -> User:
        if not self.bot:
            self.bot = await self.user_api.me()
        return self.bot

    async def send_message(self, messages):
        for req in await messages.build():
            async with log.catch('Post message error:', ignore=[asyncio.TimeoutError]):
                await self.message_api.post_message(messages.data.channel_id, req)
