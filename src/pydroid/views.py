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

from types import NoneType

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
        self.parent = None

        self.x, self.y = pos[0], pos[1]
        self.size = size

        self.background = (255, 255, 255)
        self.curBackground = self.background

        self.focused = False
        self.focusable = True
        self.focusableInTouchMode = False

        self.pressed = False
        self.pressable = True

        self.addEventCallback((MOUSEBUTTONDOWN, None), self._handleClickDown)
        self.addEventCallback((MOUSEBUTTONUP, None), self._handleClickUp)

    def reset(self):
        pass

    def update(self):
        pass

    # Handles basic drawing behavior such as background color
    def draw(self):
        bounds = (self.x, self.y, self.size[0], self.size[1])
        pygame.draw.rect(self.screen, self.curBackground, bounds)

    def setPosition(self, pos):
        self.x, self.y = pos[0], pos[1]

    # Returns True if the given position is within or on the bounds of this
    # view. Bounds for checking are not inclusive.
    def posInBounds(self, x, y):
        return (x > self.x and x < self.x + self.size[0]) and \
            (y > self.y and y < self.y + self.size[1])

    # Set if the view is able to be focused on.
    def setFocusable(self, focusable):
        self.focusable = focusable

        # If not focusable then set it to not focused currently.
        if not self.focusable:
            self.clearFocus()

    # Set if the view is able to be focused on in touch mode.
    def setFocusableInTouchMode(self, focusableInTouchMode):
        self.focusableInTouchMode = focusableInTouchMode

    # Focuses this view if it is focusable and updates the focused index
    # member in the parent, to match the position of this child view.
    def requestFocus(self):
        if self.focusable:
            if isinstance(self.parent, ViewGroup):
                self.parent._updateFocus(self)

            self.focused = True

    # Removes focus from this view if it had any and updates the focused index
    # member variable in the parent to signify no views are focused.
    def clearFocus(self):
        if self.focused:
            if isinstance(self.parent, ViewGroup):
                self.parent._clearChildFocus()

            self.focused = False

    # Set if this view is pressable. If False is passed in, then the view's
    # pressed state is set to False.
    def setPressable(self, pressable):
        self.pressable = pressable

        if not self.pressable:
            self.pressed = False

    # Set if the current view is pressed or not
    def setPressed(self, pressed):
        if self.pressable:
            self.pressed = pressed

            if self.pressed:
                self.curBackground = self.pressedBackground
            else:
                self.curBackground = self.background

    # The default implementation for a down click is to check if it's within the
    # bounds of this view. If so, this view is focused on.
    def _handleClickDown(self, e):
        # If the view is not visible it can not be focused on and then focus
        # on it if the click event position is within the bound box of this
        # view. Change the background color accordingly.
        self.pressed = self.setPressed(True)

        # If this view is clicked and it's focusable in TOUCH_MODE, then it
        # is focused on now.
        if self.focusableInTouchMode:
            self.requestFocus()

    # If the view has a click up event it can not be pressed. It can still
    # be focused however if the view was focusableInTouchMode. A click up
    # on the view would not change the focus state. Only clicking down
    # outside the view would do that.
    def _handleClickUp(self, e):
        self.setPressed(False)

