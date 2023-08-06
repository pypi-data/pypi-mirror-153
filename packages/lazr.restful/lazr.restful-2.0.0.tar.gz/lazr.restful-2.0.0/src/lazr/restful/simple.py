"""Simple implementations of various Zope and lazr.restful interfaces."""

__all__ = [
    "BaseRepresentationCache",
    "BaseWebServiceConfiguration",
    "DictionaryBasedRepresentationCache",
    "IMultiplePathPartLocation",
    "MultiplePathPartAbsoluteURL",
    "Publication",
    "PublicationMixin",
    "Request",
    "RootResource",
    "RootResourceAbsoluteURL",
    "SimulatedWebsiteRequest",
    "TraverseWithGet",
]

import traceback
from urllib.parse import (
    quote,
    unquote,
)

from zope.component import (
    adapter,
    getMultiAdapter,
    getUtility,
    queryMultiAdapter,
)
from zope.interface import Attribute, Interface, implementer
from zope.publisher.browser import BrowserRequest
from zope.publisher.interfaces import IPublication, IPublishTraverse, NotFound
from zope.publisher.publish import mapply
from zope.security.management import endInteraction, newInteraction
from zope.traversing.browser import absoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.browser.absoluteurl import _insufficientContext, _safe

import grokcore.component

from lazr.restful import EntryAdapterUtility, HTTPResource, ServiceRootResource
from lazr.restful.interfaces import (
    IRepresentationCache,
    IServiceRootResource,
    ITopLevelEntryLink,
    ITraverseWithGet,
    IWebBrowserOriginatingRequest,
    IWebServiceConfiguration,
    IWebServiceLayer,
)
from lazr.restful.publisher import (
    WebServicePublicationMixin,
    WebServiceRequestTraversal,
)
from lazr.restful.utils import (
    implement_from_dict,
    tag_request_with_version_name,
)


@implementer(IPublication)
class PublicationMixin:
    """A very simple implementation of `IPublication`.

    The object passed to the constructor is returned by getApplication().
    """

    def __init__(self, application):
        """Create the test publication.

        The object at which traversal should start is passed as parameter.
        """
        self.application = application

    def beforeTraversal(self, request):
        """Sets the request as the current interaction.

        (It also ends any previous interaction, that's convenient when
        tests don't go through the whole request.)
        """
        endInteraction()
        newInteraction(request)

    def getApplication(self, request):
        """Returns the application passed to the constructor."""
        return self.application

    def callTraversalHooks(self, request, ob):
        """Does nothing."""

    def traverseName(self, request, ob, name):
        """Traverse by looking for an `IPublishTraverse` adapter."""
        # XXX flacoste 2009/03/06 bug=338831. This is copied from
        # zope.app.publication.publicationtraverse.PublicationTraverse.
        # This should really live in zope.publisher, we are copying because
        # we don't want to depend on zope.app stuff.
        # Namespace support was dropped.
        if name == ".":
            return ob

        if IPublishTraverse.providedBy(ob):
            ob2 = ob.publishTraverse(request, name)
        else:
            # self is marker.
            adapter = queryMultiAdapter(
                (ob, request), IPublishTraverse, default=self
            )
            if adapter is not self:
                ob2 = adapter.publishTraverse(request, name)
            else:
                raise NotFound(ob, name, request)

        return self.wrapTraversedObject(ob2)

    def wrapTraversedObject(self, ob):
        """Wrap the traversed object, for instance in a security proxy.

        By default, does nothing."""
        return ob

    def afterTraversal(self, request, ob):
        """Does nothing."""

    def callObject(self, request, ob):
        """Call the object, returning the result."""
        return mapply(ob, request.getPositionalArguments(), request)

    def afterCall(self, request, ob):
        """Does nothing."""

    def handleException(self, object, request, exc_info, retry_allowed=1):
        """Prints the exception."""
        # Reproduce the behavior of ZopePublication by looking up a view
        # for this exception.
        exception = exc_info[1]
        view = queryMultiAdapter((exception, request), name="index.html")
        if view is not None:
            request.response.reset()
            request.response.setResult(view())
        else:
            traceback.print_exception(*exc_info)

    def endRequest(self, request, ob):
        """Ends the interaction."""
        endInteraction()


