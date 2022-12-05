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
SLACK_TOKEN=xoxb-hogehoge docker-compose up -p project_name -d
```

## Module usage

### message.switchbot.meter

- config.json
```
        "message.switchbot.meter": {
            "keyword": "wake word",
            "user": "user name (NOT display name)",
            "token": "<developer token>",
            "device": "<device ID>"
        }
```

### message.switchbot.plug

- config.json
```
        "message.switchbot.plug": {
            "on": "on wake word",
            "off": "off wake word",
            "user": "user name (NOT display name)",
            "token": "<developer token>",
            "device": "<device ID>"
        }
```

### message.openai

- config.json
```
	"message.openai": {
	    "prefix": "hamu:",
	    "sorry": "Sorry, I am not sure.",
	    "apikey": "sk-xxxxxx"
	}
```
