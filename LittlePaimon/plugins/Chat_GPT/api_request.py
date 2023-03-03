from LittlePaimon.config import config
from requests import session

session = session()
session.headers = {'authorization': f'Bearer {config.chatGPT_APIKEY}'}
BASE_URL = 'https://api.openai.com/v1'


def get_completions(prompt: str, max_tokens: int = 500, temperature: int = 1):
    result = session.post(f'{BASE_URL}/completions', json={
        "model": "text-davinci-003",  # 该模型是GPT-3中最强的模型
        "prompt": prompt,  # 用户说的话
        "max_tokens": max_tokens,  # 200个token大致相当于75个汉字
        "temperature": temperature  # 0-2，数值越大随机性越大
    }).json()
    if result.get('error'):
        return result['error']['message']
    answer_result = result['choices'][0]
    text = answer_result['text'].strip()
    if answer_result['finish_reason'] == 'length':
        text += f'（目前长度最多只支持{max_tokens}个tokens，超出部分已省略。）'
    return text


def get_chat_completions(content: str, max_tokens: int = 5000, temperature: int = 1):
    result = session.post(f'{BASE_URL}/chat/completions', json={
        "model": "gpt-3.5-turbo-0301",  # 该模型是GPT-3中最强的模型
        "messages": [{"role": "user", "content": content}],  # 用户说的话
        "max_tokens": max_tokens,  # 200个token大致相当于75个汉字
        "temperature": temperature  # 0-2，数值越大随机性越大
    }).json()
    if result.get('error'):
        return result['error']['message']
    answer_result = result['choices'][0]
    text = answer_result['message']['content'].strip()
    if answer_result['finish_reason'] == 'length':
        text += f'（目前长度最多只支持{max_tokens}个tokens，超出部分已省略。）'
    return text
