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

import pygame

def PygameHelper:
    def __init__(self, size=(640, 320), fill=(255, 255, 255)):
        pygame.init()

        # Create the screen based on the parameters
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(fill)
        pygame.display.flip()
        self.size = size

        self.running = False
        self.clock = pygame.time.Clock()

        self.fps = 0

        # Create the dictionaries that bind an event to a user
        # defined callback. Each event has one possible callback
        # and if a callback is assigned to an event code which is
        # already assigned then the new will overwrite the old.
        self.eventCallbacks = {}

    # Adds a callback for the keyboard event code. All codes have one
    # unique callback. event should be a tuple where the first entry
    # is the key code, and the second entry is the event type.
    def addEventCallback(self, event, callback):
        self.eventCallbacks[event] = callback

    # Removes the callback for the provided event and returns the
    # previously added callback or None if there was none defined
    # for the event.
    def removeEventCallback(self, event):
        return self.eventCallbacks(event, None)

    # The following functions _handleEvents, update, and draw, are
    # called once every loop iteration as seen in mainLoop.

    # For each current event in the queue check it against the codes
    # for the defined callbacks. This function does not have to
    # defined by the client, nor should it be called publicly.
    #
    # To control event handlers use the callback access methods.
    def _handleEvents(self):
        pass

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

        # Accept input and update the screen, 
        while self.running:
            self._handlEvents();
            self.update();
            self.draw();
            pygame.display.flip()

            self.clock.tick(self.fps)
