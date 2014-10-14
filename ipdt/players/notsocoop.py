# -*- coding: utf-8 -*-
from __future__ import division
import ipdt.player

class Player(ipdt.player.Player) :
      """" NotSoCoop" coopère tout le temps sauf à quelques instants où il
      met un 'false' à la place d'un 'True' pour prendre l'avantage.
      """

      name="NotSoCoop"
      author="Marc Oudart"

      def __init__(self, param):
          self.nb_True = 0

      def play(self, last_move):
      	  if last_move == None : 
	     self.nb_True += 1
             return True
          elif last_move == False:
	     return False
	  elif self.nb_True < 5:
             self.nb_True += 1
	     return True
          else :
             self.nb_True = 0
             return False