################################################################################
# Author: Matias Grioni
# Created: 7/14/15
#
# A container for multiple different views. Add views by accessing the children
# member variable and calling .append()
################################################################################
class ViewGroup(View):
    def __init__(self, module, pos, size=(0, 0)):
        super(ViewGroup, self).__init__(module, pos, size)
        self.children = []

        self._focusedIndex = -1

        # ViewGroups are not focusable or clickable by default. They are to
        # house other views and organize them.
        self.setFocusable(False)
        self.setPressable(False)

    def handleEvent(self, e):
        if e.type in (KEYUP, KEYDOWN):
            # If this current ViewGroup is focused, then this won't return True
            # and the event will still be sent to the event handlers for this
            # ViewGroup.
            if self._focusedIndex != -1:
                nextChild = self._getFocusedNext()
                if nextChild is not None:
                    nextChild.handleEvent(e)
        elif e.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
            for child in self.children:
                if child.posInBounds(*e.pos):
                    child.handleEvent(e)
                else:
                    child.clearFocus()
 
        super(ViewGroup, self).handleEvent(e)

    def update(self):
        super(ViewGroup, self).update()
        for child in self.children:
            child.update()

    def draw(self):
        super(ViewGroup, self).draw()
        for child in self.children:
            child.draw()

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    # Returns the child of this ViewGroup that is focused. If no view is focused
    # then None is returned.
    def getFocusedChild(self):
        focus = None

        if self._focusedIndex != -1:
            child = self.children[self._focusedIndex]

            if isinstance(child, ViewGroup):
                focus = child.getFocusedChild()
            elif isinstance(child, View):
                focus = child

        return focus

    def _getFocusedNext(self):
        focus = None

        for child in self.children:
            if not focus:
                if child.focused:
                    focus = child
                elif isinstance(child, ViewGroup):
                    focus = child._getFocusedNext()

        return focus

    def _clearChildFocus(self):
        self._focusedIndex = -1

        if isinstance(self.parent, ViewGroup):
            self.parent._clearChildFocus()

    # TODO: Document this.
    # NOTE: Deprecated
    """
    def _focusNext(self):
        if self._focusedIndex < 0:
            self._focusedIndex = 0

        curChild = self.children[self._focusedIndex]
        nextChildFocused = False
        if not curChild.focused:
            if curChild.focusable:
                curChild.requestFocus()
                nextChildFocused = True

        if not nextChildFocused:
            if isinstance(curChild, ViewGroup):
                nextFocusIndex = curChild._focusNext()
                if nextFocusIndex >= 0:
                    nextChildFocused = True

        if not nextChildFocused:
            for (i, child) in enumerate(self.children[self._focusedIndex + 1:]):
                self.children[self._focusedIndex].clearFocus()
                child = self.children[i + self._focusedIndex + 1]

                if child.focusable:
                    child.requestFocus()
                    self._focusedIndex += i + 1
                    nextChildFocused = True
                    break

        if not nextChildFocused:
            self.children[self._focusedIndex].clearFocus()
            self._focusedIndex = -1

        return self._focusedIndex
    """

    def _updateFocus(self, child):
        focus = self._findFocus()
        if focus is not None:
            focus.clearFocus()

        self._focusedIndex = self.children.index(child)
        
        if isinstance(self.parent, ViewGroup):
            self.parent._updateFocus(self)

    def _findFocus(self):
        focus = None

        for child in self.children:
            if not focus:
                if child.focused:
                    focus = child
                elif isinstance(child, ViewGroup):
                    focus = child._findFocus()

        return focus   

######################################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# Widget to display any arbitrary text in position (x, y) on a pygame
# surface with customizable font.
######################################################################
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
class Menu(ViewGroup):
    def __init__(self, module, pos, size):
        super(Menu, self).__init__(module, pos, size)
        self.options = []

    # Option callbacks are called when the user selects an
    # option from the menu with the enter key. Provide
    # the option name and the method to be run when the
    # item is selected. Provide any parameters to the
    # callback through the optional args argument
    def addOptionCallback(self, option, callback, *args, **kwargs):
        if option in self.options:
            index = self.options.index(option)
            self.children[index].addEventCallback((KEYDOWN, K_RETURN),
                                                  callback, *args, **kwargs)
            self.children[index].addEventCallback((MOUSEBUTTONDOWN, 1), callback, *args, **kwargs)

    # Remove the current callback for the option provided. Returns the callback
    # tuple object.
    def removeOptionCallback(self, option):
        if option in self.options:
            index = self.options.index(option)
            return self.children[index].removeEventCallback((KEYDOWN, K_RETURN))

    # Automatically sets the internal option values and creates the
    # TextDisp views for the Menu and automatically displays them
    def setOptions(self, options):
        self.options = options
        del self.children[:]
        
        # For each text option provided create the TextDisp for them.
        for (i, option) in enumerate(options):
            # Accounts for variable heights in the menu items.
            if i == 0:
                menuItem = TextDisp(self.module, (self.x + 30, self.y), option)
            else:
                # Set the next TextDisp 10 pixels below the prior one
                prior = self.children[i - 1]
                newY = prior.y + prior.size[1] + 10
                menuItem = TextDisp(self.module, (self.x + 30, newY), option)

            self.children.append(menuItem)

    # Draw the text and the appropriate selector shape
    def draw(self):
        super(Menu, self).draw()

        for (i, textdisp) in enumerate(self.children):
            textdisp.draw()

            # Draw the triangle indicator
            if i == self._focusedIndex:
                sidePoint = (self.x + 20, textdisp.y + textdisp.size[1] / 2)
                topPoint = (sidePoint[0] - 10, sidePoint[1] - 5)
                botPoint = (sidePoint[0] - 10, sidePoint[1] + 5)

                pygame.draw.polygon(self.screen, (0, 0, 0),
                                    [sidePoint, topPoint, botPoint])
