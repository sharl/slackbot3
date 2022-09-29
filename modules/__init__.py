# -*- coding: utf-8 -*-
import os
import sys
import json
import importlib

from slack_sdk.rtm import RTMClient


class App:
    rtmclient = None
    modules = {}
    options = {}
    doc = ''

    def __init__(self):
        token = os.environ.get('SLACK_TOKEN')
        if not token:
            print('SLACK_TOKEN is not set')
            sys.exit(1)
        self.rtmclient = RTMClient(token=token)

        try:
            with open('/config/config.json') as fd:
                config = json.load(fd)
        except Exception:
            with open('config/config.json') as fd:
                config = json.load(fd)

        self.name = config.get('name', 'bot')
        self.icon_emoji = config.get('icon_emoji', ':bot:')
        mods = config.get('modules', {})
        docs = []
        for module in sorted(mods):
            m = importlib.import_module('modules.{}'.format(module))
            self.modules[module] = m
            self.options[module] = mods[module]
            doc = m.call.__doc__
            if doc:
                docs.append(doc)
        self.doc = '\n'.join(docs)

        # add members
        self.rtmclient.doc = self.doc
        self.rtmclient.name = self.name
        self.rtmclient.icon_emoji = self.icon_emoji
        self.rtmclient.modules = self.modules
        self.rtmclient.options = self.options

    def start(self):
        self.rtmclient.start()
