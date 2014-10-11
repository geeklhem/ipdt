import ipdt.player

class Player(ipdt.player.Player):
    name = "Defector"
    def play(self,last_move):
        return False
