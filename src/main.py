#!/usr/bin/python

###########################################################
# Author: Matias Grioni
# Created: 6/15/15
#
# The starting main menu for this game. Simply defines/calls
# the different PygameHelper modules that are run for the
# option selections.
###########################################################

from Menu import Menu

class MainMenu(Menu):
    def __init__(self, size=(640, 480), fill=(255, 255, 255)):
        options = ["Play", "Settings", "Quit"]
        super(MainMenu, self).__init__(size=size, fill=fill, options)

if __name__ == "__main__":
    menu = MainMenu()
    menu.execute(50)
