#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# The menu that pops up once at least one of the players
# dies. Similar to the pause menu however no resume option.
###########################################################

import widgets

class GameOverMenu(widgets.Menu):
    def __init__(self, scores, parent=None, size=(640, 480),
                 fill=(255, 255, 255)):
        options = ["Next game", "Main menu", "Quit"]
        super(GameOverMenu, self).__init__(options, parent, size, fill)

        self.addOptionCallback("Next game", self._startGameOver)
        self.addOptionCallback("Main menu", self.back, count=2)
        self.addOptionCallback("Quit", self.quit)

        self.p1Score = widgets.TextDisp(10, 10, "Player 1: " + str(scores[0]),
                                        fontsize=15)
        self.p2Score = widgets.TextDisp(self.size[0] - 150, 10,
                                        "Player 2: " + str(scores[1]),
                                        fontsize=15)

    def draw(self):
        super(GameOverMenu, self).draw()

        self.p1Score.draw(self.screen)
        self.p2Score.draw(self.screen)

    def _startGameOver(self):
        self.parent.reset()
        self.back()
