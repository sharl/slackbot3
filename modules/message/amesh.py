# -*- coding: utf-8 -*-
import subprocess


class call:
    """アメッシュ : アメッシュ画像を表示"""
    def __init__(self, payload):
        item = payload['data']
        text = item['text']
        rtmclient = payload['rtm_client']
        webclient = payload['web_client']
        channel = item['channel']
        thread_ts = item.get('thread_ts')

        keyword = 'アメッシュ'
        if text == keyword and item.get('bot_id') is None:
            amesh = subprocess.check_output(['amesh', '-c'])
            with open('/tmp/amesh.png', 'wb') as fd:
                fd.write(amesh)
            webclient.files_upload(
                username=keyword,
                icon_emoji=rtmclient.icon_emoji,
                channels=channel,
                file='/tmp/amesh.png',
                title='amesh',
                thread_ts=thread_ts,
            )
