#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/14/15
#
# A menu class that extends PygameHelper. This way
# callbacks for navigation can be added simply and drawing
# the items and background can be added in easily.
# For now only a fullscreen menu is allowed.
###########################################################

import pygame
from pygame.locals import *
from PygameHelper import PygameHelper

class Menu(PygameHelper):
    def __init__(self, options, parent=None, size=(640, 480), fill=(255, 255, 255)):
        super(Menu, self).__init__(parent, size, fill)

        # Create a list of surfaces for the provided options
        self.font = pygame.font.SysFont("monospace", 15)
        self.setOptions(options)

        self.optionCallbacks = {}

        # Define the default keyboard events for menu navigation
        self.addEventCallback((KEYDOWN, K_UP), self._moveSelectedUp)
        self.addEventCallback((KEYDOWN, K_DOWN), self._moveSelectedDown)
        self.addEventCallback((KEYDOWN, K_RETURN), self._selectItem)

    # Option callbacks are called when the user selects an
    # option from the menu with the enter key. Provide
    # the option name and the method to be run when the
    # item is selected.
    def addOptionCallback(self, option, callback):
        self.optionCallbacks[option] = callback

    # Remove the current 
    def removeOptionCallback(self, option):
        return self.optionsCallback(option, None)

    # To set the options for the menu use this method rather
    # than setting self.options automatically.
    def setOptions(self, options):
        self.options = options
        self.renderedOptions = [self.font.render(option, True, (0, 0, 0)) for option in options]

    # Draw the text
    def draw(self):
        for (i, option) in enumerate(self.renderedOptions):
            x = self.size[0] / 2 - option.get_width() / 2
            y = 100 + i * option.get_height()
            self.screen.blit(option, (x, y))

    def _moveSelectedUp(self):
        pass

    def _moveSelectedDown(self):
        pass

    def _selectItem(self):
        self.optionCallbacks["Play"]()
