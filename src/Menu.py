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

        self.selectedItem = 0

        # Create a list of surfaces for the provided options
        self.font = pygame.font.SysFont("monospace", 25)
        self.setOptions(options)

        self.optionCallbacks = {}

        # Define the default keyboard events for menu navigation
        self.addEventCallback((KEYDOWN, K_UP), self._moveSelectedUp)
        self.addEventCallback((KEYDOWN, K_DOWN), self._moveSelectedDown)
        self.addEventCallback((KEYDOWN, K_RETURN), self._selectItem)

    # Option callbacks are called when the user selects an
    # option from the menu with the enter key. Provide
    # the option name and the method to be run when the
    # item is selected. Provide any parameters to the
    # callback through the optional args argument
    def addOptionCallback(self, option, callback, *args):
        self.optionCallbacks[option] = (callback, args)

    # Remove the current 
    def removeOptionCallback(self, option):
        return self.optionsCallback(option, None)

    # To set the options for the menu use this method rather
    # than setting self.options automatically.
    def setOptions(self, options):
        self.options = options
        self.renderedOptions = [self.font.render(option, False, (0, 0, 0)) for option in options]
        self.maxWidth = max([o.get_width() for o in self.renderedOptions])

    # Draw the text and the appropriate selector shape
    def draw(self):
        self.screen.fill(self.fill)

        for (i, option) in enumerate(self.renderedOptions):
            # Draw the menu items
            x = (self.size[0] - option.get_width()) / 2
            y = 100 + i * option.get_height()
            self.screen.blit(option, (x, y))

            if i == self.selectedItem:
                sidePoint = ((self.size[0] - self.maxWidth) / 2 - 20, y + option.get_height() / 2)
                topPoint = (sidePoint[0] - 10, sidePoint[1] - 5)
                botPoint = (sidePoint[0] - 10, sidePoint[1] + 5)

                pygame.draw.polygon(self.screen, (0, 0, 0), [sidePoint, topPoint, botPoint])

    # Changes the selected item to one higher if possible
    def _moveSelectedUp(self, event):
        if self.selectedItem > 0:
            self.selectedItem -= 1

    # Changes the selected item to one lower if possible
    def _moveSelectedDown(self, event):
        if self.selectedItem < len(self.options) - 1:
            self.selectedItem += 1

    # Selects the current item that is selected and executes
    # that defined callback.
    def _selectItem(self, event):
        option = self.options[self.selectedItem]

        if option in self.optionCallbacks:
            callback = self.optionCallbacks[option][0]
            args = self.optionCallbacks[option][1]

            callback(*args)
