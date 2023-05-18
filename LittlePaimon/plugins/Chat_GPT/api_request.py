import aiohttp
from LittlePaimon.config import config
# from requests import session
from requests_async import Session
from bs4 import BeautifulSoup

BASE_URL = 'https://api.openai.com/v1'


async def get_session_chatgpt():
    session = aiohttp.ClientSession(headers={'authorization': f'Bearer {config.chatGPT_APIKEY}'})
    return session


async def get_session_web():
    session = Session()
    session.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded'
    }
    return session


async def get_completions(prompt: str, max_tokens: int = 500, temperature: int = 1):
    session = await get_session_chatgpt()
    result = await session.post(f'{BASE_URL}/completions', json={
        "model": "text-davinci-003",  # 该模型是GPT-3中最强的模型
        "prompt": prompt,  # 用户说的话
        "max_tokens": max_tokens,  # 200个token大致相当于75个汉字
        "temperature": temperature  # 0-2，数值越大随机性越大
    }, proxy='http://localhost:7981')
    result = await result.json()
    await session.close()
    if result.get('error'):
        return result['error']['message']
    answer_result = result['choices'][0]
    text = answer_result['text'].strip()
    if answer_result['finish_reason'] == 'length':
        text += f'（目前长度最多只支持{max_tokens}个tokens，超出部分已省略。）'
    return text


async def get_chat_completions(content: str, max_tokens: int = None, temperature: int = 1):
    session = await get_session_chatgpt()
    result = await session.post(f'{BASE_URL}/chat/completions', json={
        "model": "gpt-3.5-turbo-0301",  # 该模型是GPT-3中最强的模型
        "messages": [{"role": "user", "content": content}],  # 用户说的话
        "max_tokens": max_tokens,  # 200个token大致相当于75个汉字
        "temperature": temperature  # 0-2，数值越大随机性越大
    }, proxy='http://localhost:7981')
    result = await result.json()
    await session.close()
    if result.get('error'):
        return result['error']['message']
    answer_result = result['choices'][0]
    text = answer_result['message']['content'].strip()
    if answer_result['finish_reason'] == 'length':
        text += f'（目前长度最多只支持{max_tokens}个tokens，超出部分已省略。）'
    return text


async def get_web_search(q: str, max_results=3, region='cn-zh'):
    result = (await (await get_session_web()).post(
        'https://lite.duckduckgo.com/lite',
        data={
            'q': q,
            'kl': region,
            'df': None
        }
    )).text
    soup = BeautifulSoup(result, 'html.parser')
    table = soup.select('table + table')[0]
    contents = table.select('tr > td.result-snippet')
    urls = table.select('tr > td > a')
    outputs = []
    for i in range(0, max_results if max_results < len(contents) else len(contents)):
        outputs.append({'body': contents[i].text.strip(), 'href': urls[i].get('href')})
    return outputs
