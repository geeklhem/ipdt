import ipdt.player
from random import random

class Player(ipdt.player.Player):
    name = "Random player"
    def play(self, last_move):
        return random()>0.5
