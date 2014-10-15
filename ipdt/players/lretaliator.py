import ipdt.player
import random

class Player(ipdt.player.Player):
    """Leniant Retaliator, a strategy that almost never forgets (twice).

    Just like the retaliator but:
    - It takes two round of consecutive defection to start the revenge mode.
    - There is a really small probability (10^-5 by revenge round) to forgive.
    """
    
    name = "Lenient Retaliator"
    author = "Guilhem Doulcier"
    def __init__(self,param):
        self.revenge = False
        self.before_last_move = True
    def play(self,last_move):
        if (last_move is not None
            and not last_move
            and not self.before_last_move
        ):
            self.revenge = True
        self.before_last_move = last_move
        if self.revenge:
            if random.random() < 1e-5:
                self.revenge = False
            return False
        else:
            return True
