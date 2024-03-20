#!/usr/bin/env python3
from langserve import RemoteRunnable

def netobserv_client():
    remote_runnable = RemoteRunnable("http://localhost:8000/")
    out = remote_runnable.invoke({"input": "hi!"})
    print(out['output'])
    out = remote_runnable.invoke({"input": "show netobserv flows with drops?"})
    print(out['output'])
    out = remote_runnable.invoke({"input": "show netobserv flows with no drops?"})
    print(out['output'])

    out = remote_runnable.invoke({"input": "show netobserv flows high DNS latency?"})
    print(out['output'])

    out = remote_runnable.invoke({"input": "show netobserv flows high rtt latency?"})
    print(out['output'])

    out = remote_runnable.invoke({"input": "show netobserv flows with network policy drops?"})
    print(out['output'])

if __name__ == '__main__':
    netobserv_client()
