import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from riskenv import *

class ActionObservationWrapper(gym.Wrapper):

  def reset(self, **kwargs):
    observation = self.env.reset(**kwargs)
    return self.observation(observation)

  def step(self, action):
    observation, reward, done, info = self.env.step(self.action(action))
    return self.observation(observation), reward, done, info

  def action(self, action):
    raise NotImplementedError

  def reverse_action(self, action):
    raise NotImplementedError

  def observation(self, observation):
    raise NotImplementedError


class FlattenRiskWrapper(ActionObservationWrapper):
  def __init__(self, env:RiskEnv):
    super(FlattenRiskWrapper, self).__init__(env)

    game_state, territories = self.env.observation_space
    new_observation_space = (game_state,)
    for val in territories.spaces.values():
      new_observation_space += val.spaces
    self.observation_space = spaces.Tuple(new_observation_space)

    action_space_size = 1
    self._action_space_shape = tuple([val.n for val in self.env.action_space.spaces])
    for val in self.env.action_space.spaces:
      action_space_size *= val.n
    self.action_space = spaces.Discrete(action_space_size)
    print('actions_space', self.action_space, self.action_space.n)

  def action(self, action):
    assert self.action_space.contains(action)
    pos = np.zeros((self.action_space.n))
    pos[action] = 1
    pos = pos.reshape(self._action_space_shape)
    pos = np.where(pos == 1)
    coords = tuple([coord[0] for coord in pos])
    return coords

  def reverse_action(self, action):
    raise NotImplementedError

  def observation(self, observation):
    assert isinstance(observation, tuple)
    game_state, territories = observation
    assert isinstance(territories, dict)
    new_observation = (game_state,)
    for val in territories.values():
      assert isinstance(val, tuple)
      new_observation += val
    return new_observation


class DqnAgent(object):
  """A Deep Q Learn Agent!"""
  def __init__(self, env:gym.Env):
    self.action_space = env.action_space
    nb_actions = self.action_space.n
    print('nb_actions', nb_actions)
    self.observation_space = env.observation_space
    model = Sequential()
    model.add(Flatten(input_shape=(1,len(self.observation_space))))
    model.add(Dense(100))
    model.add(Activation('relu'))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    print(model.summary())
    memory = SequentialMemory(limit=50000,window_length=1)
    policy = BoltzmannQPolicy()
    dqn = DQNAgent(
      model=model,
      nb_actions=nb_actions,
      memory=memory,
      nb_steps_warmup=20,
      target_model_update=1e-2,
      policy=policy,
    )
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    self.dqn = dqn

  def fit(self,
      env:gym.Env,
      nb_steps=50000,
      visualize=False,
      verbose=0):
    self.dqn.fit(env, nb_steps=nb_steps, visualize=visualize, verbose=verbose)

  def test(self,
      env:gym.Env,
      nb_episodes=5,
      visualize=False,
      verbose=0):
    self.dqn.test(env, nb_episodes=nb_episodes, visualize=visualize, verbose=verbose)

  def save():
    self.dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
