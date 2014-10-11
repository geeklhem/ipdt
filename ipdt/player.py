""" Player base class"""

class Player(object):
    """ The base class for every player """
    name = "Generic player"
    author = "GT-mathbio"
    def __init__(self, param):
        self.param = param
    def play(self, last_coup):
        pass 
