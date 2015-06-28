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
import sys
import string, re
from pygame.locals import *

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
class Module(object):
    def __init__(self, parent=None, size=(640, 480), fill=(255, 255, 255)):
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

        self.millis = 0
        self.fps = 0

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
# Created: 6/24/15
#
# A module that wishes to have a setting associated with it
# should inherit from this. Essentially a key and value
# pair, which will be saved in a new line in the settings
# file defined globally in this module.
###########################################################
class Setting(object):
    SETTINGSFILE = "../settings/settings.txt"

    def setup(self, key, regex):
        self.key = key
        self.regex = regex

    # Used to check if the provided setting matches what is desired
    # Uses a regex to check if the match is correct. True if the
    # input is valid, False otherwise.
    def check(self, value):
        match = re.match(self.regex, value)
        return match is not None and match.group(0) == value

    # Save the value provided along with the name in the game
    # settings file as a newline @"name::value" or overwrites
    # an existing line
    def save(self, value):
        with open(Setting.SETTINGSFILE, "r+") as f:
            found = False
            newLines = []
            for line in f.readlines():
                s = line.strip("\r\n")
                args = s.split("::")

                if args[0] == self.key:
                    found = True
                    newLines.append(self.key + "::" + value)
                else:
                    newLines.append(s)

            if not found:
                newLines.append(self.key + "::" + value)

            f.seek(0)
            f.truncate()
            f.write("\n".join(newLines))

    # Given the current name of the setting, return the value
    # defined for it in the settings file or None if it is not
    # defined.
    def load(self, default=None):
        with open(Setting.SETTINGSFILE, "r") as f:
            for line in f.readlines():
                args = line.strip("\r\n").split("::")

                if args[0] == self.key:
                    return args[1]

        return default

###########################################################
# Author: Matias Grioni
# Created: 6/21/15
#
# Widget to display any arbitrary text in desired style
# in desired position.
###########################################################
class TextDisp(object):
    def __init__(self, x, y, text="", font="monospace", fontsize=20):
        self.x, self.y = x, y
        self.text = text

        self.font = pygame.font.SysFont(font, fontsize)

    def draw(self, screen):
        surface = self.font.render(self.text, False, (0, 0, 0))
        screen.blit(surface, (self.x, self.y))

###########################################################
# Author: Matias Grioni
# Created: 6/22/15
#
# An input box that takes up the whole screen, and accepts
# text input. This is a very rudimentary form of input and
# should be tweaked in the future.
###########################################################
class SettingInput(Module, Setting):
    def __init__(self, query, parent=None,
                 size=(640, 480), fill=(255, 255, 255)):
        super(SettingInput, self).__init__(parent, size, fill)
        self.printable = [p for p in string.printable \
                          if p not in string.whitespace or p == " "]
        self.x = size[0] / 2 - 200
        self.y = 100

        self.entry = ""
        self.query = query
        self.font = pygame.font.SysFont("monospace", 20)

        self.errorMsg = TextDisp(0, 0)

        self.addEventCallback((KEYDOWN, None), self._addEventChar)
        self.addEventCallback((KEYDOWN, K_RETURN), self._finish)
        self.addEventCallback((KEYDOWN, K_BACKSPACE), self._backspace)

    def setup(self, key, regex):
        super(SettingInput, self).setup(key, regex)
        self.entry = self.load("")

    def setFont(self, font="monospace", fontsize=20):
        self.font = pygame.font.SysFont(font, fontsize)

    def draw(self):
        self.screen.fill(self.fill)

        fSurface = self.font.render(self.query + self.entry, False, (0, 0, 0))
        self.screen.blit(fSurface, (self.x, self.y))
        
        self.errorMsg.draw(self.screen)

    def _backspace(self, e):
        self.entry = self.entry[:-1]

    def _addEventChar(self, e):
        if e.unicode in self.printable:
            self.entry += e.unicode

    def _finish(self, e):
        if self.regex != "":
            if self.check(self.entry):
                self.save(self.entry)
                self.back()
            else:
                self.errorMsg.text = "Input does not match required format"
        else:
            self.save(self.entry)
            self.back()

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
    def __init__(self, options, parent=None, size=(640, 480), fill=(255, 255, 255)):
        super(Menu, self).__init__(parent, size, fill)

        self.selectedItem = 0

        # Create a list of surfaces for the provided options
        self.font = pygame.font.SysFont("monospace", 20)
        self.setOptions(options)

        self.optionCallbacks = {}

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
        self.renderedOptions = [self.font.render(option, False, (0, 0, 0)) \
                                for option in options]
        self.maxWidth = max([o.get_width() for o in self.renderedOptions])

    # Draw the text and the appropriate selector shape
    def draw(self):
        self.screen.fill(self.fill)

        for (i, option) in enumerate(self.renderedOptions):
            # Draw the menu items
            x = (self.size[0] - option.get_width()) / 2
            y = 100 + i * option.get_height()
            self.screen.blit(option, (x, y))

            if i == self.selectedItem:
                sidePoint = ((self.size[0] - self.maxWidth) / 2 - 20,
                             y + option.get_height() / 2)
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
