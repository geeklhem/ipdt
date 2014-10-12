# -*- coding: utf-8 -*-
from __future__ import division
import ipdt.player
from random import random

class Player(ipdt.player.Player):

    """Il est dur, mais juste. Rationnel, mais imprévisible.
    Le juge Bao a décidé de coopérer avec ceux qui veulent coopérer mais de ne
    pas se laisser emmerder par les autres."""

    name = "Le juge Bao"
    author = "François Bienvenu"

    def __init__(self, param):
        self.p = 0.5
        self.n = 2

    def play(self, last_move):
        if last_move == None :
            return True
        elif last_move == True :
            self.p = (self.p * self.n + 1) / (self.n + 1)
        else :
            self.p = self.p * self.n / (self.n + 1)
        self.n += 1
        return random() < self.p
