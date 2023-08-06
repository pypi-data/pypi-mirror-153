# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Testing helpers for webservice unit tests."""

__all__ = [
    "create_web_service_request",
    "StubAbsoluteURL",
    "StubRootResourceURL",
    "FakeRequest",
    "FakeResponse",
    "IGenericEntry",
    "IGenericCollection",
    "pprint_collection",
    "pprint_entry",
    "simple_renderer",
    "WebServiceTestCase",
    "WebServiceTestConfiguration",
    "WebServiceTestPublication",
]

from collections import OrderedDict
from email.utils import quote as email_quote
import io
import random
import re
import simplejson
import sys
from types import ModuleType
import unittest
from urllib.parse import (
    quote,
    urljoin,
)

import wsgi_intercept

from zope.component import adapter, getGlobalSiteManager, getUtility
from zope.configuration import xmlconfig
from zope.interface import alsoProvides, implementer, Interface
from zope.publisher.interfaces.http import IHTTPApplicationRequest
from zope.publisher.paste import Application
from zope.proxy import ProxyBase
from zope.schema import TextLine
from zope.security.checker import ProxyFactory
from zope.security.interfaces import Unauthorized
from zope.testing.cleanup import CleanUp
from zope.traversing.browser.interfaces import IAbsoluteURL

from lazr.restful.declarations import (
    collection_default_content,
    exported,
    exported_as_webservice_collection,
    exported_as_webservice_entry,
    export_read_operation,
    operation_parameters,
)
from lazr.restful.interfaces import (
    IServiceRootResource,
    IWebServiceClientRequest,
    IWebServiceConfiguration,
    IWebServiceLayer,
    IWebServiceVersion,
)
from lazr.restful.simple import (
    BaseWebServiceConfiguration,
    Publication,
    Request,
    RootResourceAbsoluteURL,
    ServiceRootResource,
)
from lazr.restful.utils import tag_request_with_version_name


def create_web_service_request(
    path_info, method="GET", body=None, environ=None, hostname=None
):
    """Create a web service request object with the given parameters.

    :param path_info: The path portion of the requested URL.
    :hostname: The hostname portion of the requested URL. Defaults to
    the value specified in the configuration object.
    :param method: The HTTP method to use.
    :body: The HTTP entity-body to submit.
    :environ: The environment of the created request.
    """
    config = getUtility(IWebServiceConfiguration)
    if hostname is None:
        hostname = config.hostname
    test_environ = {
        "SERVER_URL": "http://%s" % hostname,
        "HTTP_HOST": hostname,
        "PATH_INFO": path_info,
        "REQUEST_METHOD": method,
    }
    if environ is not None:
        test_environ.update(environ)
    if body is None:
        body_instream = io.BytesIO(b"")
    else:
        test_environ["CONTENT_LENGTH"] = len(body)
        body_instream = io.BytesIO(body)
    request = config.createRequest(body_instream, test_environ)

    request.processInputs()
    # This sets the request as the current interaction.
    request.publication.beforeTraversal(request)
    return request


class FakeResponse:
    """Simple response wrapper object."""

    def __init__(self):
        self.reset()

    def setStatus(self, new_status):
        self.status = new_status

    def setHeader(self, name, value):
        self.headers[name] = value

    def getHeader(self, name):
        """Return the value of the named header."""
        return self.headers.get(name)

    def getStatus(self):
        """Return the response status code."""
        return self.status

    def reset(self):
        """Set response values back to their initial state."""
        self.status = 599
        self.headers = {}
        self.result = ""

    def setResult(self, result):
        if result is None:
            result = ""

        if not isinstance(result, str):
            raise ValueError("only strings and None results are handled")

        self.result = result


