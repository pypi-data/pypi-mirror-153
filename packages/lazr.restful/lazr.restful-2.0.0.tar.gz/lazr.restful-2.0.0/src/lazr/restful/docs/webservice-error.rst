Exceptions on the web service
*****************************

Exceptions on the LAZR web service are handled like other exceptions
occurring during zope publication: a view is looked-up and used to
return the response to the client.

=====
Setup
=====

    >>> from zope.component import getSiteManager, getUtility
    >>> from zope.interface import implementer
    >>> from lazr.restful.interfaces import IWebServiceConfiguration
    >>> sm = getSiteManager()
    >>> @implementer(IWebServiceConfiguration)
    ... class SimpleWebServiceConfiguration:
    ...     show_tracebacks = False
    ...     active_versions = ['trunk']
    ...     last_version_with_mutator_named_operations = None
    >>> webservice_configuration = SimpleWebServiceConfiguration()
    >>> sm.registerUtility(webservice_configuration)

    >>> from lazr.restful.interfaces import IWebServiceVersion
    >>> class ITestServiceRequestTrunk(IWebServiceVersion):
    ...     pass
    >>> sm.registerUtility(
    ...     ITestServiceRequestTrunk, IWebServiceVersion, name='trunk')


=======================
WebServiceExceptionView
=======================

WebServiceExcpetionView is a generic view class that can handle
exceptions during web service requests.

    >>> from lazr.restful.error import WebServiceExceptionView

    >>> def render_error_view(error, request):
    ...     """Create a WebServiceExceptionView to render the exception.
    ...
    ...     The exception is raised, because exception view can be expected
    ...     to be called from within an exception handler.
    ...     """
    ...     try:
    ...         raise error
    ...     except Exception as error:
    ...         return WebServiceExceptionView(error, request)()

That view returns the exception message as content, and sets the
result code to the one specified using the webservice_error() directive.

    >>> from lazr.restful.declarations import webservice_error
    >>> class InvalidInput(Exception):
    ...     """Client provided invalid input."""
    ...     webservice_error(400)

Depending on the show_tracebacks setting, it may also print a
traceback of the exception.  Tracebacks are only shown for errors
that have a 5xx http error code.

    >>> from textwrap import dedent
    >>> from lazr.restful.testing.webservice import FakeRequest

    >>> webservice_configuration.show_tracebacks
    False

When tracebacks are not shown, the view simply returns the exception
message and sets the status code to the one related to the exception.

    >>> request = FakeRequest()
    >>> render_error_view(
    ...     InvalidInput("foo@bar isn't a valid email address"), request)
    "foo@bar isn't a valid email address"
    >>> request.response.headers['Content-Type']
    'text/plain'
    >>> request.response.status
    400

When the request contains an OOPSID, it will be set in the X-Lazr-OopsId
header:

    >>> print(request.response.headers.get('X-Lazr-OopsId'))
    None
    >>> request = FakeRequest()
    >>> request.oopsid = 'OOPS-001'
    >>> ignored = render_error_view(InvalidInput('bad email'), request)
    >>> print(request.response.headers['X-Lazr-OopsId'])
    OOPS-001

Even if show_tracebacks is set to true, non-5xx error codes will not
produce a traceback.

    >>> webservice_configuration.show_tracebacks = True
    >>> print(render_error_view(InvalidInput('bad email'), request))
    bad email


Internal server errors
======================

Exceptions that are server-side errors are handled a little
differently.

    >>> class ServerError(Exception):
    ...     """Something went wrong on the server side."""
    ...     webservice_error(500)

If show_tracebacks is True, the user is going to see a full traceback anyway,
so there's no point in hiding the exception message.  When tracebacks are
shown, the view puts a traceback dump in the response.

    >>> print(render_error_view(ServerError('DB crash'), request))
    DB crash
    <BLANKLINE>
    Traceback (most recent call last):
     ...
    ServerError: DB crash

If show_tracebacks is False, on an internal server error they client
will see the exception class name instead of a message.

    >>> webservice_configuration.show_tracebacks = False
    >>> print(render_error_view(ServerError('DB crash'), request))
    ServerError


==================
Default exceptions
==================

Standard exceptions have a view registered for them by default.

    >>> from zope.configuration import xmlconfig
    >>> zcmlcontext = xmlconfig.string("""
    ... <configure xmlns="http://namespaces.zope.org/zope">
    ...   <include package="lazr.restful" file="basic-site.zcml"/>
    ... </configure>
    ... """)

    >>> from zope.component import getMultiAdapter
    >>> def render_using_default_view(error):
    ...     """Render an exception using its default 'index.html' view.
    ...     :return: response, result tuple. (The response object and
    ...         the content).
    ...     """
    ...     try:
    ...         raise error
    ...     except Exception as error:
    ...         request = FakeRequest()
    ...         view = getMultiAdapter((error, request), name="index.html")
    ...         result = view()
    ...         return request.response, result


NotFound exceptions have a 404 status code.

    >>> from zope.publisher.interfaces import NotFound
    >>> response, result = render_using_default_view(
    ...     NotFound(object(), 'name'))
    >>> response.status
    404

Unauthorized exceptions have a 401 status code.

    >>> from zope.security.interfaces import Unauthorized
    >>> response, result = render_using_default_view(Unauthorized())
    >>> response.status
    401

Other exceptions have the 500 status code.

    >>> response, result = render_using_default_view(Exception())
    >>> response.status
    500
