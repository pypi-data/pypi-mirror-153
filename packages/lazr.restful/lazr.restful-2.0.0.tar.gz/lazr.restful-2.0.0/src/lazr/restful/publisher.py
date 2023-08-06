# Copyright 2009 Canonical Ltd.  All rights reserved.

"""Publisher mixins for the webservice.

This module defines classes that are usually needed for integration
with the Zope publisher.
"""

__all__ = [
    "browser_request_to_web_service_request",
    "WebServicePublicationMixin",
    "WebServiceRequestTraversal",
]

from urllib.parse import (
    quote,
    urlsplit,
    urlunsplit,
)

import simplejson
from zope.component import (
    adapter,
    getMultiAdapter,
    getUtility,
    queryAdapter,
    queryMultiAdapter,
)
from zope.interface import (
    alsoProvides,
    implementer,
)
from zope.interface.interfaces import ComponentLookupError
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IBytes
from zope.security.checker import ProxyFactory

from lazr.restful import (
    CollectionResource,
    EntryField,
    EntryFieldResource,
    EntryResource,
    ScopedCollection,
)
from lazr.restful.interfaces import (
    IByteStorage,
    ICollection,
    ICollectionField,
    IEntry,
    IEntryField,
    IHTTPResource,
    INotificationsProvider,
    IReference,
    IServiceRootResource,
    IWebBrowserInitiatedRequest,
    IWebServiceClientRequest,
    IWebServiceConfiguration,
)
from lazr.restful.utils import tag_request_with_version_name


class WebServicePublicationMixin:
    """A mixin for webservice publication.

    This should usually be mixed-in with ZopePublication, or Browser,
    or HTTPPublication.
    """

    def traverseName(self, request, ob, name):
        """See `zope.publisher.interfaces.IPublication`.

        In addition to the default traversal implementation, this publication
        also handles traversal to collection scoped into an entry.
        """
        # If this is the last traversal step, then look first for a scoped
        # collection. This is done because although Navigation handles
        # traversal to entries in a scoped collection, they don't usually
        # handle traversing to the scoped collection itself.
        if len(request.getTraversalStack()) == 0:
            try:
                entry = getMultiAdapter((ob, request), IEntry)
            except ComponentLookupError:
                # This doesn't look like a lazr.restful object. Let
                # the superclass handle traversal.
                pass
            else:
                if name.endswith("_link"):
                    # The user wants to access the link resource itself,
                    # rather than the object on the other side of the link.
                    if name.endswith("_collection_link"):
                        schema_name = name[:-16]
                    else:
                        schema_name = name[:-5]
                    field = entry.schema.get(schema_name)
                    return EntryField(entry, field, name)
                field = entry.schema.get(name)
                if ICollectionField.providedBy(field):
                    result = self._traverseToScopedCollection(
                        request, entry, field, name
                    )
                    if result is not None:
                        return result
                elif IBytes.providedBy(field):
                    return self._traverseToByteStorage(
                        request, entry, field, name
                    )
                elif IReference.providedBy(field):
                    sub_entry = getattr(entry, name, None)
                    if sub_entry is None:
                        raise NotFound(ob, name, request)
                    else:
                        return sub_entry
                elif field is not None:
                    return EntryField(entry, field, name)
                else:
                    # Falls through to our parent version.
                    pass
        return super().traverseName(request, ob, name)

    def _traverseToByteStorage(self, request, entry, field, name):
        """Try to traverse to a byte storage resource in entry."""
        # Even if the library file is None, we want to allow
        # traversal, because the request might be a PUT request
        # creating a file here.
        return getMultiAdapter((entry, field.bind(entry)), IByteStorage)

    def _traverseToScopedCollection(self, request, entry, field, name):
        """Try to traverse to a collection in entry.

        This is done because we don't usually traverse to attributes
        representing a collection in our regular Navigation.

        This method returns None if a scoped collection cannot be found.
        """
        collection = getattr(entry, name, None)
        if collection is None:
            return None
        scoped_collection = ScopedCollection(entry.context, entry, request)
        # Tell the IScopedCollection object what collection it's managing,
        # and what the collection's relationship is to the entry it's
        # scoped to.
        scoped_collection.collection = collection
        scoped_collection.relationship = field
        return scoped_collection

    def getDefaultTraversal(self, request, ob):
        """See `zope.publisher.interfaces.browser.IBrowserPublication`.

        The WebService doesn't use the getDefaultTraversal() extension
        mechanism, because it only applies to GET, HEAD, and POST methods.

        See getResource() for the alternate mechanism.
        """
        # Don't traverse to anything else.
        return ob, None

    def getResource(self, request, ob):
        """Return the resource that can publish the object ob.

        This is done at the end of traversal.  If the published object
        supports the ICollection, or IEntry interface we wrap it into the
        appropriate resource.
        """
        try:
            if (
                ICollection.providedBy(ob)
                or queryMultiAdapter((ob, request), ICollection) is not None
            ):
                # Object supports ICollection protocol.
                resource = CollectionResource(ob, request)
            elif (
                IEntry.providedBy(ob)
                or queryMultiAdapter((ob, request), IEntry) is not None
            ):
                # Object supports IEntry protocol.
                resource = EntryResource(ob, request)
            elif (
                IEntryField.providedBy(ob)
                or queryAdapter(ob, IEntryField) is not None
            ):
                # Object supports IEntryField protocol.
                resource = EntryFieldResource(ob, request)
            elif queryMultiAdapter((ob, request), IHTTPResource) is not None:
                # Object can be adapted to a resource.
                resource = queryMultiAdapter((ob, request), IHTTPResource)
            elif IHTTPResource.providedBy(ob):
                # A resource knows how to take care of itself.
                return ob
            else:
                # This object should not be published on the web service.
                raise NotFound(ob, "")
        except ComponentLookupError:
            raise NotFound(ob, "")

        # Wrap the resource in a security proxy.
        return ProxyFactory(resource)

    def _processNotifications(self, request):
        """Add any notification messages to the response headers.

        If the webservice has defined an INotificationsProvider adaptor, use
        it to include with the response the relevant notification messages
        and their severity levels.
        """
        notifications_provider = INotificationsProvider(request, None)
        notifications = []
        if (
            notifications_provider is not None
            and notifications_provider.notifications
        ):
            notifications = [
                (notification.level, notification.message)
                for notification in notifications_provider.notifications
            ]
        json_notifications = simplejson.dumps(notifications)
        request.response.setHeader("X-Lazr-Notifications", json_notifications)

    def callObject(self, request, object):
        """Help web browsers handle redirects correctly."""
        value = super().callObject(request, object)
        self._processNotifications(request)
        if request.response.getStatus() // 100 == 3:
            if IWebBrowserInitiatedRequest.providedBy(request):
                # This request was (probably) sent by a web
                # browser. Because web browsers, content negotiation,
                # and redirects are a deadly combination, we're going
                # to help the browser out a little.
                #
                # We're going to take the current request's "Accept"
                # header and put it into the URL specified in the
                # Location header. When the web browser makes its
                # request, it will munge the original 'Accept' header,
                # but because the URL it's accessing will include the
                # old header in the "ws.accept" header, we'll still be
                # able to serve the right document.
                location = request.response.getHeader("Location", None)
                if location is not None:
                    accept = request.getHeader("Accept", "application/json")
                    qs_append = "ws.accept=" + quote(accept)
                    # We don't use the URI class because it will raise
                    # an exception if the Location contains invalid
                    # characters. Invalid characters may indeed be a
                    # problem, but let the problem be handled
                    # somewhere else.
                    (scheme, netloc, path, query, fragment) = urlsplit(
                        location
                    )
                    if query == "":
                        query = qs_append
                    else:
                        query += "&" + qs_append
                    uri = urlunsplit((scheme, netloc, path, query, fragment))
                    request.response.setHeader("Location", str(uri))
        return value


