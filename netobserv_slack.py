#!/usr/bin/env python3

import os
import slack_key

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from chat_netobserv import netobserv_ai_setup

os.environ['SLACK_APP_TOKEN'] = slack_key.app_token
os.environ['SLACK_BOT_TOKEN'] = slack_key.bot_token
app = App(token=os.environ["SLACK_BOT_TOKEN"])

QUERY_FLOWS_WITH_DROP = "show me flows with drop"
QUERY_FLOWS_WITH_NO_DROP = "show me flows with no drop"
QUERY_FLOWS_WITH_SLOW_RTT = "show me flows with slow rtt"
QUERY_FLOWS_WITH_SLOW_DNS = "show me flows with slow dns queries"

def help(message, say, logger):
    say("I'm a bot that can help you troubleshoot OpenShift cluster networking issues. I can help you find flows with drop, flows with no drop and flows with slow rtt.")
    say("examples of questions I can answer:")
    say("`show me flows with no drop`")
    say("`show me flows with drop`")
    say("`show me flows with slow rtt`")
    say("`show me flows with slow dns queries`")


#Message handler for Slack
@app.message(".*")
def message_handler(message, say, logger):
    print(message)

    if message['text'] == "help":
        help(message, say, logger)
        return

    agent = netobserv_ai_setup()

    if QUERY_FLOWS_WITH_NO_DROP == message['text']:
        output = agent.run("show me flows with no drop")
    elif QUERY_FLOWS_WITH_DROP == message['text']:
        output = agent.run("show me flows with drop")
    elif QUERY_FLOWS_WITH_SLOW_RTT == message['text']:
        output = agent.run("show me flows with slow rtt")
    elif QUERY_FLOWS_WITH_SLOW_DNS == message['text']:
        output = agent.run("show me flows with slow dns")
    else:
        output = agent(message['text'])
    print(output)
    say(output)



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
