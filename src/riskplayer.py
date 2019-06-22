# Module to represent a Risk player.

# Package imports:
from copy import deepcopy

# Classes:

## Class to store the basic information of a player:
class PlayerInfo(object):

    # Constructor:
    def __init__(self, name, type, ai=None):
        self.name = name
        self.type = type
        self.ai = ai

## Class to store the basic mechanics of a risk player. May be an AI or Agent.
class RiskPlayer(object):

    # Constructor:
    def __init__(self, name, board, type, ai=None):
        self.name = name
        self.world = board.world
        self.type = type
        self.color = 0

        if(type == "AI" and ai != None):
            self.ai = ai(self, board, board.world)

    # Property methods:
    @property
    def territories(self):
        for t in self.world.territories.values():
            if t.owner == self:
                yield t

    @property
    def territory_count(self):
        count = 0
        for t in self.world.territories.values():
            if t.owner == self:
                count += 1
        return count

    @property
    def areas(self):
        for a in self.world.areas.values():
            if a.owner == self:
                yield a

    @property
    def forces(self):
        return sum(t.forces for t in self.territories)

    @property
    def alive(self):
        return self.territory_count > 0

    @property
    def reinforcements(self):
        return max(self.territory_count//3, 3) + sum(a.value for a in self.areas)

    # Methods:
    def canAttack(self):
        for territory in self.territories:
            # If even a single territory has a target on it's border and more
            # than one troop, we can still attack!
            if(territory.forces > 1 and territory.border):
                return True

        # Else, we cannot attack.
        return False

    # Overwriting default object methods:
    def __repr__(self):
        return "P;%s" % (self.name)

    def __hash__(self):
        return hash(("player", self.name))

    def __eq__(self, other):
        if isinstance(other, RiskPlayer):
            return self.name == other.name
        return False

    def __deepcopy__(self, memo):
        newobj = RiskPlayer(self.name, self, lambda *x, **y: None, {})
        newobj.color = self.color
        newobj.world = deepcopy(self.world, memo)
        return newobj
