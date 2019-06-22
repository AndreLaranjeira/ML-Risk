# Module to represent the Risk game board.

# Package imports:
import logging
import random

# User imports:
from riskplayer import RiskPlayer
from territory import World
from world import CONNECT, AREAS

# Module logger:
logger = logging.getLogger("risk-board")
logger.setLevel(logging.DEBUG)
logging.basicConfig()

# Classes:

## Class to store the basic mechanics of a Risk game board.
class RiskBoard(object):

    def __init__(self):

        # Initialize world:
        self.world = World()
        self.world.load(AREAS, CONNECT)

        # Initialize player list:
        self.players = {}
        self.next_color = 1;

        # Initialize turn information:
        self.turn = 0

    # Method to add players to the board:
    def addPlayer(self, name, type, ai=None):
        assert name not in self.players
        new_player = RiskPlayer(name, self, type, ai)
        self.players[name] = new_player;
        self.players[name].color = self.next_color;
        self.next_color += 1;
        if(type == "AI"):
            self.players[name].ai.start()

    # Method to start the game board distribution once the players have been
    # added.
    def start(self):
        assert 2 <= len(self.players) <= 5  # Limit player count.
        self.turn_order = list(self.players)
        random.shuffle(self.turn_order)     # Change this to use seed?

        # Distribute territories between players:
        territories = list(self.world.territories.values())
        random.shuffle(territories)
        initial_troops_count = 35 - 2*len(self.players)
        self.initial_troops = {p: initial_troops_count for p in self.players}

        while territories:
            t = territories.pop()
            t.forces += 1
            self.initial_troops[self.player.name] -= 1
            t.owner = self.player
            self.info("Dealt player %s territory %s", self.player.name, t.name)
            self.turn += 1

        self.info("Board succesfully started!")

        # Now the board is all set for the game to start.
        # Remember, the game start with players choosing where to place their
        # remaining initial troops!

    # Properties:

    ## Property that returns the player whose turn is next.
    @property
    def player(self):
        return self.players[self.turn_order[self.turn % len(self.players)]]

    # General game methods:

    ## Attack method:
    def attack(self, src, target, f_atk=None, f_move=None):

        # Check to see if the attack is valid:
        if src is None:
            self.warn("Attack invalid src %s", src)
            return -1
        if target is None:
            self.warn("Attack invalid target %s", target)
            return -1
        if src.owner != self.player:
            self.warn("Attack unowned src %s", src.name)
            return -1
        if target.owner == self.player:
            self.warn("Attack owned target %s", target.name)
            return -1
        if target not in src.connect:
            self.warn("Attack unconnected %s %s", src.name, target.name)
            return -1
        if src.forces == 1:
            self.warn("Not enought troops to attack from source %s", src.name)
            return -1

        # The attack seems valid, so we store the opponent's name...
        opponent = target.owner.name

        # ... and simulate the actual combat.
        victory = self.combat(src, target, f_atk, f_move)

        # Log the outcome of the attack:
        if(victory):
            self.info("%s conquered %s from %s", self.player.name, target.name,
                      opponent)
        else:
            self.info("%s defended %s from %s", opponent, target.name,
                      self.player.name)

        return 0;

    ## Method to clean up board:
    def cleanUpBoard(self):
        for p in self.players.values():
            if p.type == "AI":
                p.ai.end()

    ## Combat method:
    def combat(self, src, target, f_atk=None, f_move=None):
        n_atk = src.forces
        n_def = target.forces

        if f_atk is None:
            f_atk = lambda a, d: True
        if f_move is None:
            f_move = lambda a: a - 1

        while n_atk > 1 and n_def > 0 and f_atk(n_atk, n_def):
            atk_dice = min(n_atk - 1, 3)
            atk_roll = sorted([random.randint(1, 6) for i in range(atk_dice)], reverse=True)
            def_dice = min(n_def, 2)
            def_roll = sorted([random.randint(1, 6) for i in range(def_dice)], reverse=True)

            for a, d in zip(atk_roll, def_roll):
                if a > d:
                    n_def -= 1
                else:
                    n_atk -= 1

        if n_def == 0:
            move = f_move(n_atk)
            min_move = min(n_atk - 1, 3)
            max_move = n_atk - 1
            if move < min_move:
                self.warn("Combat invalid move request %s (%s-%s)", move, min_move, max_move)
                move = min_move
            if move > max_move:
                self.warn("Combat invalid move request %s (%s-%s)", move, min_move, max_move)
                move = max_move
            src.forces = n_atk - move
            target.forces = move
            target.owner = src.owner
            return True

        else:
            src.forces = n_atk
            target.forces = n_def
            return False

    ## Method to show if the initial placement ended:
    def finishedInitialPlacement(self):
        return sum(self.initial_troops.values()) == 0

    ## Method to freemove:
    def freemove(self, src, target, count):

        # Check to see if the freemove is valid:
        if src is None:
            self.warn("Freemove invalid src %s", src)
            return -1
        if target is None:
            self.warn("Freemove invalid target %s", target)
            return -1
        if src.owner != self.player:
            self.warn("Freemove unowned src %s", src.name)
            return -1
        if target.owner != self.player:
            self.warn("Freemove unowned target %s", target.name)
            return -1
        if not 0 <= count < src.forces:
            self.warn("Freemove invalid count %s", f)
            return -1

        src.forces -= count
        target.forces += count
        self.info("%s moved %s troops from %s to %s", self.player.name, count,
                  src.name, target.name)

        return 0

    ## Method to simulate a full turn:
    def fullTurn(self):
        # Check to see if the current player is alive:
        if self.player.alive:
            # Check to see if it is an AI:
            if self.player.type == "AI":

                # Reinforcement phase:
                choices = self.player.ai.reinforce(self.player.reinforcements)
                assert sum(choices.values()) == self.player.reinforcements
                for territory, forces in choices.items():
                    self.reinforce(territory, int(forces))

                # Combat phase:
                for src, target, f_attack, f_move in self.player.ai.attack():
                    self.attack(self.world.territory(src),
                                self.world.territory(target),
                                f_attack,
                                f_move)

                # Freemove phase:
                freemove_input = self.player.ai.freemove()

                if freemove_input:
                    src, target, count = freemove_input
                    self.freemove(self.world.territory(src),
                                  self.world.territory(target),
                                  int(count))


        # End the turn:
        self.turn += 1

    ## Method to check if the game has ended:
    def gameEnded(self):
        players_alive = [p for p in self.players.values() if p.alive]

        if len(players_alive) == 1:
            winner_name = players_alive[0].name
            self.info("Player %s won the game!", winner_name)
            self.cleanUpBoard()
            return (True, winner_name)

        else:
            return (False, None)

    ## Initial placement method:
    def initialPlacement(self, input=None):
        if self.finishedInitialPlacement():
            return 0

        else:
            if self.initial_troops[self.player.name] > 0:
                if(self.player.type == "AI"):
                    choice = self.player.ai.initial_placement(None,
                             self.initial_troops[self.player.name])

                elif input != None:
                    choice = input

                else:
                    self.warn("No initial place input")
                    return -1

                error = self.reinforce(choice, 1)

                if(error == 0):
                    self.initial_troops[self.player.name] -= 1

                self.turn += 1

                return 0 if not error else -1

    ## Reinforce method:
    def reinforce(self, choice, number):
        t = self.world.territory(choice)

        if t is None:
            self.warn("Initial invalid territory %s", choice)
            return -1
        elif t.owner != self.player:
            self.warn("Initial unowned territory %s", t.name)
            return -1
        elif number < 0:
            self.warn("Reinforce invalid count %s", number)
            return -1
        else:
            t.forces += number
            self.info("%s reinforced %s", self.player.name, t.name)
            return 0

    # Logger methods:
    def info(self, *args):
        logger.info(*args)

    def warn(self, *args):
        logger.warn(*args)
