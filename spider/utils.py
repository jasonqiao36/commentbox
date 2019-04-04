import random

import requests
from fake_useragent import UserAgent
from lxml import etree

from config import PROXIES
from spider.encrypt import gen_data, gen_cookies
from spider.log import crawler

TIMEOUT = 5


def choice_proxy():
    if PROXIES:
        return random.choice(PROXIES + [''])
    return ''


def get_user_agent():
    ua = UserAgent()
    return ua.random


def fetch(url, retry=0):
    crawler.info(url)
    s = requests.Session()
    proxies = {
        'http': choice_proxy()
    }
    s.headers.update({
        'Referer': 'http://music.163.com/',
        'User-Agent': get_user_agent(),
    })
    try:
        return s.get(url, timeout=TIMEOUT, proxies=proxies)
    except requests.exceptions.RequestException:
        if retry < 3:
            return fetch(url, retry=retry + 1)
        raise


def post(url):
    headers = {
        "Referer": "https://music.163.com",
        "User-Agent": get_user_agent(),
        'Host': 'music.163.com',
        'Proxy-Connection': 'keep-alive',
        'Origin': 'https://music.163.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    cookies = gen_cookies()
    return requests.post(url, headers=headers, cookies=cookies, data=gen_data())


def get_tree(url):
    r = fetch(url)
    return etree.HTML(r.text)
