# -*- coding: utf-8 -*-
class call:
    def __init__(self, payload):
        item = payload['data']
        rtmclient = payload['rtm_client']
        webclient = payload['web_client']

        reaction = 'see_no_evil'
        if isinstance(rtmclient.options, dict) and rtmclient.options.get('reaction'):
            reaction = rtmclient.options['reaction']
        if item['reaction'] == reaction:
            _channel = item['item']['channel']
            _ts = item['item']['ts']
            webclient.chat_delete(
                channel=_channel,
                ts=_ts,
            )
