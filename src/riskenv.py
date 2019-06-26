# Module to implement the OpenAI gym environment for the Risk game.

# Package imports:
import gym
from gym import spaces
from gym.utils import seeding
import logging
import random

# User imports:
from riskboard import RiskBoard
from world import KEY

# Module logger:
logger = logging.getLogger("risk-env")
logger.setLevel(logging.DEBUG)
logging.basicConfig()

# Private variables:
INVALID_ACTION = -1
REWARD_LOSE = -1
REWARD_WIN = 1
MAX_ARMY_NUM = 120

# Classes:

## Class to represent the OpenAI gym environment for the Risk game.
class RiskEnv(gym.Env):

    # Class constructor:
    def __init__(self, opponents, train_freemove=False):

        # Copy the opponent information:
        self.country_list = sorted(list(KEY.values()))
        self.opponents = opponents
        self.opponent_names = list(map(lambda o: o.name, opponents))
        self.player_num = len(opponents) + 1
        self.train_freemove = train_freemove

        # Action space:
        #   Country 1: Used as the argument in the ressuply phase and as the
        # country where the attack originates from in the attack phase.
        #   Country 2: Used as the country to be attacked in the attack phase.
        #   Flag: If 1, end the attack phase.
        self.action_space = spaces.Tuple((
            spaces.Discrete(42),    # Country 1.
            spaces.Discrete(42),    # Country 2.
            spaces.Discrete(2)      # Flag.
        ))

        # Observation state:
        #   Game state: Signal if the game is in the ressuply phase or the
        # attack phase.
        #   Countries: Dictionary for the countries. Keys are the same of the
        # risk game implementation. Each country contains information about the
        # owner of the country (0 is the Agent, others are enemy AIs) and the
        # number of troops in it.
        self.observation_space = spaces.Tuple((
            spaces.Discrete(3),    # Game state.
            # Countries.
            spaces.Dict({
                "a": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "b": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "c": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "d": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "e": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "f": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "g": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "h": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "i": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "j": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "k": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "l": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "m": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "n": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "o": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "p": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "q": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "r": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "s": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "t": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "u": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "v": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "w": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "x": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "y": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "z": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "A": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "B": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "C": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "D": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "E": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "F": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "G": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "H": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "I": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "J": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "K": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "L": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "M": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "N": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "O": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM))),
                "P": spaces.Tuple((spaces.Discrete(self.player_num),
                                   spaces.Discrete(MAX_ARMY_NUM)))
            })
        ))

        # Generate a random seed for the game's logic.
        self.seed()

        # Start the game:
        self.reset()

    # Random seed generator:
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # Reset board method:
    def reset(self):
        # Create a new board for the players:
        self.board = RiskBoard()

        # Add the player information for the agent:
        self.board.addPlayer("Agent", "Agent")

        # Add the player information for the opponents:
        for opponent in self.opponents:
            self.board.addPlayer(opponent.name, opponent.type, opponent.ai)

        # Start the game:
        self.board.start()

        # Set the game phase:
        self.game_phase = 1

        return self._getObs()

    # Learning step method:
    def step(self, action):
        assert self.action_space.contains(action)

        # Set the info return to an empty dictionary (it won't be needed):
        info = dict()

        # This while loop is just to guarantee a better transition between game
        # phases.
        while(True):

            # Initial reinforcement phase:
            if(self.game_phase == 1):

                # Make all the players that aren't the Agent play:
                while((self.board.player.name != "Agent") and
                      (not self.board.finishedInitialPlacement())):
                    self.board.initialPlacement()

                if(not self.board.finishedInitialPlacement()):

                    # Make the Agent play:
                    country = self._actionToCountry(action[0])

                    # Did he play a valid move? If yes:
                    if(self.board.initialPlacement(country) == 0):
                        # If there is another reinforcement to be done, return.
                        # Else, let's wait for the opponents.
                        if(self.board.initial_troops["Agent"] != 0):
                            return (self._getObs(), self._getReward(), False,
                                    info)

                    # If the move was invalid, the game is over:
                    else:
                        self.board.cleanUpBoard()
                        return (self._getObs(), INVALID_ACTION, True, info)

                else:
                    self.game_phase = 2

            # Enemy turn phase:
            if(self.game_phase == 2):

                # Make everybody that is not the Agent play:
                while(self.board.player.name != "Agent"):
                    self.board.fullTurn()   # Have the next player play.

                    # Did this player kill the Agent?
                    if not self._isAgentAlive():
                        self.board.cleanUpBoard()
                        return (self._getObs(), REWARD_LOSE, True, info)

                # If we get here, the agent is still alive and ready to play.
                # But first, we need to show him how the board is looking like:
                self.game_phase = 3     # Agent reinforcement phase.
                self.available_troops = self.board.player.reinforcements

                # Show the Agent the board with the command to reinforce:
                return (self._getObs(), self._getReward(), False, info)

            # Agent reinforcement phase:
            if(self.game_phase == 3):

                # Ok, the Agent gets to reinforce. Use 1 troop!
                country = self._actionToCountry(action[0])

                # Was the reinforcement valid? If yes:
                if(self.board.reinforce(country, 1) == 0):
                    self.available_troops -= 1

                    # If we are out of reinforcements, begin the attack phase!
                    if(self.available_troops == 0):
                        self.game_phase = 4

                    # Return the board state:
                    return (self._getObs(), self._getReward(), False, info)

                # If no:
                else:
                    self.board.cleanUpBoard()
                    return (self._getObs(), INVALID_ACTION, True, info)

            # Agent attack phase:
            if(self.game_phase == 4):

                # Ok, the Agent gets to attack or to pass the turn.
                src = self._actionToCountry(action[0])
                target = self._actionToCountry(action[1])
                stop_flag = True if action[2] == 1 else False

                # Did the Agent stop the attack or run out of troops?
                if(stop_flag):
                    if(self.train_freemove):
                        self.game_phase = 5     # Freemove phase.
                        return (self._getObs(), self._getReward(), False, info)
                    else:
                        self.board.turn += 1    # Pass the turn.
                        self.game_phase = 2     # Opponent's turn phase.
                        # Don't return anything! Wait for the opponents to play!
                        # Here is where the while loop comes in handy!

                # If not, than he must attack:
                else:
                    # If the attack is valid, we have some conditions to check:
                    if(self.board.attack(src, target) == 0):
                        # First, check to see if we won:
                        end_info = self.board.gameEnded()

                        # Agent won:
                        if(end_info[0] == True and end_info[1] == "Agent"):
                            return (self._getObs(), REWARD_WIN, True, info)

                        # Agent didn't win:
                        # (The code should not execute this due to it's logic!)
                        elif(end_info[0] == True):
                            return (self._getObs(), REWARD_LOSE, True, info)

                        # The game is not over, so we should keep playing!

                        # If we cannot attack anymore change the game phase:
                        elif(not self.board.player.canAttack()):
                            if(self.train_freemove):
                                self.game_phase = 5     # Freemove phase.
                                return (self._getObs(), self._getReward(),
                                        False, info)
                            else:
                                self.board.turn += 1    # Pass the turn.
                                self.game_phase = 2     # Opponent's turn phase.
                                # Don't return anything!
                                # Wait for the opponents to play!
                                # Here is where the while loop comes in handy!

                        else:
                            return (self._getObs(), self._getReward(), False,
                                    info)

                    # If the attack is invalid, just return immediately:
                    else:
                        return (self._getObs(), INVALID_ACTION, True, info)

            # Agent freemove phase:
            if(self.game_phase == 5):
                pass
                # TODO Implement this phase... if needed.

    # Private methods:

    ## Translate Agent input:
    def _actionToCountry(self, action):
        return self.country_list[action]

    ## Determine Agent's next action:
    def _gamePhaseCode(self):

        # A little explanation. This method reads the game phase and returns a
        # code based on the action that the Agent should take next.

        # Reinforcement action (initial troops or normal reinforcement):
        if(self.game_phase >= 1 and self.game_phase <= 3):
            return 0

        # Attack action:
        elif self.game_phase == 4:
            return 1

        # Freemove action:
        elif self.game_phase == 5:
            return 2

        # Treat all other possibilities as a reinforcement action:
        else:
            return 0

    ## Read the board:
    def _getObs(self):
        territories = dict()

        for t_key, t_name in KEY.items():
            territory = self.board.world.territories[t_name]
            owner_name = territory.owner.name

            if(owner_name == "Agent"):
                owner_code = 0

            else:
                owner_code = self.opponent_names.index(owner_name) + 1

            territories[t_key] = (owner_code, territory.forces)

        return (self._gamePhaseCode(), territories)

    ## Get the Agent's reward:
    def _getReward(self):
        return (self.board.players["Agent"].territory_count / 42)

    ## Check if the Agent is still alive:
    def _isAgentAlive(self):
        return self.board.players["Agent"].alive

