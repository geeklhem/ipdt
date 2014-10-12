import ipdt.player

class Player(ipdt.player.Player):
    """Tit-for-two-tats, a strategy of equivalent retaliation that can let it slide."""
    name = "Tit-for-two-tats"
    def __init__(self,param):
        self.before_last_move = None
    def play(self,last_move):
        
        if last_move is None or self.before_last_move is None:
            return True
        else:
            if not last_move and not self.before_last_move:
                return False
            else:
                return True
        self.before_last_move = last_move
