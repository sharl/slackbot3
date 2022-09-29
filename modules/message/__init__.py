# -*- coding: utf-8 -*-
from slack_sdk.rtm import RTMClient


@RTMClient.run_on(event='message')
def message(**payload):
    rtmclient = payload['rtm_client']
    rtmclient.caches.parse(payload)
    rtmclient.logger.log(payload)

    for module in rtmclient.modules:
        if module.startswith('message'):
            rtmclient.modules[module].call(payload)