class Publication(WebServicePublicationMixin, PublicationMixin):
    """A simple publication.

    Combines the IPublication implementation of PublicationMixin
    with the web service implementation of WebServicePublicationMixin,
    """

    pass


@implementer(ITraverseWithGet)
class TraverseWithGet:
    """An implementation of `IPublishTraverse` that uses the get() method.

    This is a simple traversal technique that works with any object
    that defines a lookup method called get().

    This class should not be confused with
    WebServiceRequestTraversal. This class (or any other class that
    implements IPublishTraverse) controls traversal in the web
    application towards an object that implements IEntry. Once an
    IEntry has been found, further traversal (eg. to scoped
    collections or fields) always happens with
    WebServiceRequestTraversal.
    """

    def publishTraverse(self, request, name):
        """See `IPublishTraverse`."""
        name = unquote(name)
        value = self.get(request, name)
        if value is None:
            raise NotFound(self, name)
        return value

    def get(self, request, name):
        """See `ITraverseWithGet`."""
        raise NotImplementedError


@implementer(IWebServiceLayer)
class Request(WebServiceRequestTraversal, BrowserRequest):
    """A web service request with no special features."""


@implementer(IWebBrowserOriginatingRequest)
class SimulatedWebsiteRequest(BrowserRequest):
    """A (simulated) request to a website as opposed to a web service.

    If you can adapt a web service request to this class (or some
    other class that implements IWebBrowserOriginatingRequest), you
    can take advantage of the web_url feature.
    """


class RootResource(ServiceRootResource, TraverseWithGet):
    """A service root that expects top-level objects to be defined in code.

    ServiceRootResource expects top-level objects to be registered as
    Zope interfaces.
    """

    grokcore.component.provides(IServiceRootResource)

    @property
    def top_level_names(self):
        return list(self.top_level_objects.keys())

    def get(self, request, name):
        """Traverse to a top-level object."""
        return self.top_level_objects.get(name)

    def getTopLevelPublications(self):
        """Return a mapping of top-level link names to published objects."""
        top_level_resources = {}
        # First collect the top-level collections.
        for name, (
            schema_interface,
            obj,
        ) in self.top_level_collections.items():
            adapter = EntryAdapterUtility.forSchemaInterface(
                schema_interface, self.request
            )
            link_name = "%s_collection_link" % adapter.plural_type
            top_level_resources[link_name] = obj
        # Then collect the top-level entries.
        for name, entry_link in self.top_level_entry_links.items():
            link_name = "%s_link" % ITopLevelEntryLink(entry_link).link_name
            top_level_resources[link_name] = entry_link
        return top_level_resources

    @property
    def top_level_objects(self):
        """Return this web service's top-level objects."""
        objects = {}
        for name, (
            schema_interface,
            obj,
        ) in self.top_level_collections.items():
            objects[name] = obj
        objects.update(self.top_level_entry_links)
        return objects

    @property
    def top_level_collections(self):
        """Return this web service's top-level collections.

        :return: A hash mapping a name to a 2-tuple (interface, collection).
        The interface is the kind of thing contained in the collection.
        """
        if not hasattr(self, "_top_level_collections"):
            (
                self._top_level_collections,
                self._top_level_entry_links,
            ) = self._build_top_level_objects()
        return self._top_level_collections

    @property
    def top_level_entry_links(self):
        """Return this web service's top-level entry links."""
        if not hasattr(self, "_top_level_entry_links"):
            (
                self._top_level_collections,
                self._top_level_entry_links,
            ) = self._build_top_level_objects()
        return self._top_level_entry_links

    def _build_top_level_objects(self):
        """Create the list of top-level objects.

        :return: A 2-tuple of hashes (collections, entry_links). The
        'collections' hash maps a name to a 2-tuple (interface, object).
        The interface is the kind of thing contained in the collection.
        For instance, 'users': (IUser, UserSet())

        The 'entry_links' hash maps a name to an object.
        """
        return ({}, {})


