import ipdt.player

class Player(ipdt.player.Player):
    """Tit-for-Tat, a strategy that is all about equivalent retaliation."""
    name = "Tit-for-tat"
    def play(self,last_move):
        if last_move is None:
            return True
        else:
            if last_move:
                return True
            else:
                return False
