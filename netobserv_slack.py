#!/usr/bin/env python3

import os
import slack_key

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from chat_netobserv import Netobserv_ai_setup

os.environ['SLACK_APP_TOKEN'] = slack_key.app_token
os.environ['SLACK_BOT_TOKEN'] = slack_key.bot_token
app = App(token=os.environ["SLACK_BOT_TOKEN"])

#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)

    agent = Netobserv_ai_setup()

    if "nodrop" in message['text']:
        output = agent("show me all flows with no drop")
    elif "drop" in message['text']:
        output = agent("show me all flows with drop")
    elif "slow rtt" in message['text']:
        output = agent("show me all flows with slow rtt")
    else:
        output = agent(message['text'])

    for flow in output:
        say(flow)



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()