#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/18/15
#
# Defines the pause menu for the Game using the Menu
# library.
###########################################################

from pydroid import modules, views

class PauseMenu(modules.Module):
    def __init__(self, parent):
        super(PauseMenu, self).__init__(parent, (255, 255, 255), parent.size)

        self._initMenu()
        self._initScores()

        # Now add the children view to a viewgroup container
        container = views.ViewGroup(self, (0, 0), self.size)
        container.children.append(self.menu)
        container.children.append(self.p1Score)
        container.children.append(self.p2Score)

        self.setView(container)

    # Initialize this modules menu view.
    def _initMenu(self):
        self.menu = views.Menu(self, (0, 50), self.size)
        self.menu.setOptions(["Resume", "Start over", "Main menu", "Quit"])

        self.menu.addOptionCallback("Resume", self.back)
        self.menu.addOptionCallback("Start over", self._startGameOver)
        self.menu.addOptionCallback("Main menu", self.back, count=2)
        self.menu.addOptionCallback("Quit", self.quit)

    # Initialize the views for the scores of this game that is paused.
    def _initScores(self):
        # Create the TextDisp objects but don't put in any text yet
        self.p1Score = views.TextDisp(self, (10, 10))
        self.p1Score.setFont(fontsize=15)

        self.p2Score = views.TextDisp(self, (self.size[0] - 150, 10))
        self.p2Score.setFont(fontsize=15)

    # Set the text for the scores in the two corners.
    def setScores(self, scores):
        self.p1Score.setText("Player 1: " + str(scores[0]))
        self.p2Score.setText("Player 2: " + str(scores[1]))

    # Assumes that the parent is the GameModule object
    def _startGameOver(self):
        self.parent.reset()
        self.back()
