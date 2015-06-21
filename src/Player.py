#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/20/15
#
# Class that defines the common characteristic amongst
# Players. Such as score, update, draw methods and checking
# if the player is currently alive. Super class should be
# called for init and reset.
###########################################################

class Player(object):
    def __init__(self, score=0, alive=True):
        self.score = self.fScore = score
        self.alive = self.fAlive = alive

    def reset(self):
        pass

    def checkAlive(self, *args):
        pass

    def inbounds(self, bounds):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass
