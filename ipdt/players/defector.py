import ipdt.player

class Player(ipdt.player.Player):
    """Defector, a strategy that never cooperates."""
    name = "Defector"
    def play(self,last_move):
        return False
