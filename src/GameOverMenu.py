#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# The menu that pops up once at least one of the players
# dies. Similar to the pause menu however no resume option.
###########################################################

from pydroid import modules, settings, widgets

class GameOverMenu(modules.Menu):
    def __init__(self, parent, fill=(255, 255, 255)):
        super(GameOverMenu, self).__init__(parent, fill)
        self.setOptions(["Next game", "Main menu", "Quit"])

        self.addOptionCallback("Next game", self._startGameOver)
        self.addOptionCallback("Main menu", self.back, count=2)
        self.addOptionCallback("Quit", self.quit)

        self.p1Score = widgets.TextDisp(10, 10)
        self.p1Score.setFont(fontsize=15)
        
        self.p2Score = widgets.TextDisp(self.size[0] - 150, 10)
        self.p2Score.setFont(fontsize=15)

    def setScores(self, scores):
        self.p1Score.setText("Player 1: " + str(scores[0]))
        self.p2Score.setText("Player 2: " + str(scores[1]))

    def draw(self):
        super(GameOverMenu, self).draw()

        self.p1Score.draw(self.screen)
        self.p2Score.draw(self.screen)

    def _startGameOver(self):
        self.parent.reset()
        self.back()
