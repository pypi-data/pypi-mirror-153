# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Test harness for LAZR doctests."""

__all__ = []

import os
import doctest
from pkg_resources import resource_filename

from van.testing.layer import zcml_layer, wsgi_intercept_layer
from zope.testing import renormalizing

from lazr.restful.example.base.root import CookbookServiceRootResource
from lazr.restful.testing.webservice import (
    WebServiceTestPublication,
    WebServiceApplication,
)


class CookbookWebServiceTestPublication(WebServiceTestPublication):
    def getApplication(self, request):
        return CookbookServiceRootResource()


DOCTEST_FLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
)


checker = renormalizing.OutputChecker()


class FunctionalLayer:
    allow_teardown = False
    zcml = os.path.abspath(resource_filename("lazr.restful", "ftesting.zcml"))


zcml_layer(FunctionalLayer)


class WSGILayer(FunctionalLayer):
    @classmethod
    def make_application(self):
        return WebServiceApplication({}, CookbookWebServiceTestPublication)


wsgi_intercept_layer(WSGILayer)


def load_tests(loader, tests, pattern):
    """See `zope.testing.testrunner`."""
    doctest_files = sorted(
        name
        for name in os.listdir(os.path.dirname(__file__))
        if name.endswith(".txt")
    )
    suite = doctest.DocFileSuite(
        *doctest_files,
        optionflags=DOCTEST_FLAGS,
        encoding="UTF-8",
        checker=checker,
    )
    suite.layer = WSGILayer
    tests.addTest(suite)
    return tests
