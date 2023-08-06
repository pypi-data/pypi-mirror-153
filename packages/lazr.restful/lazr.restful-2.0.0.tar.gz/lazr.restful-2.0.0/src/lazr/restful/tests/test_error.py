# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Tests of lazr.restful navigation."""

from pkg_resources import resource_filename
import os
import traceback
import unittest

from van.testing.layer import zcml_layer

from zope.component import getGlobalSiteManager
from zope.interface import Interface

from lazr.restful.declarations import error_status
from lazr.restful._resource import (
    EntryAdapterUtility,
    ReadWriteResource,
    UnknownEntryAdapter,
)
from lazr.restful.error import expose
from lazr.restful.interfaces import IWebServiceLayer, IWebServiceVersion
from lazr.restful.testing.webservice import FakeRequest


class TestResource(ReadWriteResource):
    def __init__(self, callable, request):
        self.callable = callable
        super().__init__(context=None, request=request)

    def do_GET(self):
        return self.callable()


class ExposeTestCase(unittest.TestCase):
    # Test the behavior of the expose() method.

    def test_exposed_does_not_work_on_class(self):
        self.assertRaises(ValueError, expose, Exception)

    def test_default_exposed_status_is_400(self):
        exception = expose(ValueError())
        self.assertEqual(exception.__lazr_webservice_error__, 400)

    def test_expose_can_specify_status(self):
        exception = expose(ValueError(), 409)
        self.assertEqual(exception.__lazr_webservice_error__, 409)


