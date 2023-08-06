Adapting a browser request into a web service request
*****************************************************

Most of the time, web service requests come through the web service
layer. But there are times when a request that came through the
website neeeds to be treated as a web service request. It's easy to
adapt an IBrowserRequest into an IIWebServiceClientRequest request.

This adapters uses the request factory from the IWebServiceConfiguration
utility.

    >>> from lazr.restful.interfaces import (
    ...     IWebServiceConfiguration, IWebServiceClientRequest)
    >>> from lazr.restful.publisher import (
    ...     browser_request_to_web_service_request)
    >>> from lazr.restful.testing.webservice import WebServiceTestPublication
    >>> from lazr.restful.simple import Request
    >>> from zope.interface import implementer
    >>> from zope.component import getSiteManager
    >>> from zope.publisher.browser import TestRequest

    >>> @implementer(IWebServiceConfiguration)
    ... class SimpleWebServiceConfiguration:
    ...     path_override = 'api'
    ...     active_versions = ['beta']
    ...
    ...     def createRequest(self, body_stream, environ):
    ...         request = Request(body_stream, environ)
    ...         request.setPublication(WebServiceTestPublication(None))
    ...         return request

    >>> from lazr.restful.interfaces import IWebServiceVersion
    >>> class IBetaVersion(IWebServiceVersion):
    ...     """Marker interface for web service version."""

    >>> sm = getSiteManager()
    >>> sm.registerUtility(SimpleWebServiceConfiguration())
    >>> sm.registerUtility(IBetaVersion, IWebServiceVersion, name="beta")
    >>> sm.registerAdapter(browser_request_to_web_service_request)

    >>> website_request = TestRequest(SERVER_URL="http://cookbooks.dev/")
    >>> request = IWebServiceClientRequest(website_request)
    >>> request
    <...Request...>
    >>> request.getApplicationURL()
    'http://cookbooks.dev/api/beta'

==============
The JSON Cache
==============

Objects can be stored in a cache so that they can be included in
Javascript code inside the template. This is provided by the
IJSONRequestCache. There is a default adapter available that works with
any IApplicationRequest.

An object can be stored in the cache's 'objects' dict or its 'links' dict.

    >>> from lazr.restful.interfaces import IJSONRequestCache
    >>> from lazr.restful.jsoncache import JSONRequestCache
    >>> sm.registerAdapter(JSONRequestCache)
    >>> cache = IJSONRequestCache(website_request)

The 'objects' dict is for objects that should have their full JSON
representations put into the template.

    >>> cache.objects['object1'] = 'foo'
    >>> cache.objects['object2'] = 'bar'
    >>> for key in sorted(cache.objects):
    ...     print("%s: %s" % (key, cache.objects[key]))
    object1: foo
    object2: bar

The 'links' dict is for objects that should have their self_links put
into the template, not their whole representations.

    >>> cache.links['objectA'] = 'foo'
    >>> cache.links['objectB'] = 'bar'
    >>> for key in sorted(cache.links):
    ...     print("%s: %s" % (key, cache.links[key]))
    objectA: foo
    objectB: bar

There is a TALES formatter available that can be used to obtain a
reference to this cache from TALES:

    >>> from lazr.restful.tales import WebServiceRequestAPI
    >>> from lazr.restful.testing.tales import test_tales
    >>> from zope.interface import Interface
    >>> from zope.traversing.adapters import DefaultTraversable

    >>> sm.registerAdapter(DefaultTraversable, [Interface])
    >>> sm.registerAdapter(WebServiceRequestAPI, name="webservicerequest")

    >>> cache = test_tales(
    ...     "request/webservicerequest:cache", request=website_request)
    >>> for key in sorted(cache.links):
    ...     print("%s: %s" % (key, cache.links[key]))
    objectA: foo
    objectB: bar