@implementer(IHTTPApplicationRequest, IWebServiceLayer)
class FakeRequest:
    """Simple request object for testing purpose."""

    # IHTTPApplicationRequest makes us eligible for
    # get_current_browser_request()

    def __init__(self, traversed=None, stack=None, version=None):
        if version is None:
            config = getUtility(IWebServiceConfiguration)
            version = config.active_versions[-1]
        self.version = version
        self._traversed_names = traversed
        self._stack = stack
        self.response = FakeResponse()
        self.principal = None
        self.interaction = None
        self.traversed_objects = []
        self.query_string_params = {}
        self.method = "GET"
        self.URL = "http://api.example.org/"
        self.headers = {}

    def getTraversalStack(self):
        """See `IPublicationRequest`.

        This method is called by traversal machinery.
        """
        return self._stack

    def setTraversalStack(self, stack):
        """See `IPublicationRequest`.

        This method is called by traversal machinery.
        """
        self._stack = stack

    def getApplicationURL(self):
        return "http://api.example.org"

    def get(self, key, default=None):
        """Simulate an empty set of request parameters."""
        return default


def pformat_value(value):
    """Pretty-format a single value.

    This is similar to `repr()`, but for doctest compatibility we format
    values in a way that is unambiguous across Python versions.
    """
    if isinstance(value, OrderedDict):
        # WebServiceResponseWrapper.jsonBody turns JSON objects into
        # OrderedDicts, but for doctest compatibility we just want to
        # re-sort and render these as if they were ordinary dicts.
        return (
            "{"
            + ", ".join(
                "%s: %s" % (pformat_value(k), pformat_value(v))
                for k, v in sorted(value.items())
            )
            + "}"
        )
    else:
        return repr(value)


def pprint_entry(json_body):
    """Pretty-print a webservice entry JSON representation.

    Omits the http_etag key, which is always present and never
    interesting for a test.
    """
    for key, value in sorted(json_body.items()):
        if key != "http_etag":
            print("%s: %s" % (key, pformat_value(value)))


def pprint_collection(json_body):
    """Pretty-print a webservice collection JSON representation."""
    for key, value in sorted(json_body.items()):
        if key == "total_size_link":
            continue
        if key != "entries":
            print("%s: %s" % (key, pformat_value(value)))
    print("---")
    for entry in json_body["entries"]:
        pprint_entry(entry)
        print("---")


class WebServiceTestPublication(Publication):
    """Test publication that mixes in the necessary web service stuff."""

    def wrapTraversedObject(self, ob):
        return ProxyFactory(ob)


class WebServiceApplication(Application):
    """A WSGI application for the tests."""

    def __init__(self, global_config, publication, **options):
        if isinstance(publication, str):
            Application.__init__(self, global_config, publication, **options)
        else:
            self.publication = publication(global_config, **options)

    def request(self, environ):
        return Request(environ["wsgi.input"], environ)


