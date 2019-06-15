# Program to learn how to play War based on reinforcement learning.

# Package imports:

# User imports:
from riskai import StupidAI
from riskenv import RiskEnv
from riskplayer import PlayerInfo

# Main function:
opponents = [PlayerInfo("Dummy", "AI", StupidAI),
             PlayerInfo("Dummy2", "AI", StupidAI)]

env = RiskEnv(opponents)

