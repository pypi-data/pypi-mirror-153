"""A WSGI application for a lazr.restful web service."""

__all__ = [
    "BaseWSGIWebServiceConfiguration",
    "WSGIApplication",
]

from pkg_resources import resource_string
from wsgiref.simple_server import make_server as wsgi_make_server

from zope.component import getUtility
from zope.configuration import xmlconfig
from zope.publisher.publish import publish

from lazr.restful.interfaces import (
    IWebServiceConfiguration,
    IServiceRootResource,
)
from lazr.restful.simple import (
    BaseWebServiceConfiguration,
    Publication,
    Request,
)


class WSGIApplication:

    request_class = Request
    publication_class = Publication

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        environ = self.environ
        # Create the request.
        service_root = getUtility(IServiceRootResource)
        request = self.request_class(environ["wsgi.input"], environ)
        request.setPublication(self.publication_class(service_root))
        # Support post-mortem debugging.
        handle_errors = environ.get("wsgi.handleErrors", True)
        # The request returned by the publisher may in fact be different than
        # the one passed in.
        request = publish(request, handle_errors=handle_errors)
        # Start the WSGI server response.
        response = request.response
        self.start_response(response.getStatusString(), response.getHeaders())
        # Return the result body iterable.
        return iter(response.consumeBodyIter())

    @classmethod
    def configure_server(
        cls, host, port, config_package, config_file="site.zcml"
    ):
        """Configure lazr.restful for a particular web service."""
        zcml = resource_string(config_package, config_file)
        xmlconfig.string(zcml)
        config = getUtility(IWebServiceConfiguration)
        config.hostname = host
        config.port = port

    @classmethod
    def make_server(cls, host, port, config_package, config_file="site.zcml"):
        """Create a WSGI server object for a particular web service."""
        cls.configure_server(host, port, config_package, config_file)
        return wsgi_make_server(host, int(port), cls)


class BaseWSGIWebServiceConfiguration(BaseWebServiceConfiguration):
    """A basic web service configuration optimized for WSGI apps.

    There is no difference between this and the default
    WebServiceConfiguration. It's only maintained for backwards
    compatibility.
    """
