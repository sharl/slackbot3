# -*- coding: utf-8 -*-
class call:
    def __init__(self, payload):
        item = payload['data']
        text = item['text']
        rtmclient = payload['rtm_client']
        webclient = payload['web_client']
        channel = item['channel']
        thread_ts = item.get('thread_ts')

        if text.strip().replace(' ', '') in ['help&gt;はむ', 'help＞はむ', 'ヘルプ&gt;はむ', 'ヘルプ＞はむ']:
            webclient.chat_postMessage(
                username=rtmclient.name,
                icon_emoji=rtmclient.icon_emoji,
                channel=channel,
                text=rtmclient.doc,
                thread_ts=thread_ts,
            )
