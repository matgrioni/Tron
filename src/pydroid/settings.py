###########################################################
# Author: Matias Grioni
# Created: 7/3/15
#
# A python module dealing with the loading and saving of
# settings. Also defines modules for setting input, such
# as inputting text, which is the only one right now.
# Ideally number pickers, date pickers, color pickers, etc
# would be able to be made.
###########################################################

import modules
import widgets

from pygame.locals import *
import string
import re

###########################################################
# Author: Matias Grioni
# Created: 6/24/15
#
# A class to be used statically to load settings. Similar
# to the way Android works with preferences. One saves
# a value with a key associated with it as text in the
# defined text file (/settings/settings.txt)
###########################################################
class Settings(object):
    SETTINGSFILE = "../settings/settings.txt"

    # Save the value provided along with the name in the game settings
    # file as a line in the format key::value or overwrites an existing line
    @staticmethod
    def save(key, value):
        with open(Settings.SETTINGSFILE, "r+") as f:
            found = False
            newLines = []
            for line in f.readlines():
                s = line.strip("\r\n")
                args = s.split("::")

                if args[0] == key:
                    found = True
                    newLines.append(key + "::" + value)
                else:
                    newLines.append(s)

            if not found:
                newLines.append(key + "::" + value)

            f.seek(0)
            f.truncate()
            f.write("\n".join(newLines))

    # Loads the value for the provided key in the settings file. Returns
    # the default value if the key is not found or None if no default
    # is provided.
    @staticmethod
    def load(key, default=None):
        with open(Settings.SETTINGSFILE, "r") as f:
            for line in f.readlines():
                args = line.strip("\r\n").split("::")

                if args[0] == key:
                    return args[1]

        return default

###########################################################
# Author: Matias Grioni
# Created: 7/3/15
#
# Backbone behind any modules that are made to accept and
# save input. It also accepts regex in order to check if
# the input matches what is desired and produces error
# messages along with descriptions.
###########################################################
class SettingModule(modules.Module):
    # Creates the SettingModule with the defined color for text, fill for
    # background color and window size. Note, if a parent is provided,
    # the size will be equal to the size of the parent regardless of the
    # value passed in.
    def __init__(self, parent=None, color=(0, 0, 0), fill=(255, 255, 255),
                 size=(640, 480)):
        super(SettingModule, self).__init__(parent, color, fill, size)

        # Variable to store the current value. Only strings for value.
        # Also initializes the TextDisp text to be used for the setting
        # description and error if necessary.
        self.value = ""
        
        # Initialize the description and error messages for the SettingModule
        self.desc = widgets.TextDisp(0, 0)
        self.error = widgets.TextDisp(0, self.size[1] - 100)
        self.errorMsg = "Input not in proper format"

        self.desc.setFont(color=self.color)
        self.error.setFont(color=self.color)

        self.addEventCallback((KEYDOWN, K_RETURN), self.save)

    # Setup this SettingModule with the key to save under and also
    # an optional regex pattern to use to check with. Initializes
    # the value of this setting with the stored value or the default
    # if none is found.
    def setting(self, key, regex="", default=""):
        self.key = key
        self.regex = regex

        # Load the value if there is one already stored or the default
        # one if this value has not been stored yet.
        self.value = Settings.load(key, default)

    # Set the text for the description and error messages. If either
    # parameter is omitted that message is let intact
    def setup(self, desc=None, error=None):
        if desc is not None:
            self.desc.setText(desc)

        if error is not None:
            self.errorMsg = error

    # Draws the description and error messages. This already fills every loop
    # so children of SettingModule do not need to call screen.fill only draw
    # what they need displayed.
    def draw(self):
        self.screen.fill(self.fill)
        self.desc.draw(self.screen)
        self.error.draw(self.screen)

    # Saves the current value with the provided key if the input matches
    # the regex, or if there is no regex it auomatically saves the values.
    def save(self, e):
        if self.regex != "":
            if self.check():
                Settings.save(self.key, self.value)
                self.back()
            else:
                self.error.setText(self.errorMsg)
        else:
            Settings.save(self.key, self.value)
            self.back()

    # Checks if the current inputted value to this SettingModule is
    # a valid. If no regex has been provided then this will return false.
    def check(self):
        match = re.match(self.regex, self.value)
        return match is not None and match.group(0) == self.value

###########################################################
# Author: Matias Grioni
# Created: 6/22/15
#
# An input box that takes up the whole screen, and accepts
# text input. This is a very rudimentary form of input and
# should be tweaked in the future.
###########################################################
class SettingInput(SettingModule):
    def __init__(self, parent=None, color=(0, 0, 0), fill=(255, 255, 255),
                 size=(640, 480)):
        super(SettingInput, self).__init__(parent, color, fill, size)
        # The list of characters we want to print out when the keyboard
        # event is fired.
        self.printable = [p for p in string.printable \
                          if p not in string.whitespace or p == " "]
        self.x = 75
        self.y = 100

        self.query = ""
        self.disp = widgets.TextDisp(self.x, self.y)

        # Set the default pygame event actions for all SettingInput
        # objects.
        self.addEventCallback((KEYDOWN, None), self._addChar)
        self.addEventCallback((KEYDOWN, K_BACKSPACE), self._backspace)

    # Wrapper around the local query object TextDisp object
    def setQuery(self, query):
        self.query = query
        self.disp.setText(query + self.value)

    # Draws the current value
    def draw(self):
        super(SettingInput, self).draw()
        self.disp.draw(self.screen)

    # Local method to remove the last character from the setting value
    # Shouldn't be used by client.
    def _backspace(self, e):
        self.value = self.value[:-1]
        self.disp.setText(self.query + self.value)

    # Adds the unicode representation of they keyboard event if it is an
    # acceptable character in the printable list defined in __init__.
    def _addChar(self, e):
        if e.unicode in self.printable:
            self.value += e.unicode
            self.disp.setText(self.query + self.value)
