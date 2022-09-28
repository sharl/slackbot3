# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup


class call:
    """台風 : 台風情報を表示
台風広域 : 広域の台風情報を表示"""
    def __init__(self, payload):
        item = payload['data']
        text = item['text']
        rtmclient = payload['rtm_client']
        webclient = payload['web_client']
        channel = item['channel']
        thread_ts = item.get('thread_ts')

        url = 'https://typhoon.yahoo.co.jp/weather/jp/typhoon/'
        typhoons = {
            '台風広域': url,
            '台風': url + '?c=1',
        }
        if item.get('subtype', None) is None:
            r = requests.get(url, timeout=10)
            if r and r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                lis = soup.find_all('li', class_='tabView_item')
                for l in lis[2:]:
                    typhoons['台風' + l.a.text] = l.a['href']

                if text in typhoons:
                    url = typhoons[text]
                    r = requests.get(url, timeout=10)
                    if r and r.status_code == 200:
                        soup = BeautifulSoup(r.content, 'html.parser')
                        div = soup.find('div', class_='tabView_content_image')
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
