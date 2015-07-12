#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/18/15
#
# Defines the pause menu for the Game using the Menu
# library.
###########################################################

from pydroid import modules, widgets

class PauseMenu(modules.Menu):
    def __init__(self, parent, fill=(255, 255, 255)):
        super(PauseMenu, self).__init__(parent, fill)
        self.setOptions(["Resume", "Start over", "Main menu", "Quit"])

        self.addOptionCallback("Resume", self._resumeGame)
        self.addOptionCallback("Start over", self._startGameOver)
        self.addOptionCallback("Main menu", self.back, count=2)
        self.addOptionCallback("Quit", self.quit)

        # Create the TextDisp objects but don't put in any text yet
        self.p1Score = widgets.TextDisp(10, 10)
        self.p1Score.setFont(fontsize=15)

        self.p2Score = widgets.TextDisp(self.size[0] - 150, 10)
        self.p2Score.setFont(fontsize=15)

    # Set the text for the scores in the two corners.
    def setScores(self, p1Score, p2Score):
        self.p1Score.setText("Player 1: " + str(p1Score))
        self.p2Score.setText("Player 2: " + str(p2Score))

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
