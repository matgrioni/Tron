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

        self.turning = False

        self.p1 = LineRider(10, 240, Direction.RIGHT)
        self.p2 = LineRider(625, 240, Direction.LEFT)

        # Add the necessary callbacks for the movement
        # of the players.
        self.addEventCallback((KEYDOWN, (K_RIGHT, K_LEFT)), self._dirKeydown)
        self.addEventCallback((KEYUP, (K_RIGHT, K_LEFT)), self._dirKeyup)
        self.addEventCallback((KEYDOWN, K_RIGHT), self._p1TurnRight)
        self.addEventCallback((KEYDOWN, K_LEFT), self._p1TurnLeft)

    # Simply move each player along as needed
    def update(self):
        self.p1.update()
        self.p2.update()

    def draw(self):
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)

    def _p1TurnRight(self, event):
        if not self.turning:
            self.p1.turnRight()

    def _p1TurnLeft(self, event):
        if not self.turning:
            self.p1.turnLeft()

    def _p2TurnRight(self, event):
        if not self.turning:
            self.p2.turnRight()

    def _p2TurnLeft(self, event):
        if not self.turning:
            self.p2.turnRight()

    # These methods are called when a key to turn the line
    # riders are moved, so that we can keep track of each
    # event as it happens. This way the riders don't turn
    # more than once per keypress.
    def _dirKeydown(self, event):
        self.turning = True

    def _dirKeyup(self, event):
        self.turning = False

# If this is the main program, run the game at 60 fps
if __name__ == "__main__":
    g = Game()
    g.execute(40)
