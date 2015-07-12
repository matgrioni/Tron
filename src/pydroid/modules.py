#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/14/15
#
# Module that contains all the widgets for the program.
# The idea is that for all the necessary widgets, inputs,
# displays and screens of the program. Some widget can be
# extended and used.
###########################################################

import pygame
from pygame.locals import *

import sys
import string, re

import widgets

###########################################################
# Author: Matias Grioni
# Created: 6/2/15
#
# A base class for the pygame logic units. Allows an oop
# design and for modularization of the logic rather than
# procedural design in a large while loop.
#
# Extend this class and override the different handler,
# update and draw methods.
#
# This class is inspired from phyces original code for
# PygameHelper. The one major difference is that the
# original used the function handleEvents with if blocks
# to check for all the current events. This implementation
# defines callbacks and the events for which these callbacks
# are used.
#
# This gives the user more ability to control what and when
# is being called for the events.
#
# This code also has the ability to stack modules on top of
# each other. The quit function will quit the entire game
# when called and back will stop the current module and
# therefore the prior module will resume execution.
###########################################################
class Module(object):
    def __init__(self, parent=None, fill=(255, 255, 255), size=(640, 480)):
        # This is only included so that when widget classes that extend this
        # can easily extend the constructor while using multiple inheritance
        super(Module, self).__init__()

        # If this is the root PygameHelper object must initialize
        # pygame and create the screen. Otherwise take these objects
        # from the provided parent.
        if parent is None:
            pygame.init()
            self.size = size
            self.screen = pygame.display.set_mode(size)
        else:
            self.screen = parent.screen
            self.size = (self.screen.get_width(), self.screen.get_height())


        self.parent = parent
        self.fill = fill

        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.millis = 0

        # Create the dictionaries that bind an event to a user
        # defined callback. Each event has one possible callback
        # and if a callback is assigned to an event code which is
        # already assigned then the new will overwrite the old.
        self.eventCallbacks = {}

        self.addEventCallback((KEYDOWN, K_ESCAPE), self.back)
        self.addEventCallback((QUIT, None), self.quit)

    # Similar to init except it keeps all the callbacks the same.
    # Equivalent to the state of the module before update was ever
    # called.
    def reset(self):
        pass

    # Adds a callback for the keyboard event code. All codes have one
    # unique callback. event should be a tuple where the first entry
    # is the event type, and the second entry is the key code.
    # The key code for KEYUP or KEYDOWN is event.key, for
    # MOUSEBUTTONUP or MOUSEBUTTONDOWN its event.button, for
    # MOUSEMOTION its event.buttons.
    #
    # For a callback to be defined only for the event type, the
    # event param should only be (type, None). A callback can be
    # defined for multiple events too. For example, (KEYDOWN,
    # (K_ESCAPE, K_UP)), will fire on KEYDOWN for the escape key
    # and up arrow. If an event matches multiple callbacks the
    # priority is single qualifier,  multiple qualifiers, general
    # type.
    #
    # Lastly, the callback should have a function parameter 
    # for an event.
    def addEventCallback(self, event, callback, *args, **kwargs):
        self.eventCallbacks[event] = (callback, args, kwargs)

    # Removes the callback for the provided event and returns the
    # previously added callback or None if there was none defined
    # for the event.
    def removeEventCallback(self, event):
        return self.eventCallbacks(event, None)

    def clearEventCallbacks(self):
        self.eventCallbacks.clear()

    # The following functions _handleEvents, update, and draw, are
    # called once every loop iteration as seen in mainLoop.

    # For each current event in the queue check it against the codes
    # for the defined callbacks. This function does not have to
    # defined by the client, nor should it be called publicly.
    #
    # To control event handlers use the callback access methods.
    def _handleEvents(self):
        for e in pygame.event.get():
            # Determine the necessary event information.
            if e.type == KEYUP or e.type == KEYDOWN:
                info = (e.type, e.key)
            elif e.type == MOUSEBUTTONDOWN or e.type == MOUSEBUTTONUP:
                info = (e.type, e.button)
            elif e.type == MOUSEMOTION:
                info = (e.type, e.buttons)
            else:
                # info has to be assigned to something so
                # no error is thrown.
                info = (None, None)
            
            # The progression of checks for the event is first
            # for the general event, then for events with
            # multiple qualifiers, then for a specific event
            # with one type and one qualifier.
            
            # Check specifics first.
            if info in self.eventCallbacks:
                callback = self.eventCallbacks[info]
                self._handleCallback(e, callback)

            # Then check for a callback linked to multiple events
            # such as (KEYDOWN, (K_ESCAPE, K_UP))
            for (key, _) in self.eventCallbacks.iteritems():
                if type(key[1]) is tuple:
                    if info[0] == key[0] and info[1] in key[1]:
                        callback = self.eventCallbacks[key]
                        self._handleCallback(e, callback)

            # Also check if the general callback for only the
            # event type is defined.
            if (e.type, None) in self.eventCallbacks:
                callback = self.eventCallbacks[(e.type, None)]
                self._handleCallback(e, callback)

    # Provided the tuple of (callback, *args, **kwargs) call the method
    def _handleCallback(self, e, callback):
        func = callback[0]
        args = callback[1]
        kwargs = callback[2]

        func(e, *args, **kwargs)

    # Update the game state after one loop iteration. This helper class
    # does not implement this but a class that does implements the game
    # logic here.
    def update(self):
        pass
    
    # Draw whatever is needed to the screen. This function is defined
    # in classes that derive from PygameHelper.
    def draw(self):
        pass

    # Runs the current game definition in this instance of PygameHelper.
    def execute(self, fps=0):
        self.running = True
        self.fps = fps

        self.screen.fill(self.fill)
        pygame.display.flip()

        # Accept input and update the screen, 
        while self.running:
            self._handleEvents()
            self.update()
            self.draw()
            pygame.display.flip()

            self.clock.tick(self.fps)
            self.wait()

        # For when the loop is over, if it's transitioning
        # to a new screen we want to clear it before then
        self.screen.fill(self.fill)
        pygame.display.flip()

    def wait(self):
        pygame.time.delay(self.millis)

    def title(self, s):
        pygame.display.set_caption(s)

    # Moves up through the module stack back times. If the
    # current module is the root, quit the app. 
    def back(self, e=None, count=1):
        if count > 0:
            if self.parent is None:
                self.quit(e)
            else:
                # If the parent has a different fill color
                # then change the screen to that fill color
                self.fill = self.parent.fill
                self.running = False

                count -= 1
                self.parent.back(e, count)

    # Used specifically for quitting the entire application.
    # e can be None since quitting the application doesn't
    # have to be associated with a certain event. For example
    # a menu option could quit the application.
    def quit(self, e=None):
        self.running = False
        pygame.quit()
        sys.exit()

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
class Menu(Module):
    def __init__(self, parent=None, fill=(255, 255, 255), size=(640, 480)):
        super(Menu, self).__init__(parent, fill, size)

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

    # To set the options for the menu use this method rather
    # than setting self.options automatically.
    def setOptions(self, options):
        self.options = options
        del self.textdisps[:]
        
        for (i, option) in enumerate(options):
            if i == 0:
                self.textdisps.append(widgets.TextDisp(30, 30, option))
            else:
                prior = self.textdisps[i - 1]
                newY = prior.y + prior.height + 10

                self.textdisps.append(widgets.TextDisp(30, newY, option))

    # Draw the text and the appropriate selector shape
    def draw(self):
        self.screen.fill(self.fill)

        for (i, textdisp) in enumerate(self.textdisps):
            textdisp.draw(self.screen)

            # Draw the triangle indicator
            if i == self.selectedItem:
                sidePoint = (20, textdisp.y + textdisp.height / 2)
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
