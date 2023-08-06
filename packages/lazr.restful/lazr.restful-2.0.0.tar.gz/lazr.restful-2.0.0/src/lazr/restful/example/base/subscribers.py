# Copyright 2009 Canonical Ltd.  All rights reserved.

"""Event listeners for the example web service."""

__all__ = ["update_cookbook_revision_number"]

import grokcore.component
from lazr.lifecycle.interfaces import IObjectModifiedEvent
from lazr.restful.example.base.interfaces import ICookbook


@grokcore.component.subscribe(ICookbook, IObjectModifiedEvent)
def update_cookbook_revision_number(object, event):
    """Increment ICookbook.revision_number."""
    if ICookbook.providedBy(object):
        object.revision_number += 1
