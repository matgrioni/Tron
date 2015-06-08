#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/6/15
#
# Main Game class definition and execution. The class
# extends PygameHelper and update, draw, etc are overriden
# and defined for this specific Tron game.
##########################################################

from pygame.locals import *
from PygameHelper import PygameHelper
from LineRider import Direction, LineRider

class Game(PygameHelper):
    def __init__(self, size=(640, 480)):
        super(Game, self).__init__(size)

        self.p1 = LineRider(300, 200, Direction.RIGHT)
        self.p2 = LineRider(400, 200, Direction.LEFT)

        # Add the necessary callbacks for the movement
        # of the players.
        #self.addEventCallback((KEYDOWN, K_RIGHT), self._p1TurnRight())
        #self.addEventCallback((KEYDOWN, K_LEFT), self._p1TurnLeft())

    # Simply move each player along as needed
    def update(self):
        self.p1.update()
        self.p2.update()

    def draw(self):
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)

    def _p1TurnRight(self, event):
        pass

    def _p1TurnLeft(self, event):
        pass

    def _p2TurnRight(self, event):
        pass

    def _p2TurnLeft(self, event):
        pass

# If this is the main program, run the game at 60 fps
if __name__ == "__main__":
    g = Game()
    g.execute(60)
