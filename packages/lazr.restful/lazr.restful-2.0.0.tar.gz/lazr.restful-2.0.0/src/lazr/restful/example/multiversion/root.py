"""The RESTful service root."""

__all__ = [
    "BelowRootAbsoluteURL",
    "RootAbsoluteURL",
    "WebServiceConfiguration",
    "MultiversionWebServiceRootResource",
]

from zope.traversing.browser import AbsoluteURL

from lazr.restful.wsgi import BaseWSGIWebServiceConfiguration
from lazr.restful.simple import RootResource, RootResourceAbsoluteURL
from lazr.restful.example.multiversion.resources import (
    IKeyValuePair,
    PairSet,
    KeyValuePair,
)


class RootAbsoluteURL(RootResourceAbsoluteURL):
    """A technique for generating the service's root URL.

    This class contains no code of its own. It's defined so that
    grok will pick it up.
    """


class BelowRootAbsoluteURL(AbsoluteURL):
    """A technique for generating a root URL given an ILocation.

    This class contains no code of its own. It's defined so that
    grok will pick it up.
    """


class WebServiceConfiguration(BaseWSGIWebServiceConfiguration):
    code_revision = "1"
    active_versions = ["beta", "1.0", "2.0", "3.0", "trunk"]
    first_version_with_total_size_link = "2.0"
    last_version_with_mutator_named_operations = "1.0"
    use_https = False
    view_permission = "zope.Public"


class MultiversionWebServiceRootResource(RootResource):
    """The root resource for the WSGI example web service."""

    def _build_top_level_objects(self):
        pairset = PairSet()
        pairset.pairs = [
            KeyValuePair(pairset, "foo", "bar"),
            KeyValuePair(pairset, "foo2", "bar"),
            KeyValuePair(pairset, "foo3", "bar"),
            KeyValuePair(pairset, "1", "2"),
            KeyValuePair(pairset, "Some", None),
            KeyValuePair(pairset, "Delete", "me"),
            KeyValuePair(pairset, "Also delete", "me"),
        ]
        collections = dict(pairs=(IKeyValuePair, pairset))
        return collections, {}
