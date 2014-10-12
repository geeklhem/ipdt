import ipdt.player

class Player(ipdt.player.Player):
    """Retailator, a strategy that never forgets."""
    name = "Retailator"
    def __init__(self,param):
        self.revenge = False
    def play(self,last_move):
        if last_move is not None and not last_move:
            self.revenge = True

        if self.revenge:
            return False
        else:
            return True
