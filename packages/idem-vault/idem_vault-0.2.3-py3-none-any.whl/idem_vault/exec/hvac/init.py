"""
This plugin provides an interface for interacting with the raw hvac API using Idem's acct system and CLI paradigm.

All underlying calls are done asynchronously in a Thread-pool Executor
"""


def __init__(hub):
    # Provides the ctx argument to all execution modules
    # which will have profile info from the account module
    hub.exec.hvac.ACCT = ["vault"]

    # Load dynamic subs for accessing hvac client
    hub.pop.sub.dynamic(
        sub=hub.exec.hvac,
        subname="client",
        resolver=hub.tool.hvac.resolve.client,
        context=None,
    )
