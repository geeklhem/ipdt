""" Player base class"""

class Player(object):
    """The base class for every player. You have to create a class
    inheriting it to define your own strategy.

    The name and author class attributes are used in the different
    output of the program.
    """
    name = "Generic player"
    author = "GT-mathbio"
    
    def __init__(self, param):
        """
        Use this function to set up match wise attributes.
        Args:
            param (dict): the match parameters.
        """
        self.param = param
        
    def play(self, last_move):
        """
        Use this function to choose your action each turn.
        
        Args:
            last_move (boolean): Your oponent last move `True` for cooperation,
                `False` for defection and `None` in the first round.
        Return: 
            (boolean): Your move (same convention)
        """
        pass 
