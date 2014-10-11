import ipdt.player

class Player(ipdt.player.Player):
    name = "Naive cooperator"
    def play(self, last_move):
        return True 
