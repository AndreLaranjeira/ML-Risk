# Program to learn how to play War based on reinforcement learning.

# Package imports:

# User imports:
from riskai import StupidAI
from riskenv import *
from riskplayer import PlayerInfo
from riskagent import *
import logging
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

logging.disable()

# Main function:
opponents = [PlayerInfo("Dummy", "AI", StupidAI),
             PlayerInfo("Dummy2", "AI", StupidAI)]

env = FlattenRiskWrapper(RiskEnv(opponents))

agent = DqnAgent(env)

ans = str(input("Deseja carregar os pesos de um arquivo?(S/n) "))
if ans.lower() != 'n':
    name = str(input("Nome do modelo: "))
    agent.load(name)

ans = str(input("Deseja pular o treinamento?(s/N) "))
if ans.lower() != 's':
  agent.fit(env, verbose=0,nb_steps=50000)

logging.disable(logging.NOTSET)

agent.test(env, verbose=2)

ans = str(input("Deseja salvar?(S/n) "))
name = ''
if ans.lower() != 'n':
  name = input("Nome do modelo: ")
  agent.save(name)


ans = str(input("Deseja calcular e exibir os gráficos das métricas?\nO nome será {}.(S/n) ".format(name)))
if ans.lower() != 'n':
  should_plot = {
    'episode_reward': plt.figure("Reward").gca(),
    'nb_episode_steps': plt.figure("Steps").gca(),
  }
  for k, v in should_plot.items():
    v.plot(agent.history[k])
    v.set_xlabel("Episodes")
    v.xaxis.set_major_locator(MaxNLocator(integer=True))
  should_plot['episode_reward'].set_ylabel("Accumulated Reward")
  should_plot['episode_reward'].set_title("Reward Evolution")
  should_plot['nb_episode_steps'].set_ylabel("Number of Steps")
  should_plot['nb_episode_steps'].set_title("Steps per Episode Evolution")

  should_plot_test = {
    'episode_reward': plt.figure("Test Reward").gca(),
    'nb_steps': plt.figure("Test Steps").gca(),
  }
  for k, v in should_plot_test.items():
    v.plot(agent.test_history[k])
    v.set_xlabel("Test Episodes")
    v.xaxis.set_major_locator(MaxNLocator(integer=True))
  should_plot_test['episode_reward'].set_ylabel("Accumulated Reward")
  should_plot_test['episode_reward'].set_title("Reward")
  should_plot_test['nb_steps'].set_ylabel("Number of Steps")
  should_plot_test['nb_steps'].set_title("Steps per Episode")

  ans = str(input("Deseja salvar as imagens?(S/n) "))
  if ans.lower() != 'n':
    for label in plt.get_figlabels():
      fig = plt.figure(label)
      fig.savefig('img/dqn_{}_{}.png'.format(name, label.replace(' ', '_')))

  plt.show()
