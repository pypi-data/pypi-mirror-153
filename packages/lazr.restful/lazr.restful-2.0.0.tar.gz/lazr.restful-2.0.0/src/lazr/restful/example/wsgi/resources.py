__all__ = ["IKeyValuePair", "IPairSet", "KeyValuePair", "PairSet"]

from zope.component import getUtility
from zope.interface import implementer
from zope.schema import Text
from zope.location.interfaces import ILocation

from lazr.restful.declarations import (
    collection_default_content,
    exported,
    exported_as_webservice_collection,
    exported_as_webservice_entry,
)
from lazr.restful.interfaces import IServiceRootResource
from lazr.restful.simple import TraverseWithGet


@exported_as_webservice_entry()
class IKeyValuePair(ILocation):
    key = exported(Text(title="The key"))
    value = exported(Text(title="The value"))


@exported_as_webservice_collection(IKeyValuePair)
class IPairSet(ILocation):
    @collection_default_content()
    def getPairs():
        """Return the key-value pairs."""

    def get(request, name):
        """Retrieve a key-value pair by its key."""


@implementer(IKeyValuePair, ILocation)
class KeyValuePair:
    """An object representing a key-value pair"""

    def __init__(self, set, key, value):
        self.set = set
        self.key = key
        self.value = value

    # ILocation implementation
    @property
    def __parent__(self):
        return self.set

    @property
    def __name__(self):
        return self.key


@implementer(IPairSet, ILocation)
class PairSet(TraverseWithGet):
    """A repository for key-value pairs."""

    def __init__(self):
        self.pairs = []

    def getPairs(self):
        return self.pairs

    def get(self, request, name):
        pairs = [pair for pair in self.pairs if pair.key == name]
        if len(pairs) == 1:
            return pairs[0]
        return None

    # ILocation implementation
    @property
    def __parent__(self):
        return getUtility(IServiceRootResource)

    @property
    def __name__(self):
        return "pairs"
