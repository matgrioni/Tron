#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/14/15
#
# Module that contains all the widgets for the program.
# The idea is that for all the necessary views, inputs,
# displays and screens of the program. Some widget can be
# extended and used.
###########################################################

import pygame
from pygame.locals import *

import utils

import sys
import string, re

######################################################################
# Author: Matias Grioni
# Created: 8/4/15
#
# The different input modes for the module. The module can be either
# in touch mode or keyboard mode.
#
# In touch mode, the user is using the the mouse to click and interact
# with elements. Most elements are not focusable except a few such as
# InputBox which need to hold focus to accept input.
#
# In keyboard mode, the user uses the keyboard to interact with the
# views as necessary.
######################################################################
class InputMode(object):
    TOUCH_MODE, KEY_MODE = range(2)

###########################################################
# Author: Matias Grioni
# Created: 6/2/15
#
# A base class for the pygame logic units. Allows an oop
# design and for modularization of the logic rather than
# procedural design in a large while loop.
#
# Extend this class and then set the view you want to pouplate
# this module with. Parallel is to setContentView in Android.
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
class Module(utils.EventHandler):
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
            
            # Start out each module in touch mode
            self.mode = InputMode.TOUCH_MODE
        else:
            self.screen = parent.screen
            self.size = (self.screen.get_width(), self.screen.get_height())
            self.mode = parent.mode

        self.parent = parent
        self.fill = fill

        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Create the dictionaries that bind an event to a user
        # defined callback. Each event has one possible callback
        # and if a callback is assigned to an event code which is
        # already assigned then the new will overwrite the old.
        self.eventCallbacks = {}

        self.addEventCallback((KEYDOWN, K_ESCAPE), self.back)
        self.addEventCallback((QUIT, None), self.quit)
        self.addEventCallback((MOUSEBUTTONDOWN, None), self._handleClickDown)
        self.addEventCallback((KEYDOWN, (K_TAB, K_UP, K_DOWN)),
                              self._handleInputModeKeyChanger)

    def setView(self, view):
        self.view = view

    def title(self, s):
        pygame.display.set_caption(s)

    def reset(self):
        # Force reset the screen
        self.screen.fill(self.fill)       
        pygame.display.flip()

        self.fps = 60
        self.view.reset()

    # The following are base logic functions that are mostly bare here
    # but should be implemented in child classes.

    # Handles all events in the pygame event queue, and then bubbles down
    # all events through the view hierarchy, so that any child views,
    # grandchildren, etc, can have event listeners that will be reached.
    def handleEvents(self):
        # Simply handle all the event callbacks assigned to this activity.
        for e in pygame.event.get():
            self.handleEvent(e)

            # If the module is in TOUCH_MODE, then the event is either a mouse
            # event, or a keyboard event if the view is focusableInTouchMode.
            # Either way, all events must be routed to the main event.
            #
            # If the module is in KEY_MODE, then the event is a keyboard event
            # assuredly. If there is a view focused, then dispatch the event to
            # it.TODO: Not really sure if this is redundant in any way. Just making
            # sure.

            # Now once the module has handled all the events it needs to,
            # continue passing the event through the view tree. Assuming that
            # the root view takes up the entire screen.
            if self.mode == InputMode.TOUCH_MODE:
                self.view.handleEvent(e)
            elif self.mode == InputMode.KEY_MODE:
                if self.view.focused:
                    self.view.handleEvent(e)

    def update(self):
        if self.view is not None:
            self.view.update()
    
    def draw(self):
        if self.view is not None:
            self.view.draw()

    # Runs the current game definition in this instance of PygameHelper.
    def execute(self):
        self.running = True

        # Even if the module, isn't running, it should display the initial
        # screen but not update its screen. This helps if there is a pause
        # in execution.
        self.screen.fill(self.fill)
        self.draw()
        pygame.display.flip()

        # Accept input and update the screen, 
        while self.running:
            self.handleEvents()
            self.update()
            self.draw()
            pygame.display.flip()

            self.clock.tick(self.fps)

        # For when the loop is over, if it's transitioning
        # to a new screen we want to clear it before then, and then draw
        # the next screen so that it starts off with a clean slate.
        # Mostly, for timing purposes though, in the future, an activity
        # lifecycle should be implemented.
        self.screen.fill(self.fill)
        if self.parent is not None:
            self.parent.draw()
        pygame.display.flip()

    # Moves up through the module stack back times. If the
    # current module is the root, quit the app. 
    def back(self, e=None, count=1):
        if count > 0:
            if self.parent is None:
                self.quit()
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

    # If there is a click down, then the module automatically enters TOUCH_MODE
    # The event would then be dispatched to the root view for this module.
    # If there is a view that is currently focused on, then that view is
    # unfocused.
    def _handleClickDown(self, e):
        # Any views that had focus in KEY_MODE should lose focus.
        if self.mode == InputMode.KEY_MODE:
            if self.view.focused:
                self.view.setFocused(False)

        self.mode = InputMode.TOUCH_MODE

    # If there is a keydown event for the up or down arrows, or the
    # tab key, then we enter KEY_MODE, but only if there are no views
    # that are focused (they would be focusableInTouchMode).
    def _handleInputModeKeyChanger(self, e):
        if self.mode == InputMode.TOUCH_MODE:
            if self.view.focused:
                self.mode = InputMode.KEY_MODE
                self.view.setFocused(False)