@implementer(IWebServiceClientRequest)
class WebServiceRequestTraversal:
    """Mixin providing web-service resource wrapping in traversal.

    This should be mixed in the request using to the base publication used.
    """

    VERSION_ANNOTATION = "lazr.restful.version"

    def traverse(self, ob):
        """See `zope.publisher.interfaces.IPublisherRequest`.

        This is called once at the beginning of the traversal process.

        WebService requests call the `WebServicePublication.getResource()`
        on the result of the base class's traversal.
        """
        self._removeVirtualHostTraversals()

        # We don't trust the value of 'ob' passed in (it's probably
        # None) because the publication depends on which version of
        # the web service was requested.
        # _removeVirtualHostTraversals() has determined which version
        # was requested and has set the application appropriately, so
        # now we can get a good value for 'ob' and traverse it.
        ob = self.publication.getApplication(self)
        result = super().traverse(ob)
        return self.publication.getResource(self, result)

    def _removeVirtualHostTraversals(self):
        """Remove the /[path_override] and /[version] traversal names."""
        names = list()
        config = getUtility(IWebServiceConfiguration)
        if config.path_override is not None:
            api = self._popTraversal(config.path_override)
            if api is not None:
                names.append(api)
                # Requests that use the webservice path override are
                # usually made by web browsers. Mark this request as one
                # initiated by a web browser, for the sake of
                # optimizations later in the request lifecycle.
                alsoProvides(self, IWebBrowserInitiatedRequest)

        # Only accept versioned URLs. Any of the active_versions is
        # acceptable.
        version = None
        for version_string in config.active_versions:
            if version_string is not None:
                version = self._popTraversal(version_string)
                if version is not None:
                    names.append(version)
                    self.setVirtualHostRoot(names=names)
                    break
        if version is None:
            raise NotFound(self, "", self)
        tag_request_with_version_name(self, version)

        # Find the appropriate service root for this version and set
        # the publication's application appropriately.
        try:
            # First, try to find a version-specific service root.
            service_root = getUtility(IServiceRootResource, name=self.version)
        except ComponentLookupError:
            # Next, try a version-independent service root.
            service_root = getUtility(IServiceRootResource)
        self.publication.application = service_root

    def _popTraversal(self, name=None):
        """Remove a name from the traversal stack, if it is present.

        :name: The string to look for in the stack, or None to accept
        any string.

        :return: The name of the element removed, or None if the stack
            wasn't changed.
        """
        stack = self.getTraversalStack()
        if len(stack) > 0 and (name is None or stack[-1] == name):
            item = stack.pop()
            self.setTraversalStack(stack)
            return item
        return None


@implementer(IWebServiceClientRequest)
@adapter(IBrowserRequest)
def browser_request_to_web_service_request(
    website_request, web_service_version=None
):
    """An adapter from a browser request to a web service request.

    Used to instantiate Resource objects when handling normal web
    browser requests.
    """
    config = getUtility(IWebServiceConfiguration)
    if web_service_version is None:
        web_service_version = config.active_versions[-1]

    body = website_request.bodyStream.getCacheStream()
    environ = dict(website_request.environment)
    # Zope picks up on SERVER_URL when setting the _app_server attribute
    # of the new request.
    environ["SERVER_URL"] = website_request.getApplicationURL()
    web_service_request = config.createRequest(body, environ)
    web_service_request.setVirtualHostRoot(
        names=[config.path_override, web_service_version]
    )
    tag_request_with_version_name(web_service_request, web_service_version)
    web_service_request._vh_root = website_request.getVirtualHostRoot()
    return web_service_request
