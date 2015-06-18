#!/usr/bin/python

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
# This gives the user more ability to control what and when
# is being called for the events.
###########################################################

import pygame, sys
from pygame.locals import *

class PygameHelper(object):
    def __init__(self, parent=None, size=(640, 480), fill=(255, 255, 255)):
        # If this is the root PygameHelper object must initialize
        # pygame and create the screen. Otherwise take these objects
        # from the provided parent.
        self.parent = parent
        if parent is None:
            pygame.init()
            self.size = size
            self.screen = pygame.display.set_mode(size)
        else:
            self.screen = parent.screen
            self.size = (self.screen.get_width(), self.screen.get_height())

        self.fill = fill
        self.running = False
        self.clock = pygame.time.Clock()

        self.fps = 0

        # Create the dictionaries that bind an event to a user
        # defined callback. Each event has one possible callback
        # and if a callback is assigned to an event code which is
        # already assigned then the new will overwrite the old.
        self.eventCallbacks = {}

        self.addEventCallback((KEYDOWN, K_ESCAPE), self.quit)
        self.addEventCallback((QUIT, None), self.quit)

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
    def addEventCallback(self, event, callback):
        self.eventCallbacks[event] = callback

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
                callback(e)

            # Then check for a callback linked to multiple events
            # such as (KEYDOWN, (K_ESCAPE, K_UP))
            for (key, _) in self.eventCallbacks.iteritems():
                if type(key[1]) is tuple:
                    if info[0] == key[0] and info[1] in key[1]:
                        callback = self.eventCallbacks[key]
                        callback(e)

            # Also check if the general callback for only the
            # event type is defined.
            if (e.type, None) in self.eventCallbacks:
                callback = self.eventCallbacks[(e.type, None)]
                callback(e)

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

    def quit(self, e=None):
        self.running = False
        if self.parent is None:
            pygame.quit()
            sys.exit()
