#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# A menu of the possible settings for the game.
###########################################################

import widgets

class SettingsMenu(widgets.Menu):
    def __init__(self, parent=None, size=(640, 480), fill=(255, 255, 255)):
        options = ["Player 1 Color", "Player 2 Color",
                   "Background Color", "Back"]
        super(SettingsMenu, self).__init__(options, parent, size, fill)

        self.addOptionCallback("Player 1 Color", self._saveColor, "p1")
        self.addOptionCallback("Player 2 Color", self._saveColor, "p2")
        self.addOptionCallback("Background Color", self._saveColor, "bg")
        self.addOptionCallback("Back", self.back)

    def _saveColor(self, desc):
        inputBox = widgets.SettingInput("Color: ", parent=self)
        inputBox.setFont("monospace", 15)
        inputBox.setup(desc, "\\(\\d{1,3}\\s*,\\s*\\d{1,3}\\s*,\\s*\\d{1,3}\\)")

        inputBox.execute(self.fps)
