import requests
from typing import Union
from re import findall
from nonebot import on_command
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
from nonebot.rule import to_me

from LittlePaimon.plugins.Chat_GPT.api_request import get_completions, get_chat_completions, get_web_search
from LittlePaimon.utils.message import CommandCharacter, CommandLang, MessageBuild


__plugin_meta__ = PluginMetadata(
    name='ChatGPT聊天',
    description='ChatGPT聊天',
    usage='@Bot chat [聊天内容]',
    extra={
        'author': 'meatjam',
        'version': '1.0',
        'priority': 11,
        # 'configs': {
        #     '签到开始小时': 0,
        #     '签到开始分钟': 5,
        #     '米游币开始小时': 0,
        #     '米游币开始分钟': 30
        # }
    }
)

chat_gpt = on_command('chat', priority=8, block=True, rule=to_me(), state={
    'pm_name': 'ChatGPT聊天',
    'pm_description': 'ChatGPT聊天',
    'pm_usage': '@Bot chat [聊天内容]',
    'pm_priority': 3
})

web_search = on_command('web', priority=8, block=True, rule=to_me(), state={
    'pm_name': '联网的智能化Web搜索',
    'pm_description': '联网的智能化Web搜索',
    'pm_usage': '@Bot web ([期望返回数]默认3条) [搜索内容]',
    'pm_priority': 3
})


# is_thinking = False


@chat_gpt.handle()
async def _(event: Union[GroupMessageEvent, PrivateMessageEvent], msg: Message = CommandArg()):
    # global is_thinking
    if not event.to_me:
        return
    # if is_thinking:
    #     await chat_gpt.finish('正在思考中......（一次只能一条哦，请等待回复后再发送。）')
    #     return
    msg = msg.extract_plain_text().strip()
    # is_thinking = True
    try:
        await chat_gpt.finish(await get_chat_completions(msg))
    except FinishedException:
        pass
    except Exception as e:
        await chat_gpt.finish(f'出错了，请稍后重试。{e}')
    # finally:
    #     is_thinking = False


@web_search.handle()
async def _(event: Union[GroupMessageEvent, PrivateMessageEvent], msg: Message = CommandArg()):
    if not event.to_me:
        return
    msg_input = msg.extract_plain_text().strip()
    number_index = msg_input.find(' ')
    first_input = msg_input[:number_index]
    if len(findall(r'\D', first_input)) > 0:
        msg = msg_input
        max_results = 3
    else:
        msg = msg_input[number_index:].strip()
        max_results = int(first_input)
    try:
        result = await get_web_search(msg, max_results)
        output_strings = []
        i = 1
        for content in result:
            output_strings.append(f'[{i}] "{content["body"]}"\n{content["href"]}\n')
            i += 1
        await chat_gpt.finish('\n'.join(output_strings))
    except FinishedException:
        pass
    except Exception as e:
        await chat_gpt.finish(f'出错了，请稍后重试。{e}')
