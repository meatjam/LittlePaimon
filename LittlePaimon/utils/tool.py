import asyncio
import datetime
import functools
import hashlib
import inspect
import time
from collections import defaultdict
from pathlib import Path

from .logger import logger
from .requests import aiorequests

RESOURCE_BASE_PATH = Path() / 'resources' / 'LittlePaimon'


class FreqLimiter:
    """
    频率限制器（冷却时间限制器）
    """

    def __init__(self):
        """
        初始化一个频率限制器
        """
        self.next_time = defaultdict(float)

    def check(self, key: str) -> bool:
        """
        检查是否冷却结束
        :param key: key
        :return: 布尔值
        """
        return time.time() >= self.next_time[key]

    def start(self, key: str, cooldown_time: int = 0):
        """
        开始冷却
        :param key: key
        :param cooldown_time: 冷却时间(秒)
        """
        self.next_time[key] = time.time() + (cooldown_time if cooldown_time > 0 else 60)

    def left(self, key: str) -> int:
        """
        剩余冷却时间
        :param key: key
        :return: 剩余冷却时间
        """
        return int(self.next_time[key] - time.time()) + 1


freq_limiter = FreqLimiter()


def cache(ttl=datetime.timedelta(hours=1)):
    """
    缓存装饰器
    :param ttl: 过期时间
    """
    def wrap(func):
        cache_data = {}

        @functools.wraps(func)
        async def wrapped(*args, **kw):
            nonlocal cache_data
            bound = inspect.signature(func).bind(*args, **kw)
            bound.apply_defaults()
            ins_key = '|'.join([f'{k}_{v}' for k, v in bound.arguments.items()])
            default_data = {"time": None, "value": None}
            data = cache_data.get(ins_key, default_data)
            now = datetime.datetime.now()
            if not data['time'] or now - data['time'] > ttl:
                try:
                    data['value'] = await func(*args, **kw)
                    data['time'] = now
                    cache_data[ins_key] = data
                except Exception as e:
                    raise e
            return data['value']

        return wrapped

    return wrap


async def check_resource():
    logger.info('资源检查', '开始检查资源')
    resource_list = await aiorequests.get('http://img.genshin.cherishmoon.fun/resources/resources_list')
    resource_list = resource_list.json()
    flag = False
    for resource in resource_list:
        file_path = RESOURCE_BASE_PATH.parent / resource['path']
        if file_path.exists():
            if not resource['lock'] or hashlib.md5(file_path.read_bytes()).hexdigest() == resource['hash']:
                continue
            else:
                file_path.unlink()
        flag = True
        try:
            await aiorequests.download(url=f'http://img.genshin.cherishmoon.fun/resources/{resource["path"]}',
                                       save_path=file_path, exclude_json=resource['path'].split('.')[-1] != 'json')
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.warning('资源检查', f'下载<m>{resource["path"].split("/")[-1]}</m>时<r>出错: {e}</r>')
    if flag:
        logger.info('资源检查', '<g>资源下载完成</g>')
    else:
        logger.info('资源检查', '<g>资源完好，无需下载</g>')
