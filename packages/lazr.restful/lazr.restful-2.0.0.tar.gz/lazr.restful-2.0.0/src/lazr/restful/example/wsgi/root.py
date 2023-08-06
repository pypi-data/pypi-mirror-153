"""The RESTful service root."""

__all__ = [
    "BelowRootAbsoluteURL",
    "RootAbsoluteURL",
    "WebServiceConfiguration",
    "WSGIExampleWebServiceRootResource",
]

from zope.traversing.browser import AbsoluteURL

from lazr.restful.example.wsgi.resources import (
    IKeyValuePair,
    PairSet,
    KeyValuePair,
)
from lazr.restful.wsgi import BaseWSGIWebServiceConfiguration
from lazr.restful.simple import RootResource, RootResourceAbsoluteURL


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
    active_versions = ["1.0"]
    use_https = False
    last_version_with_mutator_named_operations = None
    view_permission = "zope.Public"


class WSGIExampleWebServiceRootResource(RootResource):
    """The root resource for the WSGI example web service."""

    def _build_top_level_objects(self):
        pairset = PairSet()
        pairset.pairs = [
            KeyValuePair(self, "foo", "bar"),
            KeyValuePair(self, "1", "2"),
        ]
        collections = dict(pairs=(IKeyValuePair, pairset))
        return collections, {}
