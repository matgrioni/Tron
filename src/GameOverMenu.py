#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# The menu that pops up once at least one of the players
# dies. Similar to the pause menu however no resume option.
###########################################################

from pydroid import modules, settings, views

class GameOverMenu(modules.Module):
    def __init__(self, parent):
        super(GameOverMenu, self).__init__(parent, (255, 255, 255))

        # Create the children views
        self._initMenu()
        self._initScores()

        # Then create the container for them, set this container as the
        # view of this module.
        container = views.ViewGroup(self, (0, 0), self.size)
        container.children.append(self.menu)
        container.children.append(self.p1Score)
        container.children.append(self.p2Score)

        self.setView(container)

    # Create the menu child view.
    def _initMenu(self):
        self.menu = views.Menu(self, (0, 100), self.size)
        self.menu.setOptions(["Next game", "Main menu", "Quit"])

        self.menu.addOptionCallback("Next game", self.back)
        self.menu.addOptionCallback("Main menu", self.back, count=2)
        self.menu.addOptionCallback("Quit", self.quit)

    # Create the score children views in the top left and right corners.
    def _initScores(self):
        self.p1Score = views.TextDisp(self, (10, 10))
        self.p1Score.setFont(fontsize=15)
        
        self.p2Score = views.TextDisp(self, (self.size[0] - 150, 10))
        self.p2Score.setFont(fontsize=15)

    # Set the score text for the views here.
    def setScores(self, scores):
        self.p1Score.setText("Player 1: " + str(scores[0]))
        self.p2Score.setText("Player 2: " + str(scores[1]))
