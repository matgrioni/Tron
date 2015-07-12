###########################################################
# Author: Matias Grioni
# Created: 7/3/15
#
# Widgets are small components that are inserted in modules
# which are full screen interactions. Widgets are for
# example a TextDisp, EditText, etc.
###########################################################

import pygame

###########################################################
# Author: Matias Grioni
# Created: 7/12/15
#
# A base class for widgets. Includes fields such size,
# position, focus and background color.
###########################################################
class Widget(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# Widget to display any arbitrary text in position (x, y)
# on a pygame surface with customizable font.
###########################################################
class TextDisp(Widget):
    # Creates a TextDisp at the provided coordinates displaying provided text.
    # The font is monospace, size 20, and black by default
    def __init__(self, x, y, text=""):
        super(TextDisp, self).__init__(x, y)

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
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    # Draws the text at x, y on the provided surface
    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))
