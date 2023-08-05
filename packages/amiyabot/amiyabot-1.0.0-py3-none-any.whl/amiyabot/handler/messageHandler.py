import qqbot

from typing import List, Tuple, Optional
from qqbot.model.ws_context import WsContext
from amiyabot.builtin.message.builder import package_message
from amiyabot.builtin.message import Message, Verify, WaitEvent, WaitEventCancel, wait_events
from amiyabot.handler import MessageHandlerItem, BotHandlerFactory
from amiyabot import log

CHOICE = Optional[Tuple[Verify, MessageHandlerItem]]


async def choice_handlers(data: Message, handlers: List[MessageHandlerItem]) -> CHOICE:
    candidate: List[Tuple[Verify, MessageHandlerItem]] = []

    for item in handlers:
        check = await item.verify(data)
        if check:
            candidate.append((check, item))

    if not candidate:
        return None

    return sorted(candidate, key=lambda n: len(n[0]), reverse=True)[0]


async def message_handler(bot: BotHandlerFactory, event: WsContext, message: qqbot.Message):
    data = await package_message(bot, event, message)

    if not data:
        return

    # 执行中间处理函数
    if bot.message_handler_middleware:
        data = await bot.message_handler_middleware(data) or data

    waiting: Optional[WaitEvent] = None
    if data.channel_id:
        waiting_target = f'{data.channel_id}_{data.user_id}'
    else:
        waiting_target = data.user_id

    # 寻找是否存在等待事件
    if data.channel_id in wait_events:
        waiting = wait_events[data.channel_id]
    if waiting_target in wait_events:
        waiting = wait_events[waiting_target]

    # 若存在等待事件并且等待事件设置了强制等待，则直接进入事件
    if waiting and waiting.force:
        waiting.set(data)
        return

    choice = await choice_handlers(data, bot.message_handlers)

    # 执行选中的功能
    if choice:
        handler = choice[1]
        data.verify = choice[0]

        # 执行前置处理函数
        flag = True
        if bot.before_reply_handlers:
            for action in bot.before_reply_handlers:
                res = await action(data)
                if not res:
                    flag = False
        if not flag:
            return

        # 执行功能并取消等待
        async with log.catch('Handler error:', ignore=[WaitEventCancel]):
            reply = await handler.action(data)
            if reply:
                await data.send(reply)
                if waiting:
                    waiting.cancel()

    # 未选中任何功能或功能无法返回时，进入等待事件（若存在）
    if waiting:
        waiting.set(data)
