# -*- coding: utf-8 -*-
from slack_sdk.rtm import RTMClient


@RTMClient.run_on(event='reaction_added')
def reaction_added(**payload):
    rtmclient = payload['rtm_client']
    for module in rtmclient.modules:
        if module.startswith('reaction_added'):
            rtmclient.modules[module].call(payload)
