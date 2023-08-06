import qqbot

from typing import List, Tuple, Union, Optional
from qqbot.model.ws_context import WsContext
from amiyabot.builtin.message.builder import package_message
from amiyabot.builtin.message import Message, Verify, WaitEvent, WaitChannelEvent, WaitEventCancel, wait_events_bucket
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

    waiter: Union[WaitEvent, WaitChannelEvent, None] = None
    if data.channel_id:
        waiting_target = f'{data.channel_id}_{data.user_id}'
    else:
        waiting_target = data.user_id

    # 寻找是否存在等待事件
    if data.channel_id in wait_events_bucket:
        waiter = wait_events_bucket[data.channel_id]
    if waiting_target in wait_events_bucket:
        waiter = wait_events_bucket[waiting_target]

    if waiter and not waiter.check_alive():
        waiter = None

    # 若存在等待事件并且等待事件设置了强制等待，则直接进入事件
    if waiter and waiter.force:
        waiter.set(data)
        return

    choice = await choice_handlers(data, bot.message_handlers)
    if choice:
        handler = choice[1]

        # 执行前置处理函数
        flag = True
        if bot.before_reply_handlers:
            for action in bot.before_reply_handlers:
                res = await action(data)
                if not res:
                    flag = False
        if not flag:
            return

        # 执行功能，若存在等待事件，则取消
        async with log.catch('Handler error:', ignore=[WaitEventCancel]):
            reply = await handler.action(data)
            if reply:
                if waiter and waiter.type == 'user':
                    waiter.cancel()
                await data.send(reply)

    # 未选中任何功能或功能无法返回时，进入等待事件（若存在）
    if waiter:
        waiter.set(data)
