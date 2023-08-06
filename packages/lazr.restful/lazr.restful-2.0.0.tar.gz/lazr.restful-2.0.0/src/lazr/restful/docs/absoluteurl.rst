URL generation
**************

lazr.restful includes some classes that make it easy to generate URLs
for your objects.

RootResourceAbsoluteURL
=======================

It's easy to have an object implement ILocation and define its
URL recursively, in terms of its parent's URL. But the recursion has
to bottom out somewhere, so you need at least one real implementation
of IAbsoluteURL. lazr.simple.RootResourceAbsoluteURL is designed to
build a URL for your service root resource out of information you put
into your IWebServiceConfiguration implementation.

First, RootResourceAbsoluteURL needs to be registered.

    >>> from zope.component import getSiteManager
    >>> from lazr.restful.simple import RootResourceAbsoluteURL
    >>> sm = getSiteManager()
    >>> sm.registerAdapter(RootResourceAbsoluteURL)

Next, you need a configuration object.

    >>> from zope.interface import implementer
    >>> from lazr.restful.interfaces import IWebServiceConfiguration
    >>> @implementer(IWebServiceConfiguration)
    ... class SimpleWebServiceConfiguration:
    ...     hostname = "hostname"
    ...     service_root_uri_prefix = "root_uri_prefix/"
    ...     active_versions = ['active_version', 'latest_version']
    ...     last_version_with_mutator_named_operations = None
    ...     port = 1000
    ...     use_https = True

As always, the configuration object needs to be registered as the
utility for IWebServiceConfiguration.

    >>> configuration = SimpleWebServiceConfiguration()
    >>> sm.registerUtility(configuration)

Now we can get a RootResourceAbsoluteURL object, given a root resource
and a request.

    >>> from zope.component import getMultiAdapter
    >>> from lazr.restful.simple import RootResource, Request
    >>> from zope.traversing.browser.interfaces import IAbsoluteURL

    >>> resource = RootResource()
    >>> request = Request("", {})
    >>> request.annotations[request.VERSION_ANNOTATION] = (
    ...     'active_version')
    >>> adapter = getMultiAdapter((resource, request), IAbsoluteURL)

Calling the RootResourceAbsoluteURL will give the service root's
absolute URL.

    >>> print(adapter())
    https://hostname:1000/root_uri_prefix/active_version/

Converting the adapter to a string will give the same result, but
without the trailing slash.

    >>> print(str(adapter))
    https://hostname:1000/root_uri_prefix/active_version

(This is useful for the recursive case. When finding the URL to a
subordinate resource, Zope's AbsoluteURL implementation calls str() on
this object and joins that string to the subordinate object's name
with a slash. Putting a slash here would result in subordinate objects
having two consecutive slashes in their URLs.)

Changing the web service configuration changes the generated URLs.

    >>> configuration.use_https = False
    >>> print(getMultiAdapter((resource, request), IAbsoluteURL)())
    http://hostname:1000/root_uri_prefix/active_version/

    >>> configuration.port = None
    >>> print(getMultiAdapter((resource, request), IAbsoluteURL)())
    http://hostname/root_uri_prefix/active_version/

The URL generated includes a version identifier taken from the
value of the 'lazr.restful.version' annotation.

    >>> request.annotations[request.VERSION_ANNOTATION] = (
    ...     'latest_version')
    >>> adapter = getMultiAdapter((resource, request), IAbsoluteURL)
    >>> print(adapter())
    http://hostname/root_uri_prefix/latest_version/

For purposes of URL generation, the annotation doesn't have to be a
real version defined by the web service. Any string will do.

    >>> request.annotations[request.VERSION_ANNOTATION] = (
    ...     'no_such_version')
    >>> adapter = getMultiAdapter((resource, request), IAbsoluteURL)
    >>> print(adapter())
    http://hostname/root_uri_prefix/no_such_version/

(However, the lazr.restful traversal code will reject an invalid
version, and so in a real application lazr.restful.version will not be
set. See examples/base/tests/service.txt for that test.)

Cleanup.

    >>> request.annotations[request.VERSION_ANNOTATION] = (
    ...     'active_version')


MultiplePathPartAbsoluteURL
===========================

