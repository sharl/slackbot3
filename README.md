slackbot3
=========

sample script for slackbot

## preinstall
```
git clone https://github.com/sharl/geeklets.git
cp geeklets/.amedas ~
cp geeklets/{amedas,amesh} ~/bin
```

- amesh use imagemagick

## prereq
```
pip install --upgrade slack_sdk aiohttp requests bs4
```

## usage

```
$ SLACK_TOKEN=xoxb-hogehoge ./slackbot3.py
```

## Appendix
```
make
SLACK_TOKEN=xoxb-hogehoge docker-compose up -d
```

## DB module

- initialize
```
./initdb.py init
```
to create table.

### name_history

- config.json
```
    "name_history": {
        "keyword": "email address"
    }
```

### switchbot.meter

- config.json
```
    "switchbot.meter": {
        "keyword": "wake word",
        "user": "user name (NOT display name)",
        "token": "<developer token>",
        "device": "<device ID>"
    }
```

### switchbot.plug

- config.json
```
    "switchbot.plug": {
        "on": "on wake word",
        "off": "off wake word",
        "user": "user name (NOT display name)",
        "token": "<developer token>",
        "device": "<device ID>"
    }
```
