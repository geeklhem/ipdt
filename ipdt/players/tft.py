import ipdt.player

class Player(ipdt.player.Player):
    name = "Tit-for-tat"
    def play(self,last_move):
        if last_move is None:
            return True
        else:
            if last_move:
                return True
            else:
                return False
