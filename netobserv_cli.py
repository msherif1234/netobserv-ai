import argparse
from chat_netobserv import netobserv_ai_setup

def main():
    output = ""
    parser = argparse.ArgumentParser(description='NetObserv chatbot CLI')
    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument('--drop', help='show flows with drop', action='store_true')
    exclusive_group.add_argument('--nodrop', help='show flows without drop', action='store_true')
    exclusive_group.add_argument('--slowrtt', help='show flows with slow rtt', action='store_true')
    exclusive_group.add_argument('--slowdns', help='show flows with slow dns queries', action='store_true')
    args = parser.parse_args()

    agent = netobserv_ai_setup()

    if args.nodrop:
        output = agent.run("show me flows with no drop")
    if args.drop:
        output = agent.run("show me flows with drop")
    if args.slowrtt:
        output = agent.run("show me flows with slow rtt")
    if args.slowdns:
        output = agent.run("show me flows with slow dns")

    print(output)

if __name__ == "__main__":
    main()
