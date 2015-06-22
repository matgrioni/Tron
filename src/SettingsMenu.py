#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# A menu of the possible settings for the game.
###########################################################

from widgets import InputDisp, Menu

class SettingsMenu(Menu):
    def __init__(self, parent=None, size=(640, 480), fill=(255, 255, 255)):
        options = ["Player colors", "Background Color", "Back"]
        super(SettingsMenu, self).__init__(options, parent, size, fill)

        self.addOptionCallback("Player colors", self._input)
        self.addOptionCallback("Back", self.back)

    def _input(self):
        inputDisp = InputDisp("Color: ", parent=self)
        inputDisp.execute(self.fps)
