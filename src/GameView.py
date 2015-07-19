#!/usr/bin/python

######################################################################
# Author: Matias Grioni
# Created: 6/6/15
#
# The actual game view. The game loop consists of updating the players
# locations, and handling event inputs such as the arrow keys. When
# a player dies, a callback can be set to be called so that any action
# that is necessary can be taken.
#
# The class is a viewgroup that has the scores, and timer as children
# view. The players are drawn in the draw method of the viewgroup.
######################################################################

import pygame

from pydroid import modules, views, settings

from pygame.locals import *
from LineRider import Direction, LineRider
from PauseMenu import PauseMenu
from GameOverMenu import GameOverMenu

######################################################################
# Author: Matias Grioni
# Created: 7/19/15
#
# Handles the different states of the game.
#
# The playing state means that the update loop is updating the
# positions of players and accepting input and handling events.
#
# Timer means that there was some interrupt in game play, and that a
# countdown timer should be used before play is resumed. The only
# thing that is really done when it is encountered is timer.execute()
######################################################################
class GameState(object):
    TIMER, PLAYING = range(2)

class GameView(views.ViewGroup):
    def __init__(self, module):
        # Make the game fullscreen
        super(GameView, self).__init__(module, (0, 0), module.size)

        # Start the game by displaying a timer.
        self.gameState = GameState.TIMER

        # Setup the children views for this viewgroup
        self.p1Score = views.TextDisp(module, (10, 10), "0")
        self.p2Score = views.TextDisp(module, (self.size[0] - 20, 10), "0")
        self.timer = views.Timer(module, (self.size[0] / 2, self.size[1] / 2))
        self.timer.setTimer(3)

        self.children.append(self.p1Score)
        self.children.append(self.p2Score)

        self._initPlayers()
        self._initEventCallbacks()

    # Setup the players with the saved colors and also setup the views that
    # display the appropriate scores in the corner.
    def _initPlayers(self):
        # Load the tuple for the color as a string.
        p1ColorStr = settings.Settings.load("p1", "(50, 100, 12)")
        p2ColorStr = settings.Settings.load("p2", "(0, 0, 0)")

        # Convert the string to a list using split and convert each channel
        # to an int.
        p1Channels = [int(i) for i in p1ColorStr.strip()[1:-1].split(",")]
        p2Channels = [int(i) for i in p2ColorStr.strip()[1:-1].split(",")]

        # Then setup the colors
        p1Color, p2Color = tuple(p1Channels), tuple(p2Channels)
        self.p1 = LineRider(10, self.size[1] / 2,
                            Direction.RIGHT, color=p1Color)
        self.p2 = LineRider(self.size[0] - 15, self.size[1] / 2,
                            Direction.LEFT, color=p2Color)

    # Set up the callbacks for this view. Such as the arrows to move the player
    # space to pause the game, etc.
    def _initEventCallbacks(self):
        # Add callbacks for moving the player 1 and player 2 respetively.
        self.addEventCallback((KEYDOWN, (K_RIGHT, K_LEFT)), self._p1DirKeydown)
        self.addEventCallback((KEYUP, (K_RIGHT, K_LEFT)), self._p1DirKeyup)

        self.addEventCallback((KEYDOWN, (K_a, K_d)), self._p2DirKeydown)
        self.addEventCallback((KEYUP, (K_a, K_d)), self._p2DirKeyup)

        self.addEventCallback((KEYDOWN, K_SPACE), self._pause)

    # Resets the game to its initial state. (ie. before any update calls)
    def reset(self):
        self.p1.reset()
        self.p2.reset()

        self.gameState = GameState.TIMER

    # Simply move each player along as needed or update the timer depending
    # on the current game mode.
    def update(self):
        if self.gameState == GameState.TIMER:
            self.timer.execute()
            self.gameState = GameState.PLAYING
        elif self.gameState == GameState.PLAYING:
            self.p1.update()
            self.p2.update()

            # Bounds of the screen
            bounds = (0, 0, self.size[0], self.size[1])

            alive = (self.p1.checkAlive(self.p2, bounds),
                     self.p2.checkAlive(self.p1, bounds))

            # If at least one of the players is not alive, then check which
            # ones. Increment the scores of the players and then create
            # the GameOverMenu.
            if False in alive:
                if not alive[0]:
                    self.p2.score += 1
                    self.p2Score.setText(str(self.p2.score))

                if not alive[1]:
                    self.p1.score += 1
                    self.p1Score.setText(str(self.p1.score))

                # This will automatically restart the game once the update
                # loop is reached again.
                self.reset()

                gameOverMenu = GameOverMenu(self.module)
                gameOverMenu.setScores([self.p1.score, self.p2.score])
                gameOverMenu.execute()

    def draw(self):
        super(GameView, self).draw()

        # Keep drawing the players so that the menu is more
        # like a translucent overlay
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)

    def _pause(self, e):
        # Once the update loop is reached again start a timer
        self.gameState = GameState.TIMER

        pauseMenu = PauseMenu(self.module)
        pauseMenu.setScores([self.p1.score, self.p2.score])
        pauseMenu.execute()

    # Methods to control the movement of the players based
    # on the respective binded key presses.
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
