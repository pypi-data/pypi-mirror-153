# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Tests of lazr.restful navigation."""

import unittest

from zope.component import (
    ComponentLookupError,
    getMultiAdapter,
    getSiteManager,
)
from zope.interface import (
    alsoProvides,
    Interface,
    implementer,
)
from zope.publisher.interfaces import NotFound
from zope.schema import Text
from zope.testing.cleanup import cleanUp

from lazr.restful.fields import Reference
from lazr.restful.interfaces import (
    IEntry,
    IWebServiceClientRequest,
)
from lazr.restful.simple import Publication
from lazr.restful.testing.webservice import FakeRequest


class IChild(Interface):
    """Interface for a simple entry."""

    one = Text(title="One")
    two = Text(title="Two")


class IParent(Interface):
    """Interface for a simple entry that contains another entry."""

    three = Text(title="Three")
    child = Reference(schema=IChild)


@implementer(IChild)
class Child:
    """A simple implementation of IChild."""

    one = "one"
    two = "two"


class ChildEntry:
    """Implementation of an entry wrapping a Child."""

    schema = IChild

    def __init__(self, context, request):
        self.context = context


@implementer(IParent)
class Parent:
    """A simple implementation of IParent."""

    three = "three"
    child = Child()


class ParentEntry:
    """Implementation of an entry wrapping a Parent, containing a Child."""

    schema = IParent

    def __init__(self, context, request):
        self.context = context

    @property
    def child(self):
        return self.context.child


class FakeRequestWithEmptyTraversalStack(FakeRequest):
    """A fake request satisfying `traverseName()`."""

    def getTraversalStack(self):
        return ()


class NavigationTestCase(unittest.TestCase):
    def setUp(self):
        # Register ChildEntry as the IEntry implementation for IChild.
        sm = getSiteManager()
        sm.registerAdapter(
            ChildEntry, [IChild, IWebServiceClientRequest], provided=IEntry
        )

        # Register ParentEntry as the IEntry implementation for IParent.
        sm.registerAdapter(
            ParentEntry, [IParent, IWebServiceClientRequest], provided=IEntry
        )

    def tearDown(self):
        cleanUp()

    def test_toplevel_navigation(self):
        # Test that publication can reach sub-entries.
        publication = Publication(None)
        request = FakeRequestWithEmptyTraversalStack(version="trunk")
        obj = publication.traverseName(request, Parent(), "child")
        self.assertEqual(obj.one, "one")

    def test_toplevel_navigation_without_subentry(self):
        # Test that publication raises NotFound when subentry attribute
        # returns None.
        request = FakeRequestWithEmptyTraversalStack(version="trunk")
        parent = Parent()
        parent.child = None
        publication = Publication(None)
        self.assertRaises(
            NotFound, publication.traverseName, request, parent, "child"
        )

    def test_getResource_ComponentLookupError_NotFound(self):
        # Test that ComponentLookupError becomes NotFound.
        # IEntry objects may not be adaptable to a resource if
        # the underlying object cannot be found.
        class IOrphan(Interface):
            pass

        class OrphanEntry:
            schema = IOrphan

            def __init__(self):
                alsoProvides(self, IEntry)

        publication = Publication(None)
        request = FakeRequestWithEmptyTraversalStack(version="trunk")
        entry_obj = OrphanEntry()
        self.assertRaises(
            ComponentLookupError, getMultiAdapter, (entry_obj, request), IEntry
        )
        self.assertRaises(
            NotFound, publication.getResource, request, entry_obj
        )
