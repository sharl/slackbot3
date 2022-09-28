# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup


class call:
    """天気図 : 天気図を表示"""
    def __init__(self, payload):
        item = payload['data']
        text = item['text']
        rtmclient = payload['rtm_client']
        webclient = payload['web_client']
        channel = item['channel']
        thread_ts = item.get('thread_ts')

        url = 'https://weather.yahoo.co.jp/weather/chart/'
        if text == '天気図' and item.get('subtype', None) is None:
            r = requests.get(url, timeout=10)
            if r and r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                div = soup.find(id='chart-0')
                webclient.chat_postMessage(
                    channel=channel,
                    username=text,
                    icon_emoji=rtmclient.icon_emoji,
                    text=text,
                    blocks=[
		        {
			    'type': 'image',
			    'image_url': div.img['src'],
			    'alt_text': text,
		        }
                    ],
                    thread_ts=thread_ts,
                )