@implementer(IAbsoluteURL)
@adapter(ServiceRootResource, WebServiceRequestTraversal)
class RootResourceAbsoluteURL:
    """A basic implementation of `IAbsoluteURL` for a root resource."""

    def __init__(self, context, request):
        """Initialize with respect to a context and request."""
        config = getUtility(IWebServiceConfiguration)
        self.version = request.annotations[request.VERSION_ANNOTATION]
        if config.use_https:
            self.schema = "https"
        else:
            self.schema = "http"
        self.hostname = config.hostname
        self.port = config.port
        self.prefix = config.service_root_uri_prefix

    def __str__(self):
        """Return the part of the URL that contains the hostname.

        This is called when constructing the URL for some resource.
        This string should not end with a slash; Zope's AbsoluteURL
        will provide the slash when joining this string with the
        __name__ of the subordinate resource.
        """
        use_default_port = (
            self.port is None
            or self.port == 0
            or (self.schema == "https" and self.port == 443)
            or (self.schema == "http" and self.port == 80)
        )

        if use_default_port:
            return "%s://%s/%s%s" % (
                self.schema,
                self.hostname,
                self.prefix,
                self.version,
            )
        else:
            return "%s://%s:%s/%s%s" % (
                self.schema,
                self.hostname,
                self.port,
                self.prefix,
                self.version,
            )

    def __call__(self):
        """Return the URL to the service root resource.

        This value is called when finding the URL to the service root
        resource, and it needs to end with a slash so that clients
        will be able to do relative URL resolution correctly with
        respect to the service root.
        """
        return str(self) + "/"


class IMultiplePathPartLocation(Interface):

    """An ILocation-like interface for objects with multiple path parts.

    Zope's AbsoluteURL class assumes that each object in an object
    tree contributes one path part to the URL. If an object's __name__
    is 'foo' then its URL will be its __parent__'s url plus "/foo".

    But some objects have multiple path parts. Setting an object's
    __name__ to 'foo/bar' will result in a URL path like"/foo%2Fbar"
    -- not what you want. So, implement this interface instead of
    ILocation.
    """

    __parent__ = Attribute("This object's parent.")
    __path_parts__ = Attribute(
        'The path parts of this object\'s URL. For instance, ["foo", "bar"]'
        'corresponds to the URL path "foo/bar"'
    )


@implementer(IAbsoluteURL)
@adapter(IMultiplePathPartLocation, WebServiceRequestTraversal)
class MultiplePathPartAbsoluteURL:
    """Generate a URL for an IMultiplePathPartLocation.

    Unlike Zope's AbsoluteURL, this class understands when an object
    contributes multiple path parts to the URL.

    If you use basic-site.zcml, this class is automatically registered
    as the IAbsoluteURL adapter for IMultiplePathPartLocation objects
    and web service requests.
    """

    def __init__(self, context, request):
        """Initialize with respect to a context and request."""
        self.context = context
        self.request = request

    def __str__(self):
        parent = getattr(self.context, "__parent__", None)
        if parent is None:
            raise TypeError(_insufficientContext)
        start_url = str(getMultiAdapter((parent, self.request), IAbsoluteURL))

        parts = getattr(self.context, "__path_parts__", None)
        if parts is None:
            raise TypeError(_insufficientContext)
        if isinstance(parts, str) or not hasattr(parts, "__iter__"):
            raise TypeError(
                "Expected an iterable of strings for __path_parts__."
            )

        escaped_parts = [quote(part.encode(), _safe) for part in parts]
        return start_url + "/" + "/".join(escaped_parts)

    __call__ = __str__


