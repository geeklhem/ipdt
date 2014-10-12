import ipdt.player

class Player(ipdt.player.Player):
    """ Naive cooperator, a strategy that think everyone is nice. """
    name = "Naive cooperator"

    def __init__(self,param):
        """
        Use this function to set up match wise attributes.

        Args:
            param (dict): the match parameters.
        """
        pass 

    def play(self, last_move):
        """
        Use this function to choose your action each turn.

        Args:
            last_move (boolean): Your oponent last move `True` for cooperation,
                `False` for defection and `None` in the first round.
        Return: 
            (boolean): Your move (same convention).
        """  
        return True 
