import re
import time
import qqbot
import asyncio
import collections

from typing import List, Dict, Tuple, Union, Optional, Callable

equal = collections.namedtuple('equal', ['content'])  # 全等对象，接受一个字符串，表示消息文本完全匹配该值


class Verify:
    def __init__(self, result: bool, weight: Union[int, float] = 0, keywords: List[str] = None):
        """
        消息校验结果对象

        :param result:   校验结果
        :param weight:   权重（优先级），用于当同时存在多个检验结果时，可根据权值匹配优先的结果
        :param keywords: 校验成功匹配出来的关键字列表
        """
        self.result = result
        self.keywords = keywords or []
        self.weight = weight

    def __bool__(self):
        return self.result

    def __repr__(self):
        return f'<Verify, {self.result}, {self.weight}>'

    def __len__(self):
        return self.weight


class Message:
    def __init__(self, bot, message: qqbot.Message):
        """
        二次封装的消息对象
        """
        self.bot = bot
        self.message = message
        self.message_id = message.id

        self.face = []
        self.image = []

        self.text = ''
        self.text_digits = ''
        self.text_origin = ''
        self.text_initial = ''
        self.text_words = []

        self.at_target = []

        self.is_at = False
        self.is_admin = False

        self.user_id = message.author.id
        self.guild_id = message.guild_id
        self.channel_id = message.channel_id
        self.nickname = message.author.username

        self.time = int(time.time())

        self.verify: Optional[Verify] = None

    def __str__(self):
        text = self.text_origin.replace('\n', ' ')
        face = ''.join([f'[face:{n}]' for n in self.face])
        image = '[image]' * len(self.image)

        return 'Guild:{guild} Channel:{channel} {nickname}: {message}'.format(
            **{
                'guild': self.guild_id,
                'channel': self.channel_id,
                'nickname': self.nickname,
                'message': text + face + image
            }
        )

    async def send(self, reply):
        await self.bot.instance.send_message(reply)

    async def waiting(self,
                      reply=None,
                      max_time: int = 30,
                      force: bool = False,
                      target: str = 'user',
                      data_filter: Callable = None):

        if target == 'channel':
            target_id = self.channel_id
        else:
            if self.channel_id:
                target_id = f'{self.channel_id}_{self.user_id}'
            else:
                target_id = self.user_id

        wid = await wait_events.set_wait(target_id, force, target)

        if reply:
            await self.bot.instance.send_message(reply)

        while max_time:
            await asyncio.sleep(0.5)
            max_time -= 0.5

            if target_id in wait_events:

                wait_object = wait_events[target_id]

                if wid != wait_object.wid:
                    raise WaitEventCancel(target_id)

                if wait_object.data:
                    if data_filter:
                        res = await data_filter(wait_object.data)
                        if not res:
                            wait_object.data = None
                            continue

                    data = wait_object.data

                    del wait_events[target_id]
                    return data

            else:
                return None

        if wid == wait_events[target_id].wid:
            del wait_events[target_id]


class MessageMatch:
    @staticmethod
    def check_str(data: Message, text: str, level: int) -> Tuple[bool, int, List[str]]:
        if text.lower() in data.text_origin.lower():
            return True, level or 1, [str(text)]
        return False, 0, []

    @staticmethod
    def check_equal(data: Message, text: equal, level: int) -> Tuple[bool, int, List[str]]:
        if text.content == data.text_origin:
            return True, level or 10000, [str(text)]
        return False, 0, []

    @staticmethod
    def check_reg(data: Message, reg: re.Pattern, level: int) -> Tuple[bool, int, List[str]]:
        r = re.search(reg, data.text_origin)
        if r:
            return True, level or (r.re.groups or 1), [str(item) for item in r.groups()]
        return False, 0, []


class WaitEvent:
    def __init__(self, wid: int, target_id: int, force: bool, target: str):
        self.wid = wid
        self.force = force
        self.target = target
        self.target_id = target_id
        self.data: Optional[Message] = None

    def set(self, data: Message):
        self.data = data

    def cancel(self):
        self.wid = None


class WaitEventsBucket:
    def __init__(self):
        self.id = 0
        self.lock = asyncio.Lock()
        self.bucket: Dict[Union[int, str], WaitEvent] = {}

    def __contains__(self, item):
        return item in self.bucket

    def __getitem__(self, item):
        try:
            return self.bucket[item]
        except KeyError:
            return None

    def __delitem__(self, key):
        try:
            del self.bucket[key]
        except KeyError:
            pass

    async def __get_id(self):
        async with self.lock:
            self.id += 1
            return self.id

    async def set_wait(self, target_id: Union[int, str], force: bool, target: str):
        wid = await self.__get_id()

        self.bucket[target_id] = WaitEvent(wid, target_id, force, target)

        return wid


class WaitEventCancel(Exception):
    def __init__(self, key: Union[int, str]):
        self.key = key
        del wait_events[key]

    def __str__(self):
        return f'WaitEventCancel: {self.key}'


wait_events = WaitEventsBucket()
