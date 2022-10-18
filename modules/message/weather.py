# -*- coding: utf-8 -*-
from datetime import datetime
import json
import subprocess

import requests

area_json = 'https://www.jma.go.jp/bosai/common/const/area.json'
fore_json = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json'


class call:
    """天気[市区町村] : 現在からの情報を表示"""
    def __init__(self, payload):
        item = payload['data']
        text = item['text']
        rtmclient = payload['rtm_client']
        webclient = payload['web_client']
        channel = item['channel']
        thread_ts = item.get('thread_ts')

        prefix = '天気'
        if text.startswith(prefix) and item.get('subtype') is None:
            loc = text.replace(prefix, '')

            r = requests.get(area_json)
            if r and r.status_code == 200:
                areas = json.loads(r.content)

                class10s = areas['class10s']
                class15s = areas['class15s']
                class20s = areas['class20s']
                offices = areas['offices']

                for c in class20s:
                    if class20s[c]['name'] == loc:
                        region = class20s[c]['parent']
                        area = class15s[region]['parent']
                        code = class10s[area]['parent']
                        area_name = offices[code]['name']

                        r = requests.get(fore_json.format(code))
                        if r and r.status_code == 200:
                            forecast = json.loads(r.content)

                            today = forecast[0]
                            # week = forecast[1]

                            w = today['timeSeries'][0]
                            p = today['timeSeries'][1]
                            t = today['timeSeries'][2]
                            for i, a in enumerate(w['areas']):
                                if a['area']['code'] == area:
                                    # date and pop
                                    pops = {}
                                    for j, d in enumerate(p['timeDefines']):
                                        pops[datetime.fromisoformat(d).strftime('%m/%d %H')] = p['areas'][i]['pops'][j]

                                    blocks = [
                                        {
                                            'type': 'context',
                                            'elements': [
                                                {
                                                    'type': 'mrkdwn',
                                                    'text': f'*{area_name} {loc}*'
                                                }
                                            ]
                                        }
                                    ]

                                    # add svg block
                                    for j, f in enumerate(a['weatherCodes']):
                                        trans = {
                                            '203': 202,
                                        }
                                        g = trans[f] if f in trans else f

                                        d = datetime.fromisoformat(w['timeDefines'][j]).strftime('%m/%d')
                                        _pops = [d + '          ']

                                        for p in pops:
                                            if p.startswith(d):
                                                _pops.append(pops[p] + '%')

                                        blocks.append({
                                            'type': 'image',
                                            'title': {
                                                'type': 'plain_text',
                                                'text': '  '.join(_pops),
                                                'emoji': True
                                            },
                                            'image_url': f'https://www.jma.go.jp/bosai/forecast/img/{g}.png',
                                            'alt_text': 'weather'
                                        })

                                    # amedas challenge
                                    for a in t['areas']:
                                        _name = a['area']['name']
                                        _code = a['area']['code']
                                        if loc.startswith(_name):
                                            amedas = subprocess.check_output(['amedas', _code]).decode('utf8').strip()
                                            blocks.append({
                                                'type': 'context',
                                                'elements': [
                                                    {
                                                        'type': 'plain_text',
                                                        'text': amedas,
                                                    }
                                                ]
                                            })

                                    webclient.chat_postMessage(
                                        username=prefix,
                                        icon_emoji=rtmclient.icon_emoji,
                                        channel=channel,
                                        text='気象庁発表',
                                        blocks=blocks,
                                        thread_ts=thread_ts,
                                    )