## Class to represent the OpenAI gym environment for the attack scenario in a
## Risk game.
class RiskAttackEnv(RiskEnv):

    # Reset board method:
    def reset(self):
        # Create a new board for the players:
        self.board = RiskBoard()

        # Add the player information for the agent:
        self.board.addPlayer("Agent", "Agent")

        # Add the player information for the opponents:
        for opponent in self.opponents:
            self.board.addPlayer(opponent.name, opponent.type, opponent.ai)

        # Start the game:
        self.board.start()

        # Make all the players do the initial reinforcement:
        while(not self.board.finishedInitialPlacement()):

            # Rule for the players that aren't the Agent:
            if(self.board.player.name != "Agent"):
                self.board.initialPlacement()

            # Rule for the Agent:
            else:
                while(self.board.initial_troops["Agent"] != 0):
                    self.board.initialPlacement(self._borderTerritory());

        # Wait for the Agent's turn:
        while(self.board.player.name != "Agent"):
            self.board.fullTurn()   # Have the next player play.

        # Reinforce for the Agent:
        self.available_troops = self.board.player.reinforcements

        while(self.available_troops != 0):
            self.board.reinforce(self._borderTerritory(), 1)
            self.available_troops -= 1

        # Set the game state to the attack phase:
        self.game_phase = 4

        return self._getObs()

    # Learning step method:
    def step(self, action):
        assert self.action_space.contains(action)

        # Set the info return to an empty dictionary (it won't be needed):
        info = dict()

        # Ok, the Agent gets to attack or to pass the turn.
        src = self._actionToCountry(action[0])
        target = self._actionToCountry(action[1])
        stop_flag = True if action[2] == 1 else False

        # Since this is the AttackEnv, passing the turn is frowned upon:
        if(stop_flag):
            return (self._getObs(), INVALID_ACTION, True, info)

        # If not, than he must attack:
        else:

            # If the attack is valid, we have some conditions to check:
            if(self.board.attack(src, target) == 0):

                # If we cannot attack anymore, the Agent wins this Env:
                if(not self.board.player.canAttack()):
                    return (self._getObs(), REWARD_WIN, True, info)

                # Else, we just reward him adequately:
                else:
                    return (self._getObs(), self._getReward(), False, info)

            # If the attack is invalid, just return immediately:
            else:
                return (self._getObs(), INVALID_ACTION, True, info)

    # Method to return a random territory owned by the Agent that borders an
    # enemy territory:
    def _borderTerritory(self):
        border_options = [t for t in self.board.players["Agent"].territories
                          if t.border]
        return random.choice(border_options)
