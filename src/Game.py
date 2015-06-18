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

# The current 
class GameState(object):
    PLAYING, PAUSE, GAMEOVER = range(3)

class Game(PygameHelper):
    def __init__(self, parent=None, size=(640, 480), fill=(0, 0, 0)):
        super(Game, self).__init__(parent, size, fill)

        self.gameState = GameState.PLAYING

        self.p1 = LineRider(10, size[1] / 2, Direction.RIGHT, color=(50, 200, 12))
        self.p2 = LineRider(size[0] - 15, size[1] / 2, Direction.LEFT)

        self.alive = {self.p1: 1, self.p2: 1}

        # Add callbacks for moving the players.
        self.addEventCallback((KEYDOWN, (K_RIGHT, K_LEFT)), self._p1DirKeydown)
        self.addEventCallback((KEYUP, (K_RIGHT, K_LEFT)), self._p1DirKeyup)

        self.addEventCallback((KEYDOWN, (K_a, K_d)), self._p2DirKeydown)
        self.addEventCallback((KEYUP, (K_a, K_d)), self._p2DirKeyup)

    # Simply move each player along as needed
    def update(self):
        if self.gameState == GameState.PLAYING:
            self.p1.update()
            self.p2.update()

            bounds = (0, 0, self.size[0], self.size[1])

            self.alive[self.p1] = not self.p1.collides(self.p2) and \
                                      self.p1.inbounds(bounds) and \
                                      not self.p1.overlap()
            self.alive[self.p2] = not self.p2.collides(self.p1) and \
                                      self.p2.inbounds(bounds) and \
                                      not self.p2.overlap()

    def draw(self):
        # Keep drawing the players so that the menu is more
        # like a translucent overlay
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)

        if self.alive[self.p1] == 0 or self.alive[self.p2] == 0:
            self.gameState = GameState.GAMEOVER

    def _p1DirKeydown(self, event):
        if event.key == K_RIGHT:
            self.p1.turnRight()
        elif event.key == K_LEFT:
            self.p1.turnLeft()

        self.p1.turnable = False

    def _p1DirKeyup(self, event):
        self.p1.turnable = True

    def _p2DirKeydown(self, event):
        if event.key == K_d:
            self.p2.turnRight()
        elif event.key == K_a:
            self.p2.turnLeft()

    def _p2DirKeyup(self, event):
        self.p2.turnable = True
