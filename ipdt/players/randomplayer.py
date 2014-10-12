import ipdt.player
from random import random

class Player(ipdt.player.Player):
    """Random player, a strategy that has no idea of what it is doing."""
    name = "Random player"
    def play(self, last_move):
        return random()>0.5