@implementer(IRepresentationCache)
class BaseRepresentationCache:
    """A useful base class for representation caches.

    When an object is invalidated, all of its representations must be
    removed from the cache. This means representations of every media
    type for every version of the web service. Subclass this class and
    you won't have to worry about removing everything. You can focus
    on implementing key_for() and delete_by_key(), which takes the
    return value of key_for() instead of a raw object.

    You can also implement set_by_key() and get_by_key(), which also
    take the return value of key_for(), instead of set() and get().
    """

    DO_NOT_CACHE = object()

    def get(self, obj, media_type, version, default=None):
        """See `IRepresentationCache`."""
        key = self.key_for(obj, media_type, version)
        if key is self.DO_NOT_CACHE:
            return default
        return self.get_by_key(key, default)

    def set(self, obj, media_type, version, representation):
        """See `IRepresentationCache`."""
        key = self.key_for(obj, media_type, version)
        if key is self.DO_NOT_CACHE:
            return
        return self.set_by_key(key, representation)

    def delete(self, object):
        """See `IRepresentationCache`."""
        config = getUtility(IWebServiceConfiguration)
        for version in config.active_versions:
            key = self.key_for(object, HTTPResource.JSON_TYPE, version)
            if key is not self.DO_NOT_CACHE:
                self.delete_by_key(key)

    def key_for(self, object, media_type, version):
        """Generate a unique key for an object/media type/version.

        :param object: An IEntry--the object whose representation you want.
        :param media_type: The media type of the representation to get.
        :param version: The version of the web service for which to
            fetch a representation.
        """
        raise NotImplementedError()

    def get_by_key(self, key, default=None):
        """Delete a representation from the cache, given a key.

        :key: The cache key.
        """
        raise NotImplementedError()

    def set_by_key(self, key):
        """Delete a representation from the cache, given a key.

        :key: The cache key.
        """
        raise NotImplementedError()

    def delete_by_key(self, key):
        """Delete a representation from the cache, given a key.

        :key: The cache key.
        """
        raise NotImplementedError()


class DictionaryBasedRepresentationCache(BaseRepresentationCache):
    """A representation cache that uses an in-memory dict.

    This cache transforms IRepresentationCache operations into
    operations on a dictionary.

    Don't use a Python dict object in a production installation! It
    can easily grow to take up all available memory. If you implement
    a dict-like object that maintains a maximum size with an LRU
    algorithm or something similar, you can use that. But this class
    was written for testing.
    """

    def __init__(self, use_dict):
        """Constructor.

        :param use_dict: A dictionary to keep representations in. As
        noted in the class docstring, in a production installation
        it's a very bad idea to use a standard Python dict object.
        """
        self.dict = use_dict

    def key_for(self, obj, media_type, version):
        """See `BaseRepresentationCache`."""
        # Create a fake web service request for the appropriate version.
        config = getUtility(IWebServiceConfiguration)
        web_service_request = config.createRequest("", {})
        web_service_request.setVirtualHostRoot(
            names=[config.path_override, version]
        )
        tag_request_with_version_name(web_service_request, version)

        # Use that request to create a versioned URL for the object.
        value = absoluteURL(obj, web_service_request) + "," + media_type
        return value

    def get_by_key(self, key, default=None):
        """See `IRepresentationCache`."""
        return self.dict.get(key, default)

    def set_by_key(self, key, representation):
        """See `IRepresentationCache`."""
        self.dict[key] = representation

    def delete_by_key(self, key):
        """Implementation of a `BaseRepresentationCache` method."""
        self.dict.pop(key, None)


BaseWebServiceConfiguration = implement_from_dict(
    "BaseWebServiceConfiguration",
    IWebServiceConfiguration,
    {"first_version_with_total_size_link": None},
    object,
)
