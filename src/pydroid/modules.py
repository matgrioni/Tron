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

import utils

import sys
import string, re

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
        else:
            self.screen = parent.screen
            self.size = (self.screen.get_width(), self.screen.get_height())

        self.parent = parent
        self.fill = fill

        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.millis = 0

        # Create the dictionaries that bind an event to a user
        # defined callback. Each event has one possible callback
        # and if a callback is assigned to an event code which is
        # already assigned then the new will overwrite the old.
        self.eventCallbacks = {}

        self.addEventCallback((KEYDOWN, K_ESCAPE), self.back)
        self.addEventCallback((QUIT, None), self.quit)

    def setView(self, view):
        self.view = view

    def wait(self):
        pygame.time.delay(self.millis)

    def title(self, s):
        pygame.display.set_caption(s)

    def reset(self):
        self.screen.fill(self.fill)
        
        self.fps = 60
        self.millis = 0

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

            # Now once the module has handled all the events it needs to,
            # continue passing the event through the view tree.
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

        self.screen.fill(self.fill)
        pygame.display.flip()

        # Accept input and update the screen, 
        while self.running:
            self.handleEvents()
            self.update()
            self.draw()
            pygame.display.flip()

            self.clock.tick(self.fps)
            self.wait()

        # For when the loop is over, if it's transitioning
        # to a new screen we want to clear it before then
        self.screen.fill(self.fill)
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
