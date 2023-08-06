# Copyright 2006 Canonical Ltd.  All rights reserved.

"""Helper class for checking the event notifications."""

import zope.component


class TestEventListener:
    """Listen for a specific object event in tests.

    When an event of the specified type is fired off for an object with
    the specifed type, the given callback is called.

    The callback function should take an object and an event.

    At the end of the test you have to unregister the event listener
    using event_listener.unregister().
    """

    def __init__(self, object_type, event_type, callback):
        self.object_type = object_type
        self.event_type = event_type
        self.callback = callback
        sm = zope.component.getGlobalSiteManager()
        sm.registerHandler(self, (object_type, event_type), event=False)

    def __call__(self, object, event):
        self.callback(object, event)

    def unregister(self):
        """Stop the event listener from listening to events."""
        sm = zope.component.getGlobalSiteManager()
        sm.unregisterHandler(self, (self.object_type, self.event_type))
