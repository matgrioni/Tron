#!/usr/bin/python

######################################################################
# Author: Matias Grioni
# Created: 7/14/15
#
# The module for the main game activity.
######################################################################

from pydroid import modules, views

from GameView import GameView

class GameModule(modules.Module):
    def __init__(self, parent):
        super(GameModule, self).__init__(parent, (255, 255, 255), parent.size)

        # The only view necessary for this module is the game view.
        self.game = GameView(self)
        self.setView(self.game)
