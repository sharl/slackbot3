# -*- coding: utf-8 -*-
import subprocess


class call:
    """アメダス[観測地点] : アメダスでの現在の情報を表示"""
    def __init__(self, payload):
        item = payload['data']
        text = item['text']
        rtmclient = payload['rtm_client']
        webclient = payload['web_client']
        channel = item['channel']
        thread_ts = item.get('thread_ts')

        prefix = 'アメダス'
        if text.startswith(prefix) and item.get('bot_id') is None:
            loc = text.replace(prefix, '')
            amedas = subprocess.check_output(['amedas', loc]).decode('utf8').strip()
            webclient.chat_postMessage(
                username=prefix,
                icon_emoji=rtmclient.icon_emoji,
                channel=channel,
                text=amedas,
                thread_ts=thread_ts,
            )