class ErrorsTestCase(unittest.TestCase):
    def setUp(self):
        class MyException(Exception):
            pass

        self.exception_class = MyException
        super().setUp()

    def test_decorated_exception_class_becomes_error_view(self):
        # An exposed exception, when raised, will set the response
        # status code appropriately, and set the response text to the
        # exception body.
        def broken():
            @error_status(404)
            class MyException(Exception):
                pass

            raise MyException("something broke")

        request = FakeRequest(version="trunk")
        resource = TestResource(broken, request)
        result = resource()
        self.assertEqual(request.response.status, 404)
        self.assertTrue(result.startswith("something broke"))

    def test_decorated_exception_instance_becomes_error_view(self):
        # An exposed exception, when raised, will set the response
        # status code appropriately, and set the response text to the
        # exception body.
        def broken():
            error = RuntimeError("something broke")
            error = expose(error, 404)
            raise error

        request = FakeRequest(version="trunk")
        resource = TestResource(broken, request)
        result = resource()
        self.assertEqual(request.response.status, 404)
        self.assertTrue(result.startswith("something broke"))

    def test_undecorated_exception_is_propagated(self):
        # If an undecorated exception (a regular Python exception) is
        # generated during a request the exception percolates all the way out
        # of the resource (to be handled by the publisher).

        def broken():
            raise RuntimeError("something broke")

        request = FakeRequest(version="trunk")
        resource = TestResource(broken, request)
        self.assertRaises(RuntimeError, resource)

    def test_exception_decorated_as_system_error_is_propagated(self):
        # If an exception is decorated with a response code that
        # indicates a server-side problem, the exception percolates
        # all the way out of the resource (to be handled by the
        # publisher).
        def broken():
            raise expose(RuntimeError("something broke"), 503)

        request = FakeRequest(version="trunk")
        resource = TestResource(broken, request)
        self.assertRaises(RuntimeError, resource)
        self.assertEqual(request.response.getStatus(), 503)

    def test_exception_decorated_as_nonerror_is_propagated(self):
        # If an exception is decorated with a response code that
        # indicates a non-error condition, the exception percolates
        # all the way out of the resource (to be handled by the
        # publisher).
        def if_you_say_so():
            raise expose(RuntimeError("everything's fine"), 200)

        request = FakeRequest(version="trunk")
        resource = TestResource(if_you_say_so, request)
        self.assertRaises(RuntimeError, resource)
        self.assertEqual(request.response.getStatus(), 200)

    def _setup_non_web_service_exception(self, exception_class=None):
        if exception_class is None:
            exception_class = self.exception_class

        # Define a method that raises the exception.
        def has_a_view():
            raise exception_class()

        # Register a view for the exception that does not subclass
        # WebServiceExceptionView and provides no information about
        # which HTTP status code should be used.
        class ViewHasNoStatus:
            def __init__(*args):
                pass

        getGlobalSiteManager().registerAdapter(
            ViewHasNoStatus,
            (exception_class, IWebServiceLayer),
            Interface,
            name="index.html",
        )

        # The exception is re-raised, even though a view is registered
        # for it, because the view doesn't give lazr.restful the
        # information it needs to see if it can handle the exception
        # itself.
        request = FakeRequest()
        resource = TestResource(has_a_view, request)
        return resource

    def test_non_web_service_exception_is_reraised(self):
        request = FakeRequest()
        resource = self._setup_non_web_service_exception()
        self.assertRaises(self.exception_class, resource)

        # lazr.restful leaves the status code completely
        # untouched. Handling a view other than a
        # WebServiceExceptionView is the publisher's job.
        self.assertEqual(request.response.getStatus(), 599)

    def test_non_web_service_exception_includes_original_traceback(self):
        # If an exception occurs and it has a view, the original traceback is
        # still shown even though the internals of lazr.restful catch and
        # reraise the exception.
        resource = self._setup_non_web_service_exception()
        try:
            resource()
        except Exception:
            self.assertIn("raise exception_class()", traceback.format_exc())
        else:
            self.fail("No exception raised.")

    def test_passing_bad_things_to_expose(self):
        # The expose function only accepts instances of exceptions.  It
        # generates errors otherwise.
        self.assertRaises(ValueError, expose, 1)
        self.assertRaises(ValueError, expose, "x")
        self.assertRaises(ValueError, expose, RuntimeError)

    def test_missing_adapter(self):
        # If there is no multi-adapter from the entry interface (IMyEntry) and
        # a request to IEntry an exception is raised.
        class IWebServiceTestRequestBeta(IWebServiceVersion):
            pass

        class IMyEntry(Interface):
            pass

        sm = getGlobalSiteManager()
        sm.registerUtility(
            IWebServiceTestRequestBeta, IWebServiceVersion, name="beta"
        )
        self.addCleanup(
            sm.unregisterUtility,
            IWebServiceTestRequestBeta,
            IWebServiceVersion,
            name="beta",
        )
        beta_request = FakeRequest(version="beta")
        # Since the test wants to inspect the exception message (below) we're
        # not using self.assertRaises).
        try:
            EntryAdapterUtility.forSchemaInterface(IMyEntry, beta_request)
        except Exception as e:
            self.assertTrue(isinstance(e, Exception))

            # The exception's message explains what went wrong.
            self.assertEqual(
                "No IEntry adapter found for IMyEntry "
                "(web service version: beta).",
                str(e),
            )
        else:
            self.fail(
                "EntryAdapterUtility.forSchemaInterface did not raise an "
                "exception"
            )

    def test_missing_adapter_whence(self):
        # The UnknownEntryAdapter exception has a "whence" attribute that
        # higher-level code can set to give the reader of the exeption message
        # a hint about where in the code the mistake was made that triggered
        # the exception.
        exception = UnknownEntryAdapter("IInterfaceInQuestion", "2.0")
        exception.whence = "Encounterd as a result of badness in foo.py."
        self.assertEqual(
            str(exception),
            "No IEntry adapter found for IInterfaceInQuestion (web service "
            "version: 2.0).  Encounterd as a result of badness in foo.py.",
        )

    def test_original_traceback_reported_when_undecorated(self):
        # When something goes wrong the original traceback should be
        # displayed, not a traceback representing a place where the exception
        # was caught and reraised.
        def broken():
            raise RuntimeError("something broke")

        request = FakeRequest(version="trunk")
        resource = TestResource(broken, request)
        try:
            resource()
        except Exception:
            self.assertIn(
                'raise RuntimeError("something broke")', traceback.format_exc()
            )
        else:
            self.fail("No exception raised.")

    def test_reporting_original_exception_with_no_traceback(self):
        # Sometimes an exception won't have an __traceback__ attribute.  The
        # re-raising should still work (bug 854695).
        class TracebacklessException(Exception):
            pass

        resource = self._setup_non_web_service_exception(
            exception_class=TracebacklessException
        )
        try:
            resource()
        except AttributeError:
            self.fail(
                "The resource should not have generated an AttributeError. "
                "This is probably because something was expecting the "
                "exception to have a __traceback__ attribute."
            )
        except MemoryError:
            raise
        except Exception:
            self.assertIn("TracebacklessException", traceback.format_exc())
        else:
            self.fail("No exception raised.")


class FunctionalLayer:
    allow_teardown = False
    zcml = os.path.abspath(resource_filename("lazr.restful", "ftesting.zcml"))


zcml_layer(FunctionalLayer)


def load_tests(loader, tests, pattern):
    """See `zope.testing.testrunner`."""
    tests.layer = FunctionalLayer
    return tests
