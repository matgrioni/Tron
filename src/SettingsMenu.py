#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# A menu of the possible settings for the game.
###########################################################

from pydroid import modules, settings

class SettingsMenu(modules.Menu):
    COLOR_REGEX = "\\(\\d{1,3}\\s*,\\s*\\d{1,3}\\s*,\\s*\\d{1,3}\\)"

    def __init__(self, parent, fill=(255, 255, 255)):
        super(SettingsMenu, self).__init__(parent, fill)
        self.setOptions(["Player 1 Color", "Player 2 Color", "Text Color",
                         "Background Color", "Back"])

        self.addOptionCallback("Player 1 Color", self._inputColor,
                               "p1", "Enter color of Player 1 as (r, g, b)")
        self.addOptionCallback("Player 2 Color", self._inputColor,
                               "p2", "Enter color of Player 2 as (r, g, b)")
        self.addOptionCallback("Text Color", self._inputColor,
                               "txt", "Enter color of text as (r, g, b)")
        self.addOptionCallback("Background Color", self._inputColor,
                               "bg", "Enter color of game screen as (r, g, b)")
        self.addOptionCallback("Back", self.back)

    # Input the color for the described setting key
    def _inputColor(self, key, desc):
        # Setup the text input for the color with the setting key for the file
        # the regex for checking the input as a triplet, and the desc of the
        # input.
        colorInput = settings.SettingInput(parent=self)
        colorInput.setting(key, SettingsMenu.COLOR_REGEX)
        colorInput.setup(desc)
        colorInput.setQuery("Color: ")

        colorInput.execute(self.fps)
