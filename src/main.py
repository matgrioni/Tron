#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/6/15
#
# Main Game class definition and execution. The class
# extends PygameHelper and update, draw, etc are overriden
# and defined for this specific Tron game.
##########################################################

from PygameHelper import PygameHelper

class Game(PygameHelper):
    def __init__(self, size=(640, 480)):
        super(Game, self).__init__(size)

if __name__ == "__main__":
    g = Game()
    g.execute()
