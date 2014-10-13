import ipdt.tournament
import ipdt.player

class Coop(ipdt.player.Player):
    def play(self, last_move):
        return True 
class Defect(ipdt.player.Player):
    def play(self, last_move):
        return False
class Erronous(ipdt.player.Player):
    def play(self, last_move):
        return None
class Erronous2(ipdt.player.Player):
    def play(self, last_move):
        return 34
class Erronous3(ipdt.player.Player):
    def play(self, last_move):
        return ""
class Erronous4(ipdt.player.Player):
    def play(self, last_move):
        print "This function returns nothing"
        pass
class Erronous5(ipdt.player.Player):
    pass
    
F = {}
def setup():
  F["param"] = {
      "T": 100, # Number of iterations
      "cc": 1, # Payoff if I cooperated and the other too
      "cd": -1, # Payoff if I cooperated but the other defected
      "dc": 2, # Payoff if I defected and the other cooperated
      "dd": 0, # Payoff if everyone defected
  }

def test_two_coop():
    po = ipdt.tournament.match(Coop,Coop,F["param"])
    print po
    assert po == [F["param"]["T"]*F["param"]["cc"],F["param"]["T"]*F["param"]["cc"]]

def test_two_defect():
    po = ipdt.tournament.match(Defect,Defect,F["param"])
    print po
    assert po == [F["param"]["T"]*F["param"]["dd"],F["param"]["T"]*F["param"]["dd"]]

def test_coop_defect():
    po = ipdt.tournament.match(Coop,Defect,F["param"])
    print po
    assert po == [F["param"]["T"]*F["param"]["cd"],F["param"]["T"]*F["param"]["dc"]]
    
def test_erronous():
    po = ipdt.tournament.match(Coop,Erronous,F["param"])
    print po
    assert po == [F["param"]["T"]*F["param"]["cd"],F["param"]["T"]*F["param"]["dc"]]

def test_erronous2():
    po = ipdt.tournament.match(Coop,Erronous2,F["param"])
    print po
    assert po == [F["param"]["T"]*F["param"]["cc"],F["param"]["T"]*F["param"]["cc"]]

def test_erronous3():    
    po = ipdt.tournament.match(Coop,Erronous3,F["param"])
    print po
    assert po == [F["param"]["T"]*F["param"]["cd"],F["param"]["T"]*F["param"]["dc"]]

def test_erronous4():
    po = ipdt.tournament.match(Coop,Erronous4,F["param"])
    print po
    assert po == [F["param"]["T"]*F["param"]["cd"],F["param"]["T"]*F["param"]["dc"]]

def test_erronous5():    
    po = ipdt.tournament.match(Coop,Erronous5,F["param"])
    print po
    assert po == [F["param"]["T"]*F["param"]["cd"],F["param"]["T"]*F["param"]["dc"]]


