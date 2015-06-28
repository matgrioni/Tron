#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/6/15
#
# Main Game class definition and execution. The class
# extends Module and update, draw, etc are overriden
# and defined for this specific Tron game.
##########################################################

import pygame

import widgets
from pygame.locals import *
from LineRider import Direction, LineRider
from PauseMenu import PauseMenu
from GameOverMenu import GameOverMenu

# The current state of the game as an enum
class GameState(object):
    PLAYING, PAUSE, GAMEOVER, TIMER = range(4)

class Game(widgets.Module):
    def __init__(self, parent=None, size=(640, 480), fill=(255, 255, 255)):
        bgColor = widgets.Setting.attr("bg", str(fill))
        self._initBackground()

        super(Game, self).__init__(parent, size, self.bgColor)

        self.gameState = GameState.TIMER
        self.timer = 3
        self.millis = 1000
        self.timerDisp = widgets.TextDisp(self.size[0] / 2,
                                          self.size[1] / 2, str(self.timer))

        self._initPlayers()

        # Add callbacks for moving the players.
        self.addEventCallback((KEYDOWN, (K_RIGHT, K_LEFT)), self._p1DirKeydown)
        self.addEventCallback((KEYUP, (K_RIGHT, K_LEFT)), self._p1DirKeyup)

        self.addEventCallback((KEYDOWN, (K_a, K_d)), self._p2DirKeydown)
        self.addEventCallback((KEYUP, (K_a, K_d)), self._p2DirKeyup)

        self.addEventCallback((KEYDOWN, K_SPACE), self._pauseMenu)

    def _initBackground(self):
        bgColorStr = widgets.Setting.attr("bg", "(255, 255, 255)")
        bgChannels = [int(i) for i in bgColorStr.strip()[1:-1].split(",")]

        self.bgColor = tuple(bgChannels)

    def _initPlayers(self):
        p1ColorStr = widgets.Setting.attr("p1", "(50, 100, 12)")
        p2ColorStr = widgets.Setting.attr("p2", "(0, 0, 0)")

        p1Channels = [int(i) for i in p1ColorStr.strip()[1:-1].split(",")]
        p2Channels = [int(i) for i in p2ColorStr.strip()[1:-1].split(",")]

        p1Color, p2Color = tuple(p1Channels), tuple(p2Channels)

        self.p1 = LineRider(10, self.size[1] / 2,
                            Direction.RIGHT, color=p1Color)
        self.p2 = LineRider(self.size[0] - 15, self.size[1] / 2,
                            Direction.LEFT, color=p2Color)

        self.p1Score = widgets.TextDisp(10, 10, "0")
        self.p2Score = widgets.TextDisp(self.size[0] - 20, 10, "0")

    def reset(self):
        self.p1.reset()
        self.p2.reset()

        self.resetTimer()

    def resetTimer(self):
        self.gameState = GameState.TIMER
        self.timer = 3
        self.millis = 1000
        self.timerDisp.text = str(self.timer)

    # Simply move each player along as needed
    def update(self):
        if self.gameState == GameState.TIMER:
            self.timerDisp.text = str(self.timer)
            self.timer -= 1

            if self.timer < 0:
                self.gameState = GameState.PLAYING
                self.millis = 0
        elif self.gameState == GameState.PLAYING:
            self.p1.update()
            self.p2.update()

            bounds = (0, 0, self.size[0], self.size[1])

            alive = (self.p1.checkAlive(self.p2, bounds),
                     self.p2.checkAlive(self.p1, bounds))

            if not (alive[0] and alive[1]):
                if not alive[0]:
                    self.gameState = GameState.GAMEOVER
                    self.p2.score += 1
                    self.p2Score.text = str(self.p2.score)

                if not alive[1]:
                    self.gameState = GameState.GAMEOVER
                    self.p1.score += 1
                    self.p1Score.text = str(self.p1.score)

                gameOver = GameOverMenu([self.p1.score, self.p2.score],
                                        parent=self)
                gameOver.execute(self.fps)

    def draw(self):
        self.screen.fill(self.fill)

        self.p1Score.draw(self.screen)
        self.p2Score.draw(self.screen)

        # Keep drawing the players so that the menu is more
        # like a translucent overlay
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)

        if self.gameState == GameState.TIMER:
            self.timerDisp.draw(self.screen)

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

    # Create the pause menu with the current game screen as
    # the parent.
    def _pauseMenu(self, event):
        pauseMenu = PauseMenu([self.p1.score, self.p2.score], self,
                              fill=(255, 255, 255))
        pauseMenu.execute(self.fps)
