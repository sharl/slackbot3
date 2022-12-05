# -*- coding: utf-8 -*-
import json
import requests


class call:
    def __init__(self, payload):
        item = payload['data']
        text = item['text']
        rtmclient = payload['rtm_client']
        webclient = payload['web_client']
        channel = item['channel']
        thread_ts = item.get('thread_ts')

        module = __name__.replace('modules.', '')
        options = rtmclient.options[module]
        prefix = options.get('prefix', '{}:'.format(rtmclient.name))
        sorry = options.get('sorry', 'Sorry, I am not sure.')
        apikey = options.get('apikey')

        if text.startswith(prefix) and item.get('bot_id') is None:
            prompt = text.replace(prefix, '')
            data = {
                'model': 'text-davinci-003',
                'prompt': prompt,
                'temperature': 0.7,
                'max_tokens': 4000,
                'top_p': 1,
                'frequency_penalty': 0,
                'presence_penalty': 0,
            }
            try:
                r = requests.post('https://api.openai.com/v1/completions',
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Authorization': 'Bearer {}'.format(apikey),
                                  },
                                  json=data,
                                  timeout=30)
                print(r)
                if r and r.status_code == 200:
                    print(r.text)
                    answer = json.loads(r.text).get('choices', [{}])[0].get('text')
                    print(answer)
                    webclient.chat_postMessage(
                        username=rtmclient.name,
                        icon_emoji=rtmclient.icon_emoji,
                        channel=channel,
                        text=answer,
                        thread_ts=thread_ts,
                    )
                    return
            except Exception:
                pass

            webclient.chat_postMessage(
                username=rtmclient.name,
                icon_emoji=rtmclient.icon_emoji,
                channel=channel,
                text=sorry,
                thread_ts=thread_ts,
            )
