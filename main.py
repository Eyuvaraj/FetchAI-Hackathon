import os
from uagents import Agent, Context
alice = Agent(name="alice", seed="alice recovery phrase")

print("Alice's address is", alice.address)

OPENAI_KEY = open(".env", "r").read().strip()