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

# An enum implementation of the possible directions for the
# line rider. The enum values are defined as a tuple, where
# the each value is the scalar for movement in the
# corresponding direction. Therefore TOP=(dx,dy)=(0,1) 
class Direction(object):
    TOP = (0, 1)
    BOTTOM = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

# A LineRider is essentially the line created by the
# players during the game. It is made of multiple
# square blocks that are tuples of the form (x, y, w, h).
class LineRider(object):
    # Define the starting position, color, direction, size
    # of the LineRider. The direction should be a value
    # from Direction defined above. dim is the width and
    # height of the blocks that make up the LineRider.
    def __init__(self, x, y, direction, dim=5, color=(100, 100, 100)):
        self.x, self.y = x, y
        self.direction = direction
        self.dim = dim
        self.color = color

        self.blocks = [(x, y, dim, dim)]

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
