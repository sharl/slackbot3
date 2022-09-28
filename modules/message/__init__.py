# -*- coding: utf-8 -*-
from slack_sdk.rtm import RTMClient


@RTMClient.run_on(event='message')
def message(**payload):
    rtmclient = payload['rtm_client']
    for module in rtmclient.modules:
        if module.startswith('message'):
            rtmclient.modules[module].call(payload)
