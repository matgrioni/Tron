##########################################################
# Author: Matias Grioni
# Created: 6/7/15
#
# A controllable line for the game. Extends from pygame's
# provided sprite class. Composed of a starting block that
# moves forward each update cycle in its current direction.
# The LineRider is able to be turned, and must keep track
# of where it has been, to have a continuously growing
# line.
##########################################################

import pygame
from Player import Player

# An enum implementation of the possible directions for the
# line rider. The enum values are defined as a tuple, where
# the each value is the scalar for movement in the
# corresponding direction. Therefore TOP=(dx,dy)=(0,-1) 
class Direction(object):
    TOP = (0, -1)
    BOTTOM = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

# A LineRider is essentially the line created by the
# players during the game. It is made of multiple
# square blocks that are tuples of the form (x, y, w, h).
class LineRider(Player):
    # Define the starting position, color, direction, size
    # of the LineRider. The direction should be a value
    # from Direction defined above. dim is the width and
    # height of the blocks that make up the LineRider.
    def __init__(self, x, y, direction, dim=5, color=(100, 100, 100)):
        super(LineRider, self).__init__()

        self.x, self.y = x, y
        self.direction = self.fDirection = direction
        self.dim = dim
        self.color = color
        self.turnable = True

        self.blocks = [(x, y, dim, dim)]

    # Reset the LineRider to the state it was in after being created
    # As if update was never called.
    def reset(self):
        self.alive = self.fAlive

        first = self.blocks[0]
        self.x, self.y = first[0], first[1]
        self.direction = self.fDirection
        self.turnable = True

        del self.blocks[1:]

    def checkAlive(self, player, bounds):
        self.alive = not self._collides(player) and self._inbounds(bounds) \
                     and not self._overlap()

        return self.alive

    # Check if the current line rider collides with the
    # provided one. Collision is if the head of this
    # line rider intersects any block of the other.
    def _collides(self, lineRider):
        for block in lineRider.blocks:
            if self.blocks[-1] == block:
                return True

        return False

    # Check if the line rider has overlapped itself.
    def _overlap(self):
        for b in self.blocks:
            if self.blocks.count(b) > 1:
                return True

        return False

    # Check if the linerider is within the provided bounds.
    # The bounds should be provided as (x, y, width, height)
    def _inbounds(self, bounds):
        last = self.blocks[-1]

        return last[0] >= bounds[0] and last[0] < bounds[0] + bounds[2] \
               and last[1] >= bounds[1] and last[1] < bounds[1] + bounds[3]

    # Update the LineRider by adding a new Block to it in
    # the corresponding direction. 
    def update(self):
        last = self.blocks[-1]

        # Remember each block is a tuple in the form
        # (x, y, width, height)
        newX = last[0] + last[2] * self.direction[0]
        newY = last[1] + last[3] * self.direction[1]

        newBlock = (newX, newY, self.dim, self.dim)
        self.blocks.append(newBlock)

    # Iterates through all the tuples defining blocks and
    # draws them using pygame.draw.rect. Requires a ref to
    # the pygame screen object.
    def draw(self, screen):
        for b in self.blocks:
            pygame.draw.rect(screen, self.color, b, 0)

    # Turns this LineRider left assuming the forward direction
    # is the current direction of the LineRider.
    def turnLeft(self):
        if self.turnable:
            if self.direction == Direction.TOP:
                self.direction = Direction.LEFT
            elif self.direction == Direction.BOTTOM:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.TOP
            elif self.direction == Direction.LEFT:
                self.direction = Direction.BOTTOM

    # Turns the LineRider right assuming we are facing the
    # current direction.
    def turnRight(self):
        if self.turnable:
            if self.direction == Direction.TOP:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.BOTTOM:
                self.direction = Direction.LEFT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.BOTTOM
            elif self.direction == Direction.LEFT:
                self.direction = Direction.TOP
