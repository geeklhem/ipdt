# -*- coding: utf-8 -*-
from __future__ import division
import ipdt.player
from random import random

class Player(ipdt.player.Player):

    """Elle prétend voir l'avenir, mais en réalité elle ne fait qu'utiliser
    des fréquences pour estimer des probabilités et appeler ça Bayésien pour
    faire classe. Au final, elle se plante quand même pas mal, mais vu que
    quand elle se plante pas les gens crient au miracle, elle s'en fout un peu."""

    name = "Bayesian Pythia"
    author = "François Bienvenu"

    # REMARQUE : cette Pythie avait initialement été implémentée avec plus de
    # mémoire (mémoire sur trois tours), mais cela ne changeait rien sur des
    # petites parties, et il fallait faire un truc compliqué pour bien
    # exploiter l'information au début de la partie. Alors tant pis.

    def __init__(self, params):
        self.mem = [(1, 2)] * 16
        self.last_doublet = [(None, None)] * 2
        self.my_last_move = None

    def id_doublet(self, doublet) :
        """An injective function from the set of doublets to [|0, 15|]. Returns
        None when the doublet is incomplete (i.e. contains a None value)."""
        try :
            def symbol(couple) :
                def aux_symbol(v) :
                    if v == None :
                        raise ValueError("Incomplete doublet")
                    elif True :
                        return "1"
                    else :
                        return "0"
                (v1, v2) = couple
                return aux_symbol(v1) + aux_symbol(v2)
            return int("".join(map(symbol, doublet)), 2)
        except ValueError : 
            return None

    def update_proportions(self, last_move) :
        """Updates the array of (cooperative actions, total rounds) following
        each doublet. Last move should be either True or False, not None."""
        i = self.id_doublet(self.last_doublet)
        if i != None :
            (nb_coop, nb_tot) = self.mem[i]
            if last_move :
                self.mem[i] = (nb_coop + 1, nb_tot + 1)
            else :
                self.mem[i] = (nb_coop, nb_tot + 1)

    def store_incoming_info(self, last_move) :
        """Updates the doublet of last three actions."""
        self.last_doublet.append((self.my_last_move, last_move))
        del self.last_doublet[0]

    def get_coop_proba(self, doublet) :
        """AWESOME PROBABILISTIC WIZARDRY !!! #Bayesian #AmazingScience"""
        i = self.id_doublet(doublet)
        if i != None :
            nb_coop, tot = self.mem[i]
            return nb_coop / tot
        else :
            return 0.5

    def play(self, last_move):
        """If you think he's gonna defect, defect. If you're pretty sure he's
        gonna cooperate and that you can defect without consequences, do it.
        When in doubt, be nice."""
        if last_move == None :
            self.my_last_move = True
        else :
            self.update_proportions(last_move) # warning : must precede store
            self.store_incoming_info(last_move)
            p = self.get_coop_proba(self.last_doublet)
            if p > 0.9 :
                  # He is going to cooperate. What is he going to do next if
                  # you defect ?
                  putative_next = self.last_doublet[1:] + [(False, True)]
                  next_p = self.get_coop_proba(putative_next)
                  if next_p > 0.9 :
                      # If he keeps cooperating, defect ! Ah ah !
                      self.my_last_move = False
                  elif nex_p > 0.4 :
                      # If you don't know him yet, get to know him...
                      self.my_last_move = (random() < 0.5)
                  else :
                      # If he defects, then don't defect, keep cooperating.
                      self.my_last_move = True
            elif p < 0.25 :
                # He might defect ! Defect !
                self.my_last_move = False
            else :
                self.my_last_move = True
        return self.my_last_move
