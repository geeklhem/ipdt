import ipdt.player

class Player(ipdt.player.Player):
    """Pavlovian conditioning: Win stay, loose switch"""
    name = "Pavlov"
    author = "Guilhem Doulcier"
    def __init__(self,param):
        # I win if I play C and the other play self.win[C].
        self.win = {}
        self.win[True] = param["cc"] > param["cd"]
        self.win[False] = param["dc"] > param["dd"]
        
    def play(self, last_move):

        # I start by cooperating
        if last_move == None:
            self.my_move = True

        # If the last move was not wining, I switch
        elif self.win[self.my_move] != last_move:
            self.my_move = not self.my_move 

        return self.my_move