class WebServiceCaller:
    """A class for making calls to lazr.restful web services."""

    def __init__(
        self, handle_errors=True, domain="localhost", protocol="http"
    ):
        """Create a WebServiceCaller.
        :param handle_errors: Should errors raise exception or be handled by
            the publisher. Default is to let the publisher handle them.
        """
        self.domain = domain
        self.protocol = protocol
        self.handle_errors = handle_errors
        self.connection = wsgi_intercept.WSGI_HTTPConnection("localhost")

    @property
    def base_url(self):
        return "%s://%s/" % (self.protocol, self.domain)

    @property
    def default_api_version(self):
        return getUtility(IWebServiceConfiguration).active_versions[-1]

    def getAbsoluteUrl(self, resource_path, api_version=None):
        """Convenience method for creating a url in tests.

        :param resource_path: This is the url section to be joined to hostname
                              and api version.
        :param api_version: This is the first part of the absolute
                            url after the hostname.
        """
        api_version = api_version or self.default_api_version
        if resource_path.startswith("/"):
            # Prevent os.path.join() from interpreting resource_path as an
            # absolute url. This allows paths that appear consistent with urls
            # from other virtual hosts.
            # For example:
            #   /firefox = http://foo.dev/firefox
            #   /firefox = http://api.foo.dev/beta/firefox
            resource_path = resource_path[1:]
        url_with_version = "/".join((api_version, resource_path))
        return urljoin(self.base_url, url_with_version)

    def addHeadersTo(self, url, headers):
        """Add any neccessary headers to the request.

        For instance, this is where a subclass might create an OAuth
        signature for a request.

        :param: The headers that will go into the HTTP request. Modify
        this value in place.
        """

    def __call__(
        self,
        path_or_url,
        method="GET",
        data=None,
        headers=None,
        api_version=None,
    ):
        if isinstance(path_or_url, bytes):
            path_or_url = path_or_url.decode()
        else:
            path_or_url = str(path_or_url)
        if path_or_url.startswith("/"):
            api_version = api_version or self.default_api_version
            full_url = "/".join([api_version, path_or_url])
        else:
            base_url = self.base_url
            if not path_or_url.startswith(base_url):
                raise ValueError(
                    "not a testing url "
                    "(maybe you wanted a relative url but left off the "
                    "preceding slash?)",
                    path_or_url,
                )
            else:
                # The base_url ends with a slash. We want that slash to begin
                # the path, so we cut off the length of the base_url minus one
                # character.
                full_url = path_or_url[len(base_url) - 1 :]
        full_headers = {"Host": self.domain}
        if headers is not None:
            full_headers.update(headers)
        self.addHeadersTo(full_url, full_headers)  # a hook
        self.connection.request(method, full_url, data, full_headers)
        return WebServiceResponseWrapper(self.connection.getresponse())

    def get(
        self,
        path,
        media_type="application/json",
        headers=None,
        api_version=None,
    ):
        """Make a GET request."""
        full_headers = {"Accept": media_type}
        if headers is not None:
            full_headers.update(headers)
        return self(path, "GET", headers=full_headers, api_version=api_version)

    def head(self, path, headers=None, api_version=None):
        """Make a HEAD request."""
        return self(path, "HEAD", headers=headers, api_version=api_version)

    def delete(self, path, headers=None, api_version=None):
        """Make a DELETE request."""
        return self(path, "DELETE", headers=headers, api_version=api_version)

    def put(self, path, media_type, data, headers=None, api_version=None):
        """Make a PUT request."""
        return self._make_request_with_entity_body(
            path, "PUT", media_type, data, headers, api_version=api_version
        )

    def post(self, path, media_type, data, headers=None, api_version=None):
        """Make a POST request."""
        return self._make_request_with_entity_body(
            path, "POST", media_type, data, headers, api_version=api_version
        )

    def _makeBoundary(self, all_parts):
        """Make a random boundary that does not appear in `all_parts`."""
        _width = len(repr(sys.maxsize - 1))
        _fmt = "%%0%dd" % _width
        token = random.randrange(sys.maxsize)
        boundary = ("=" * 15) + (_fmt % token) + "=="
        if all_parts is None:
            return boundary
        b = boundary
        counter = 0
        while True:
            pattern = ("^--" + re.escape(b) + "(--)?$").encode("ascii")
            if not re.search(pattern, all_parts, flags=re.MULTILINE):
                break
            b = boundary + "." + str(counter)
            counter += 1
        return b

    def _writeHeaders(self, buf, headers):
        """Write MIME headers to a file object."""
        for key, value in headers:
            buf.write(key.encode())
            buf.write(b": ")
            buf.write(value.encode())
            buf.write(b"\r\n")
        buf.write(b"\r\n")

    def _writeBoundary(self, buf, boundary, closing=False):
        """Write a multipart boundary to a file object."""
        buf.write(b"--")
        buf.write(boundary.encode())
        if closing:
            buf.write(b"--")
        buf.write(b"\r\n")

    def _convertArgs(self, args):
        """Encode and convert keyword arguments to multipart/form-data.

        This is very loosely based on the email module in the Python
        standard library.  However, that module doesn't really support
        directly embedding binary data in a form: various versions of Python
        have mangled line separators in different ways, and none of them get
        it quite right.  Since we only need a tiny subset of MIME here, it's
        easier to implement it ourselves.

        Binary argument values are supported, but must be passed as
        instances of `io.BufferedIOBase` (e.g. `io.BytesIO`).

        :return: a tuple of two elements: the Content-Type of the message,
            and the entire encoded message as a byte string.
        """
        # Generate the subparts first so that we can calculate a safe boundary.
        encoded_parts = []
        for name, value in args.items():
            buf = io.BytesIO()
            if isinstance(value, io.BufferedIOBase):
                ctype = "application/octet-stream"
                # RFC 7578 says that the filename parameter isn't mandatory
                # in our case, but zope.publisher only considers a field to
                # be a file upload if a filename was passed in.
                cdisp = 'form-data; name="%s"; filename="%s"' % (
                    email_quote(name),
                    email_quote(name),
                )
            else:
                ctype = 'text/plain; charset="utf-8"'
                cdisp = 'form-data; name="%s"' % email_quote(name)
            self._writeHeaders(
                buf,
                [
                    ("MIME-Version", "1.0"),
                    ("Content-Type", ctype),
                    ("Content-Disposition", cdisp),
                ],
            )
            if isinstance(value, io.BufferedIOBase):
                buf.write(value.read())
            else:
                if not isinstance(value, str):
                    value = simplejson.dumps(value)
                lines = re.split(r"\r\n|\r|\n", value)
                for line in lines[:-1]:
                    buf.write(line.encode())
                    buf.write(b"\r\n")
                buf.write(lines[-1].encode())
            encoded_parts.append(buf.getvalue())

        # Create a suitable boundary.
        boundary = self._makeBoundary(b"\r\n".join(encoded_parts))

        # Now we can write the multipart headers, followed by all the parts.
        buf = io.BytesIO()
        self._writeHeaders(buf, [])
        for encoded_part in encoded_parts:
            self._writeBoundary(buf, boundary)
            buf.write(encoded_part)
            buf.write(b"\r\n")
        self._writeBoundary(buf, boundary, closing=True)

        media_type = 'multipart/form-data; boundary="%s"' % email_quote(
            boundary
        )
        return media_type, buf.getvalue()

    def named_get(
        self,
        path_or_url,
        operation_name,
        headers=None,
        api_version=None,
        **kwargs
    ):
        kwargs["ws.op"] = operation_name
        data = "&".join(
            [
                "%s=%s" % (key, self._quote_value(value))
                for key, value in kwargs.items()
            ]
        )
        return self.get(
            "%s?%s" % (path_or_url, data),
            data,
            headers,
            api_version=api_version,
        )

    def named_post(
        self, path, operation_name, headers=None, api_version=None, **kwargs
    ):
        kwargs["ws.op"] = operation_name
        media_type, data = self._convertArgs(kwargs)
        return self.post(
            path, media_type, data, headers, api_version=api_version
        )

    def patch(self, path, media_type, data, headers=None, api_version=None):
        """Make a PATCH request."""
        return self._make_request_with_entity_body(
            path, "PATCH", media_type, data, headers, api_version=api_version
        )

    def _quote_value(self, value):
        """Quote a value for inclusion in a named GET.

        This may mean turning the value into a JSON string.
        """
        if not isinstance(value, str):
            value = simplejson.dumps(value)
        return quote(value)

    def _make_request_with_entity_body(
        self, path, method, media_type, data, headers, api_version
    ):
        """A helper method for requests that include an entity-body.

        This means PUT, PATCH, and POST requests.
        """
        real_headers = {"Content-type": media_type}
        if headers is not None:
            real_headers.update(headers)
        return self(path, method, data, real_headers, api_version=api_version)


