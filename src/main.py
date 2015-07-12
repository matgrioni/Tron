#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/15/15
#
# The starting main menu for this game. Simply defines/calls
# the different PygameHelper modules that are run for the
# option selections.
###########################################################

from pydroid import modules, settings

from SettingsMenu import SettingsMenu
from Game import Game
import PodSixNet

class MainMenu(modules.Menu):
    def __init__(self, size=(640, 480), fill=(255, 255, 255)):
        # Load the colors for the text and background which will
        # be used throughout the game.
        
        # Not using this for now until theming is more established.
        # self._initColors()

        # No parent, this is the parent PygameHelper module
        super(MainMenu, self).__init__(fill=fill, size=size)
        self.setOptions(["Local", "Network", "Settings", "Quit"])

        self.addOptionCallback("Local", self._startGame)
        # self.addOptionCallback("Settings", self._settingsMenu)
        self.addOptionCallback("Quit", self.quit)

    # Run this to set the background and text colors for this module
    def _initColors(self):
        fillStr = settings.Settings.load("bg", "(255, 255, 255)")
        fontStr = settings.Settings.load("txt", "(0, 0, 0)")

        fillChannels = [int(n) for n in fillStr.strip()[1:-1].split(",")]
        fontChannels = [int(n) for n in fontStr.strip()[1:-1].split(",")]

        self.fill = tuple(fillChannels)
        self.color = tuple(fontChannels)

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
