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
from PauseMenu import PauseMenu

# The current state of the game as an enum
class GameState(object):
    PLAYING, PAUSE, GAMEOVER = range(3)

class Game(PygameHelper):
    def __init__(self, parent=None, size=(640, 480), fill=(255, 255, 255)):
        super(Game, self).__init__(parent, size, fill)

        self.gameState = GameState.PLAYING

        self.p1 = LineRider(10, size[1] / 2, Direction.RIGHT, color=(50, 200, 12))
        self.p2 = LineRider(size[0] - 15, size[1] / 2, Direction.LEFT)

        # Add callbacks for moving the players.
        self.addEventCallback((KEYDOWN, (K_RIGHT, K_LEFT)), self._p1DirKeydown)
        self.addEventCallback((KEYUP, (K_RIGHT, K_LEFT)), self._p1DirKeyup)

        self.addEventCallback((KEYDOWN, (K_a, K_d)), self._p2DirKeydown)
        self.addEventCallback((KEYUP, (K_a, K_d)), self._p2DirKeyup)

        self.addEventCallback((KEYDOWN, K_SPACE), self._pauseMenu)

    def reset(self):
        self.p1.reset()
        self.p2.reset()

        self.gameState = GameState.PLAYING

    # Simply move each player along as needed
    def update(self):
        if self.gameState == GameState.PLAYING:
            self.p1.update()
            self.p2.update()

            bounds = (0, 0, self.size[0], self.size[1])

            if not self.p1.checkAlive(self.p2, bounds):
                self.gameState = GameState.GAMEOVER
                self.p2.score += 1

            if not self.p2.checkAlive(self.p1, bounds):
                self.gameState = GameState.GAMEOVER
                self.p1.score += 1

    def draw(self):
        # Keep drawing the players so that the menu is more
        # like a translucent overlay
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)

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

    # Create the pause menu with the current game screen as
    # the parent.
    def _pauseMenu(self, event):
        pauseMenu = PauseMenu(self)
        pauseMenu.execute(self.fps)