class WebServiceAjaxCaller(WebServiceCaller):
    """A caller that introduces the Ajax path override to the URI prefix."""

    @property
    def default_api_version(self):
        """Introduce the Ajax path override to the URI prefix."""
        config = getUtility(IWebServiceConfiguration)
        default_version = super().default_api_version
        return config.path_override + "/" + default_version


class WebServiceResponseWrapper(ProxyBase):
    """A response from the web service with easy access to the JSON body."""

    def __init__(self, response):
        self.body = response.read()
        super().__init__(response)

    def getHeader(self, key, default=None):
        return self.getheader(key, default)

    def __str__(self):
        def normalize(key):
            """Normalize an HTTP header name to title case."""
            return "-".join(s.title() for s in key.split("-"))

        headers = [
            "%s: %s\n" % (normalize(key), value)
            for key, value in self.msg.items()
        ]
        body = self.body.decode("UTF-8")
        return "HTTP/1.1 %s %s\n%s\n%s" % (
            self.status,
            self.reason,
            "".join(headers),
            body,
        )

    def jsonBody(self):
        """Return the body of the web service request as a JSON document."""
        body = self.body
        if isinstance(body, bytes):
            body = body.decode()
        try:
            return simplejson.loads(body, object_pairs_hook=OrderedDict)
        except ValueError:
            # Return a useful ValueError that displays the problematic
            # string, instead of one that just says the string wasn't
            # JSON.
            raise ValueError(body)


