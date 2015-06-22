#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/15/15
#
# The starting main menu for this game. Simply defines/calls
# the different PygameHelper modules that are run for the
# option selections.
###########################################################

from widgets import Menu
from SettingsMenu import SettingsMenu
from Game import Game

class MainMenu(Menu):
    def __init__(self, size=(640, 480), fill=(255, 255, 255)):
        # No parent, this is the parent PygameHelper module
        options = ["Local", "Network", "Settings", "Quit"]
        super(MainMenu, self).__init__(options=options, size=size, fill=fill)

        self.addOptionCallback("Local", self._startGame)
        self.addOptionCallback("Settings", self._settingsMenu)
        self.addOptionCallback("Quit", self.quit)

    def _startGame(self):
        g = Game(parent=self)
        g.execute(self.fps)

    def _settingsMenu(self):
        settings = SettingsMenu(parent=self)
        settings.execute(self.fps)

if __name__ == "__main__":
    menu = MainMenu()
    menu.title("Tron")
    menu.execute(50)
