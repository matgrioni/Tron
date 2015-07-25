######################################################################
# Author: Matias Grioni
# Created: 7/12/15
#
# Utils class that has shared interfaces/classes that are not really
# used on their own but only shared by other classes. I wasn't really
# sure what to call it so I just made it utils, since they are useful
# and utilities, kinda. Shared functionality among classes can be
# found here.
######################################################################

import pygame
from pygame.locals import *

######################################################################
# Author: Matias Grioni
# Created: 7/12/15
#
# Classes which need to handle events should inherit this class. This
# stores the handlers, arguments as values and the event info as a key
# in a dictionary. So when an event is passed through _handleEvent
# the necessary callback is used.
######################################################################
class EventHandler(object):
    def __init__(self):
        self.eventCallbacks = {}

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
    # for an event. Args are the arguments to provide to the callback
    # and kwargs are the named arguments, following convention.
    def addEventCallback(self, event, callback, *args, **kwargs):
        self.eventCallbacks[event] = (callback, args, kwargs)

    # Removes the callback for the provided event and returns the
    # previously added callback or None if there was none defined
    # for the event.
    def removeEventCallback(self, event):
        return self.eventCallbacks.pop(event, None)

    # Removes all event listeners
    def clearEventCallbacks(self):
        self.eventCallbacks.clear()

    def handleEvent(self, e):
        # Creates a tuple with the necessary event information based on
        # the parameter. Generates the key for the callback dictionary
        # so we can check if there is a registered callback for this event.
        if e.type in (KEYUP, KEYDOWN):
            info = (e.type, e.key)
        elif e.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
            info = (e.type, e.button)
        elif e.type == MOUSEMOTION:
            info = (e.type, e.buttons)
        else:
            # Info has to be assigned to something.
            info = (None, None)

        # First check if this exact event was defined in the callbacks
        if info in self.eventCallbacks:
            callback = self.eventCallbacks[info]
            self._handleCallback(e, callback)

        # Then check if this event is found in a callback tuple with
        # multiple matching events like (KEYDOWN, (K_ESCAPE, K_UP))
        for key in self.eventCallbacks:
            if type(key[1]) is tuple:
                if info[0] == key[0] and info[1] in key[1]:
                    callback = self.eventCallbacks[key]
                    self._handleCallback(e, callback)

        # Then check if a callback is defined for only the event type
        # and not an event code in that type.
        if (e.type, None) in self.eventCallbacks:
            callback = self.eventCallbacks[(e.type, None)]
            self._handleCallback(e, callback)

    # Calls a function given as a callback tuple in the form
    # (function, *args, **kwargs) and the event to pass to the callback
    def _handleCallback(self, e, callback):
        func = callback[0]
        args = callback[1]
        kwargs = callback[2]

        func(e, *args, **kwargs)

######################################################################
# Author: Matias Grioni
# Created: 7/18/15
#
# A countdown utility. Pass in a specified time in seconds to
# countdown, and a provided callback will be called each second, and
# another callback once the timer has finished. If no callbacks are
# provided then it will merely stall the execution of the program, for
# the specified time.
######################################################################
class Timer(object):
    def __init__(self, s):
        self.s = s

        self.onTick = None
        self.onFinish = None

    # Start the synchronously countdown
    def start(self):
        tmp = self.s

        while tmp > 0:
            self.onTick(tmp)
            tmp -= 1
            pygame.time.delay(1000)

        self.onFinish()
