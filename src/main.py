# Program to learn how to play War based on reinforcement learning.

# Package imports:

# User imports:
from riskai import StupidAI
from riskenv import RiskEnv, RiskAttackEnv
from riskplayer import PlayerInfo
from riskagent import *
import logging

logging.disable()

# Main function:
opponents = [PlayerInfo("Dummy", "AI", StupidAI),
             PlayerInfo("Dummy2", "AI", StupidAI)]

env = FlattenRiskWrapper(RiskAttackEnv(opponents))

agent = DqnAgent(env)

ans = str(input("Deseja carregar os pesos de um arquivo?(S/n) "))
if ans.lower() != 'n':
    name = str(input("Nome do modelo: "))
    agent.load(name)

ans = str(input("Deseja pular o treinamento?(s/N) "))
if ans.lower() != 's':
  agent.fit(env, verbose=1)

logging.disable(logging.NOTSET)

agent.test(env, verbose=2)

ans = str(input("Deseja salvar?(S/n) "))
if ans.lower() != 'n':
  name = input("Nome do modelo: ")
  agent.save(name)
