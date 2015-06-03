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
# This class is inspired from phyces original code.
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
        self.keyCallbacks = {};
        self.mouseCallbacks = {};

    # Adds a 
    def addKeyCallback(self, code, callback) {
        self.keyCallbacks[code] = callback
    }
