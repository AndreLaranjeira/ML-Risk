# Program to learn how to play War based on reinforcement learning.

# Package imports:

# User imports:
from riskai import StupidAI
from riskenv import RiskEnv
from riskplayer import PlayerInfo
from riskagent import *

# Main function:
opponents = [PlayerInfo("Dummy", "AI", StupidAI),
             PlayerInfo("Dummy2", "AI", StupidAI)]

env = FlattenRiskWrapper(RiskEnv(opponents))

agent = DqnAgent(env)

agent.fit(env, verbose=2)

agent.test(env, verbose=2)
