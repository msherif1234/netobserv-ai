#!/usr/bin/env python3

import os
import slack_key

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from chat_netobserv import Netobserv_ai_setup

os.environ['SLACK_APP_TOKEN'] = slack_key.app_token
os.environ['SLACK_BOT_TOKEN'] = slack_key.bot_token
app = App(token=os.environ["SLACK_BOT_TOKEN"])

def help(message, say, logger):
    say("I'm a bot that can help you troubleshoot OpenShift cluster networking issues. I can help you find flows with drop, flows with no drop and flows with slow rtt.")
    say("examples of questions I can answer:")
    say("`show me all flows with no drop`")
    say("`show me all flows with drop`")
    say("`show me all flows with slow rtt`")
    say("`show me all flows with slow dns queries`")


#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)

    if message['text'] == "help":
        help(message, say, logger)
        return

    agent = Netobserv_ai_setup()

    if "nodrop" in message['text']:
        output = agent.invoke("show me all flows with no drop")
    elif "drop" in message['text']:
        output = agent.invoke("show me all flows with drop")
    elif "slow rtt" in message['text']:
        output = agent.invoke("show me all flows with slow rtt")
    elif "slow dns" in message['text']:
        output = agent.invoke("show me all flows with slow dns")
    else:
        output = agent(message['text'])

    say(output)



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