@implementer(IWebServiceConfiguration)
class WebServiceTestConfiguration(BaseWebServiceConfiguration):
    """A simple configuration for tests that need a running web service."""

    show_tracebacks = False
    active_versions = ["1.0", "2.0"]
    hostname = "webservice_test"
    last_version_with_mutator_named_operations = None
    _scopes = None

    def createRequest(self, body_instream, environ):
        request = Request(body_instream, environ)
        request.setPublication(
            WebServiceTestPublication(getUtility(IServiceRootResource))
        )
        tag_request_with_version_name(request, "2.0")
        return request

    def checkRequest(self, obj, required_scopes):
        if self._scopes is not None:
            if not required_scopes:
                raise Unauthorized(
                    "Current authentication only allows calling "
                    "scoped methods."
                )
            elif not any(scope in required_scopes for scope in self._scopes):
                raise Unauthorized(
                    "Current authentication does not allow calling "
                    "this method (one of these scopes is required: "
                    "%s)."
                    % ", ".join("'%s'" % scope for scope in required_scopes)
                )


class IWebServiceTestRequest10(IWebServiceClientRequest):
    """A marker interface for requests to the '1.0' web service."""


class IWebServiceTestRequest20(IWebServiceClientRequest):
    """A marker interface for requests to the '2.0' web service."""


class TestCaseWithWebServiceFixtures(CleanUp, unittest.TestCase):
    """A test case that needs to have some aspects of a web service set up.

    If the test case is testing a real web service, use
    WebServiceTestCase instead.
    """

    def setUp(self):
        super().setUp()
        # Register a simple configuration object.
        webservice_configuration = WebServiceTestConfiguration()
        sm = getGlobalSiteManager()
        sm.registerUtility(webservice_configuration)

        # Register IWebServiceVersions for the
        # '1.0' and '2.0' web service versions.
        alsoProvides(IWebServiceTestRequest10, IWebServiceVersion)
        sm.registerUtility(
            IWebServiceTestRequest10, IWebServiceVersion, name="1.0"
        )
        alsoProvides(IWebServiceTestRequest20, IWebServiceVersion)
        sm.registerUtility(
            IWebServiceTestRequest20, IWebServiceVersion, name="2.0"
        )

    def assertRaises(self, excClass, callableObj, *args, **kwargs):
        """Fail unless an exception of class excClass is thrown
        by callableObj when invoked with arguments args and keyword
        arguments kwargs. If a different type of exception is
        thrown, it will not be caught, and the test case will be
        deemed to have suffered an error, exactly as for an
        unexpected exception.

        This is a copy of assertRaises from testtools.
        """
        try:
            ret = callableObj(*args, **kwargs)
        except excClass:
            return sys.exc_info()[1]
        else:
            excName = self._formatTypes(excClass)
            self.fail("%s not raised, %r returned instead." % (excName, ret))

    def _formatTypes(self, classOrIterable):
        """Format a class or a bunch of classes for display in an error.

        This is a copy of _formatTypes from testtools.
        """
        className = getattr(classOrIterable, "__name__", None)
        if className is None:
            className = ", ".join(klass.__name__ for klass in classOrIterable)
        return className

    def fake_request(self, version):
        request = FakeRequest(version=version)
        alsoProvides(request, getUtility(IWebServiceVersion, name=version))
        return request


