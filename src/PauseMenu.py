#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/18/15
#
# Defines the pause menu for the Game using the Menu
# library.
###########################################################

from widgets import Menu, TextDisp

class PauseMenu(Menu):
    def __init__(self, scores, parent=None, size=(640, 480), fill=(255, 255, 255)):
        options = ["Resume", "Start over", "Main menu", "Quit"]
        super(PauseMenu, self).__init__(options, parent, size, fill)

        self.addOptionCallback("Resume", self._resumeGame)
        self.addOptionCallback("Start over", self._startGameOver)
        self.addOptionCallback("Main menu", self.back, count=2)
        self.addOptionCallback("Quit", self.quit)

        self.p1Score = TextDisp(10, 10, "Player 1: " + str(scores[0]), fontsize=15)
        self.p2Score = TextDisp(self.size[0] - 150, 10,
                                "Player 2: " + str(scores[1]), fontsize=15)

    def draw(self):
        super(PauseMenu, self).draw()

        self.p1Score.draw(self.screen)
        self.p2Score.draw(self.screen)

    def _resumeGame(self):
        self.parent.resetTimer()
        self.back()

    def _startGameOver(self):
        self.parent.reset()
        self.back()
