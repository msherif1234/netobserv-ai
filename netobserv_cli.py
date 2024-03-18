import argparse
from chat_netobserv import netobserv_ai_setup


def process_netobserv_cli():
    parser = argparse.ArgumentParser(description='NetObserv chatbot CLI')
    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument('--drop', help='show flows with drop', action='store_true')
    exclusive_group.add_argument('--nodrop', help='show flows without drop', action='store_true')
    exclusive_group.add_argument('--slowrtt', help='show flows with slow rtt', action='store_true')
    exclusive_group.add_argument('--slowdns', help='show flows with slow dns queries', action='store_true')
    exclusive_group.add_argument('--netpol', help='show flows with netpol drop', action='store_true')
    args = parser.parse_args()

    agent = netobserv_ai_setup(verbose=True)

    if args.nodrop:
        agent.invoke("show me flows with no drop")
    if args.drop:
        agent.invoke("show me flows with drop")
    if args.slowrtt:
        agent.invoke("show me flows with slow rtt")
    if args.slowdns:
        agent.invoke("show me flows with slow dns")
    if args.netpol:
        agent.invoke("show me flows with netpol drop")


if __name__ == "__main__":
    process_netobserv_cli()
