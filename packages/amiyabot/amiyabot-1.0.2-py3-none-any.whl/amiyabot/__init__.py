from . import env

import qqbot
import asyncio

from typing import List, Optional
from amiyabot.handler import BotHandlerFactory
from amiyabot.handler.messageHandler import message_handler
from amiyabot.builtin.lib.htmlConverter import ChromiumBrowser
from amiyabot.builtin.messageChain import Chain
from amiyabot.builtin.message import Message
from amiyabot import log

chromium = ChromiumBrowser()


class AmiyaBot(BotHandlerFactory):
    def __init__(self, appid: str, token: str, public: bool = True):
        super().__init__(appid, token)

        self.handler_type = qqbot.HandlerType.MESSAGE_EVENT_HANDLER
        if public:
            self.handler_type = qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER

        self.parent: Optional[BotHandlerFactory] = None

    async def start(self):
        await chromium.launch()
        await qqbot.async_listen_events(self.instance.token,
                                        False,
                                        qqbot.Handler(self.handler_type, self.__message_handler),
                                        ret_coro=True)

    async def __message_handler(self, event, message: qqbot.Message):
        asyncio.create_task(message_handler(self.parent or self, event, message, instance=self))


class MultipleAccounts(BotHandlerFactory):
    def __init__(self, bots: List[AmiyaBot]):
        super().__init__()

        for item in bots:
            item.parent = self

        self.bots = bots

    async def start(self):
        await asyncio.wait(
            [item.start() for item in self.bots]
        )
