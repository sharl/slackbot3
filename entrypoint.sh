#!/bin/bash
export SLACK_TOKEN=${SLACK_TOKEN}

exec python3 ./slackbot3.py
