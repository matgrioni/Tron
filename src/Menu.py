###########################################################
# Author: Matias Grioni
# Created: 6/14/15
#
# A menu class that extends PygameHelper. This way
# callbacks for navigation can be added simply and drawing
# the items and background can be added in easily.
###########################################################

from PygameHelper import PygameHelper

class Menu(PygameHelper):
    def __init__(self, parent=None, size=(640, 480), fill=(255, 255, 255), options):
        super(Menu, self).__init__(parent, size, fill)
        self.options = options
        self.optionsCallbacks = {}

        # Define the default keyboard events for menu navigation
        self.addEventCallback((KEYDOWN, K_UP), self._moveSelectedUp)
        self.addEventCallback((KEYDOWN, K_DOWN, self._moveSelectedDown)

    # Option callbacks are called when the user selects an
    # option from the menu with the enter key. Provide
    # the option name and the method to be run when the
    # item is selected.
    def addOptionCallback(self, option, callback):
        pass

    # Remove the current 
    def removeOptionCallback(self, option):
        return self.optionsCallback(option, None)

    def draw(self):
        pass
