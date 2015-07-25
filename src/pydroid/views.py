#####################################################################
# Author: Matias Grioni
# Created: 7/3/15
#
# Views are small components that are inserted in modules which are
# full screen interactions. Views are for example a TextDisp, EditText
# menu, etc.
#####################################################################

import pygame
from pygame.locals import *

import utils

######################################################################
# Author: Matias Grioni
# Created: 7/12/15
#
# A base class for views. Includes fields such size, position, focus
# background. Also includes general logic for event handling similar
# to modules.
######################################################################
class View(utils.EventHandler):
    def __init__(self, module, pos=(0, 0), size=(0, 0)):
        super(View, self).__init__()
        self.module = module
        self.screen = module.screen

        self.x, self.y = pos[0], pos[1]
        self.size = size

        self.background = (255, 255, 255)
        self.visible = True

    def reset(self):
        pass

    def update(self):
        pass

    # Handles basic drawing behavior such as background color
    def draw(self):
        if self.visible:
            bounds = (self.x, self.y, self.size[0], self.size[1])
            pygame.draw.rect(self.screen, self.background, bounds)

######################################################################
# Author: Matias Grioni
# Created: 7/14/15
#
# A container for multiple different views. Add views by accessing
# the children member variable, and calling .append()
######################################################################
class ViewGroup(View):
    def __init__(self, module, pos, size=(0, 0)):
        super(ViewGroup, self).__init__(module, pos, size)
        self.children = []

    def handleEvent(self, e):
        super(ViewGroup, self).handleEvent(e)

        for child in self.children:
            child.handleEvent(e)

    def update(self):
        for child in self.children:
            child.update()

    def draw(self):
        super(ViewGroup, self).draw()
        for child in self.children:
            child.draw()
        

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# Widget to display any arbitrary text in position (x, y)
# on a pygame surface with customizable font.
###########################################################
class TextDisp(View):
    # Creates a TextDisp at the provided coordinates displaying provided text.
    # The font is monospace, size 20, and black by default
    def __init__(self, module, pos, text=""):
        super(TextDisp, self).__init__(module, pos)

        self.setFont("monospace", 20, (0, 0, 0))
        self.setText(text)

    # Sets the font of this TextDisp. Any omitted parameter is not affected.
    def setFont(self, font=None, fontsize=None, color=None):
        if font is not None:
            self.fonttype = font
        
        if fontsize is not None:
            self.fontsize = fontsize

        if color is not None:
            self.color = color

        self.font = pygame.font.SysFont(self.fonttype, self.fontsize)

    # Recreates the text surface using the passed in text
    def setText(self, text):
        self.surface = self.font.render(text, False, self.color)
        self.size = (self.surface.get_width(), self.surface.get_height())

    # Draws the text at x, y on the provided surface
    def draw(self):
        super(TextDisp, self).draw()
        self.screen.blit(self.surface, (self.x, self.y))

#####################################################################
# Author: Matias Grioni
# Created: 7/12/15
#
# A simple input box that has an outline, a cursor, and a query as
# well.
#####################################################################
class InputBox(TextDisp):
    def __init__(self, x, y, query):
        super(InputBox, self).__init__(x, y, query)

###########################################################
# Author: Matias Grioni
# Created: 6/14/15
#
# A menu class that extends PygameHelper. This way
# callbacks for navigation can be added simply and drawing
# the items and background can be added in easily.
# For now only a fullscreen menu is allowed. Module contains
# all the menus that will be used in the program.
###########################################################
class Menu(View):
    def __init__(self, module, pos, size):
        super(Menu, self).__init__(module, pos, size)

        # Initialize local variables for the menu
        self.selectedItem = 0
        self.optionCallbacks = {}

        self.textdisps = []

        # Define the default keyboard events for menu navigation
        self.addEventCallback((KEYDOWN, K_UP), self._moveSelectedUp)
        self.addEventCallback((KEYDOWN, K_DOWN), self._moveSelectedDown)
        self.addEventCallback((KEYDOWN, K_RETURN), self._selectItem)

    # Option callbacks are called when the user selects an
    # option from the menu with the enter key. Provide
    # the option name and the method to be run when the
    # item is selected. Provide any parameters to the
    # callback through the optional args argument
    def addOptionCallback(self, option, callback, *args, **kwargs):
        self.optionCallbacks[option] = (callback, args, kwargs)

    # Remove the current 
    def removeOptionCallback(self, option):
        return self.optionsCallback(option, None)

    # Automatically sets the internal option values and creates the
    # TextDisp views for the Menu and automatically displays them
    def setOptions(self, options):
        self.options = options
        del self.textdisps[:]
        
        for (i, option) in enumerate(options):
            if i == 0:
                self.textdisps.append(TextDisp(self.module, (30, 30), option))
            else:
                prior = self.textdisps[i - 1]
                newY = prior.y + prior.size[1] + 10

                self.textdisps.append(TextDisp(self.module, (30, newY), option))

    # Draw the text and the appropriate selector shape
    def draw(self):
        super(Menu, self).draw()

        for (i, textdisp) in enumerate(self.textdisps):
            textdisp.draw()

            # Draw the triangle indicator
            if i == self.selectedItem:
                sidePoint = (20, textdisp.y + textdisp.size[1] / 2)
                topPoint = (sidePoint[0] - 10, sidePoint[1] - 5)
                botPoint = (sidePoint[0] - 10, sidePoint[1] + 5)

                pygame.draw.polygon(self.screen, (0, 0, 0),
                                    [sidePoint, topPoint, botPoint])

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
            kwargs = self.optionCallbacks[option][2]

            callback(*args, **kwargs)
