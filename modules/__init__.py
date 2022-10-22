# -*- coding: utf-8 -*-
import os
import sys
import json
import importlib
from datetime import datetime

from slack_sdk.rtm import RTMClient


class Caches:
    # 問い合わせを減らすためのチャンネルIDキャッシュ
    channel_ids = {}
    # 問い合わせを減らすためのユーザIDキャッシュ
    user_ids = {}
    doc = ''

    def __init__(self):
        pass

    def parse(self, payload):
        webclient = payload['web_client']

        user_id = payload.get('data', {}).get('user')
        #
        # detect user
        #
        if isinstance(user_id, str) and user_id not in self.user_ids:
            user = webclient.users_info(user=user_id)
            if user['ok'] is True:
                user_name = user.get('user', {}).get('name')
                if user_name is not None:
                    self.user_ids[user_id] = user_name

        channel_id = payload.get('data', {}).get('channel')
        #
        # detect channel
        #
        if isinstance(channel_id, str) and channel_id not in self.channel_ids:
            if channel_id.startswith('C'):
                # channel
                chan = webclient.conversations_info(channel=channel_id)
                if chan['ok'] is True:
                    channel_name = chan.get('channel', {}).get('name')
                    if channel_name is not None:
                        self.channel_ids[channel_id] = channel_name
            elif channel_id.startswith('D'):
                # im
                user_name = self.user_ids.get(user_id, '???')
                self.channel_ids[channel_id] = user_name
            elif channel_id.startswith('G'):
                # group im (mpim)
                group = webclient.groups_info(channel=channel_id)
                if group['ok'] is True:
                    channel_name = group.get('group', {}).get('name')
                    if channel_name is not None:
                        self.channel_ids[channel_id] = channel_name

            if channel_id not in self.channel_ids:
                self.channel_ids[channel_id] = channel_id


class Logger:
    def __init__(self):
        pass

    def log(self, payload):
        rtmclient = payload.get('rtm_client')
        item = payload.get('data')
        if rtmclient and item and item.get('bot_id', None) is None:
            text = item.get('text')
            user = item.get('user')
            channel = item.get('channel')
            ts = item.get('ts')
            if text and user and channel and ts:
                print('{} {}> {}: {}'.format(datetime.fromtimestamp(float(ts)).strftime('%H:%M:%S'),
                                             rtmclient.caches.channel_ids[channel],
                                             rtmclient.caches.user_ids[user],
                                             text))


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

        # add members and cache and logger
        self.rtmclient.doc = self.doc
        self.rtmclient.name = self.name
        self.rtmclient.icon_emoji = self.icon_emoji
        self.rtmclient.modules = self.modules
        self.rtmclient.options = self.options
        self.rtmclient.caches = Caches()
        self.rtmclient.logger = Logger()

    def start(self):
        self.rtmclient.start()