class WebServiceTestCase(TestCaseWithWebServiceFixtures):
    """A test case for web service operations."""

    testmodule_objects = []

    def setUp(self):
        """Set the component registry with the given model."""
        super().setUp()

        # Register a service root resource
        sm = getGlobalSiteManager()
        service_root = ServiceRootResource()
        sm.registerUtility(service_root, IServiceRootResource)

        # Register an IAbsoluteURL adapter for the service root resource.
        sm.registerAdapter(
            RootResourceAbsoluteURL,
            [IServiceRootResource, IWebServiceClientRequest],
            IAbsoluteURL,
        )

        # Build a test module that exposes the given resource interfaces.
        testmodule = ModuleType("testmodule")
        for interface in self.testmodule_objects:
            setattr(testmodule, interface.__name__, interface)
        sys.modules["lazr.restful.testmodule"] = testmodule

        # Register the test module in the ZCML configuration: adapter
        # classes will be built automatically.
        xmlconfig.string(
            """
        <configure
           xmlns="http://namespaces.zope.org/zope"
           xmlns:webservice="http://namespaces.canonical.com/webservice">
         <include package="zope.component" file="meta.zcml" />
         <include package="zope.security" file="meta.zcml"/>
         <include package="lazr.restful" file="meta.zcml" />
         <include package="lazr.restful" file="configure.zcml" />

        <adapter for="*"
            factory="zope.traversing.adapters.DefaultTraversable"
            provides="zope.traversing.interfaces.ITraversable" />

        <webservice:register module="lazr.restful.testmodule" />
        </configure>
        """
        )


@exported_as_webservice_entry()
class IGenericEntry(Interface):
    """A simple, reusable entry interface for use in tests.

    The entry publishes one field and one named operation.
    """

    # pylint: disable-msg=E0213
    a_field = exported(
        TextLine(
            title='A "field"',
            description="The only field that can be <> 0 in the entry.",
        )
    )

    @operation_parameters(message=TextLine(title="Message to say"))
    @export_read_operation()
    def greet(message):
        """Print an appropriate greeting based on the message.

        :param message: This will be included in the greeting.
        """


@exported_as_webservice_collection(IGenericEntry)
class IGenericCollection(Interface):
    """A simple collection containing `IGenericEntry`, for use in tests."""

    # pylint: disable-msg=E0211
    @collection_default_content()
    def getAll():
        """Returns all the entries."""


@implementer(IServiceRootResource)
class StubRootResource:
    """A root resource that does nothing."""

    def getTopLevelPublications(self, request):
        return {}


@implementer(IAbsoluteURL)
class StubAbsoluteURL:
    """Implements IAbsoluteURL for when you don't care what the URL is."""

    URL = "http://exampleurl/"

    def __init__(self, *args):
        pass

    def __str__(self):
        return self.URL

    __call__ = __str__


@adapter(StubRootResource, IWebServiceClientRequest)
class StubRootResourceURL(StubAbsoluteURL):
    """A stub IAbsoluteURL implementation for a StubRootResource."""

    URL = "http://exampleurl"


def simple_renderer(value):
    """Bold the original string and add a snowman.

    To use this function, define an IHTMLFieldRenderer that returns it.

    This is a good HTML field renderer to use in tests, because it
    tests Unicode values and embedded HTML.
    """
    return "\N{SNOWMAN} <b>%s</b>" % value
