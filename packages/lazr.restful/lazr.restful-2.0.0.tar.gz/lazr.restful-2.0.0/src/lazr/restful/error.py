# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Error handling on the webservice."""

__all__ = [
    "ClientErrorView",
    "expose",
    "NotFoundView",
    "RequestExpiredView",
    "SystemErrorView",
    "UnauthorizedView",
    "WebServiceExceptionView",
]

import traceback

from zope.component import getUtility
from zope.interface import implementer

try:
    # This import brings some big ugly dependencies, and is not strictly
    # necessary.
    from zope.app.exception.interfaces import ISystemErrorView
except ImportError:
    from zope.interface import Interface

    class ISystemErrorView(Interface):
        """Error views that can classify their contexts as system errors"""

        def isSystemError():
            """
            Return a boolean indicating whether the error is a system error
            """


from lazr.restful.interfaces import (
    IWebServiceConfiguration,
    IWebServiceExceptionView,
)


@implementer(IWebServiceExceptionView)
class WebServiceExceptionView:
    """Generic view handling exceptions on the web service."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def status(self):
        """The HTTP status to use for the response.

        By default, use the __lazr_webservice_error__ attribute on
        the exception.
        """
        return getattr(self.context, "__lazr_webservice_error__", 500)

    def isSystemError(self):
        """See `ISystemErrorView`."""
        return self.status // 100 == 5

    def __call__(self):
        """Generate the HTTP response describing the exception."""
        response = self.request.response
        response.setStatus(self.status)
        response.setHeader("Content-Type", "text/plain")
        if getattr(self.request, "oopsid", None) is not None:
            response.setHeader("X-Lazr-OopsId", self.request.oopsid)

        show_tracebacks = getUtility(IWebServiceConfiguration).show_tracebacks
        server_error = self.status // 100 == 5
        if not show_tracebacks and server_error:
            # Don't show the exception message; it might contain
            # private information.
            result = [self.context.__class__.__name__]
        else:
            # It's okay to show the exception message
            result = [str(self.context)]

        if show_tracebacks and server_error:
            result.append("\n\n")
            result.append(traceback.format_exc())

        return "".join(result)


# lazr/restful/configure.zcml registers these classes as adapter
# factories for common Zope exceptions.
@implementer(ISystemErrorView)
class ClientErrorView(WebServiceExceptionView):
    """Client-induced error."""

    status = 400


@implementer(ISystemErrorView)
class SystemErrorView(WebServiceExceptionView):
    """Server error."""

    status = 500


class NotFoundView(WebServiceExceptionView):
    """View for NotFound."""

    status = 404


class UnauthorizedView(WebServiceExceptionView):
    """View for Unauthorized exception."""

    status = 401


# This is currently only configured/tested in Launchpad.
class RequestExpiredView(WebServiceExceptionView):
    """View for RequestExpired exception."""

    status = 503


def expose(exception, status=400):
    """
    Tell lazr.restful to deliver details about the exception to the client.
    """
    # Since Python lets us raise exception types without instantiating them
    # (like "raise RuntimeError" instead of "raise RuntimeError()", we want to
    # make sure the caller doesn't get confused and try that with us.
    if not isinstance(exception, BaseException):
        raise ValueError(
            "This function only accepts exception instances. "
            "Use the @error_status decorator to publish an "
            "exception class as a web service error."
        )

    exception.__lazr_webservice_error__ = status

    # Mark the exception to indicate that its details should be sent to the
    # web service client.
    return exception