Zope has an AbsoluteURL class that makes it easy to turn an object
tree into a set of treelike URL paths:

http://top-level/
http://top-level/child
http://top-level/child/grandchild

And so on. It assumes that each object provides one part of the URL's
path. But what if a single object in the tree provides multiple URL's
path parts?

http://top-level/child-part1/child-part2/grandchild

AbsoluteURL won't work, but lazr.restful's MultiplePathPartAbsoluteURL
will.

To test this, we'll start with a StubRootResource and its absolute
URL generator, StubRootResourceURL.

    >>> from lazr.restful.testing.webservice import (
    ...     StubRootResource, StubRootResourceURL)
    >>> from zope.component import getSiteManager
    >>> sm = getSiteManager()
    >>> sm.registerAdapter(StubRootResourceURL)

We'll load the basic lazr.restful site configuration.

    >>> from zope.configuration import xmlconfig
    >>> def load_config():
    ...     xmlconfig.string("""
    ... <configure xmlns="http://namespaces.zope.org/zope">
    ...   <include package="lazr.restful" file="basic-site.zcml" />
    ...   <adapter
    ...    for="zope.location.interfaces.ILocation
    ...         lazr.restful.publisher.WebServiceRequestTraversal"
    ...    provides="zope.traversing.browser.interfaces.IAbsoluteURL"
    ...    factory="zope.traversing.browser.absoluteurl.AbsoluteURL"
    ...    />
    ... </configure>
    ... """)
    >>> load_config()

Here's a child of StubRootResource that implements
IMultiplePathPartLocation.

    >>> from zope.interface import implementer
    >>> from lazr.restful.simple import IMultiplePathPartLocation
    >>> @implementer(IMultiplePathPartLocation)
    ... class ChildResource:
    ...     __parent__ = StubRootResource()
    ...     __path_parts__ = ["child-part1", "child-part2"]

The ChildResource's URL includes one URL part from the root resource,
followed by two from the ChildResource itself.

    >>> resource = ChildResource()
    >>> print(str(getMultiAdapter((resource, request), IAbsoluteURL)))
    http://exampleurl/child-part1/child-part2

Now let's put an object underneath the child resource that implements
ILocation, as most resources will.

    >>> from zope.location.interfaces import ILocation
    >>> @implementer(ILocation)
    ... class GrandchildResource:
    ...     __parent__ = ChildResource()
    ...     __name__ = "grandchild"

The GrandchildResource's URL contains the URL part from the root
resource, the two from the ChildResource, and one from the
GrandchildResource itself.

    >>> print(str(getMultiAdapter(
    ...     (GrandchildResource(), request), IAbsoluteURL)))
    http://exampleurl/child-part1/child-part2/grandchild

Edge cases and error handling
=============================

MultiplePathPartAbsoluteURL escapes the same characters as AbsoluteURL.
It even escapes slashes, if a slash shows up inside a path part.

    >>> resource.__path_parts__ = ["!foo!", "bar/baz"]
    >>> print(str(getMultiAdapter((resource, request), IAbsoluteURL)))
    http://exampleurl/%21foo%21/bar%2Fbaz

If the __path_parts__ is not iterable, an attempt to get the URL
raises an exception:

    >>> resource.__path_parts__ = "foobar"
    >>> str(getMultiAdapter((resource, request), IAbsoluteURL))
    Traceback (most recent call last):
    ...
    TypeError: Expected an iterable of strings for __path_parts__.

    >>> resource.__path_parts__ = 0
    >>> str(getMultiAdapter((resource, request), IAbsoluteURL))
    Traceback (most recent call last):
    ...
    TypeError: Expected an iterable of strings for __path_parts__.

If the __parent__ or __path_parts__ is missing or None, an attempt to
get the URL raises the same exception as AbsoluteURL does.

    >>> resource.__path_parts__ = None
    >>> str(getMultiAdapter((resource, request), IAbsoluteURL))
    Traceback (most recent call last):
    ...
    TypeError: There isn't enough context to get URL information...

    >>> resource.__path_parts__ = ["foo", "bar"]
    >>> resource.__parent__ = None
    >>> str(getMultiAdapter((resource, request), IAbsoluteURL))
    Traceback (most recent call last):
    ...
    TypeError: There isn't enough context to get URL information...
