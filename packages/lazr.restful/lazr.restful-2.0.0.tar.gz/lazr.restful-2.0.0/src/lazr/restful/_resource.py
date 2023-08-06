# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Base classes for HTTP resources."""

__all__ = [
    "BatchingResourceMixin",
    "Collection",
    "CollectionResource",
    "Entry",
    "EntryAdapterUtility",
    "EntryField",
    "EntryFieldResource",
    "EntryHTMLView",
    "EntryResource",
    "HTTPResource",
    "JSONDate",
    "JSONItem",
    "ReadOnlyResource",
    "RedirectResource",
    "register_versioned_request_utility",
    "render_field_to_html",
    "ResourceJSONEncoder",
    "RESTUtilityBase",
    "ScopedCollection",
    "ServiceRootResource",
    "WADL_SCHEMA_FILE",
]

from collections import OrderedDict
from email.utils import formatdate
import copy
import hashlib
import html
from operator import itemgetter
import os
import simplejson
import simplejson.encoder
import sys
import time

from zope.component import (
    adapter,
    getAdapters,
    getAllUtilitiesRegisteredFor,
    getGlobalSiteManager,
    getMultiAdapter,
    getSiteManager,
    getUtility,
    queryMultiAdapter,
)
from zope.event import notify
from zope.interface import (
    alsoProvides,
    implementer,
    implementedBy,
    providedBy,
    Interface,
)
from zope.interface.common.idatetime import IDate
from zope.interface.common.sequence import IFiniteSequence
from zope.interface.interfaces import (
    ComponentLookupError,
    IInterface,
)
from zope.location.interfaces import ILocation
from zope.pagetemplate.engine import TrustedAppPT
from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.proxy import isProxy
from zope.publisher.http import init_status_codes, status_reasons
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema import ValidationError, getFieldsInOrder
from zope.schema.interfaces import (
    ConstraintNotSatisfied,
    IBytes,
    IField,
    RequiredMissing,
)
from zope.security.interfaces import Unauthorized
from zope.security.proxy import getChecker, removeSecurityProxy
from zope.security.management import checkPermission
from zope.traversing.browser import absoluteURL, AbsoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL

from lazr.batchnavigator import BatchNavigator
from lazr.delegates import Passthrough
from lazr.enum import BaseItem
from lazr.lifecycle.event import ObjectModifiedEvent
from lazr.lifecycle.snapshot import Snapshot
from lazr.restful.interfaces import (
    ICollection,
    ICollectionField,
    ICollectionResource,
    IEntry,
    IEntryField,
    IEntryFieldResource,
    IEntryResource,
    IFieldHTMLRenderer,
    IFieldMarshaller,
    IHTTPResource,
    IJSONPublishable,
    IReference,
    IRepresentationCache,
    IResourceDELETEOperation,
    IResourceGETOperation,
    IResourcePOSTOperation,
    IScopedCollection,
    IServiceRootResource,
    ITopLevelEntryLink,
    IUnmarshallingDoesntNeedValue,
    IWebBrowserOriginatingRequest,
    IWebServiceClientRequest,
    IWebServiceConfiguration,
    IWebServiceExceptionView,
    IWebServiceLayer,
    IWebServiceVersion,
    LAZR_WEBSERVICE_NAME,
)
from lazr.restful.marshallers import URLDereferencingMixin
from lazr.restful.utils import (
    extract_write_portion,
    get_current_web_service_request,
    parse_accept_style_header,
    sorted_named_things,
)


# The path to the WADL XML Schema definition.
WADL_SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "wadl20061109.xsd")

# Constants and levels of detail to use when unmarshalling the data.
MISSING = object()
NORMAL_DETAIL = object()
CLOSEUP_DETAIL = object()

# XXX leonardr 2009-01-29
# bug=https://bugs.edge.launchpad.net/zope3/+bug/322486:
# Add nonstandard status methods to Zope's status_reasons dictionary.
for code, reason in [(209, "Content Returned")]:
    if code not in status_reasons:
        status_reasons[code] = reason
init_status_codes()


def decode_value(value):
    """Return a unicode value curresponding to `value`."""
    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        return value.decode("utf-8")
    else:
        return simplejson.dumps(value, cls=ResourceJSONEncoder)


def _default_html_renderer(value):
    """The default technique for rendering a value as an HTML snippet."""
    return html.escape(str(value), quote=False)


@adapter(Interface, IField, IWebServiceClientRequest)
@implementer(IFieldHTMLRenderer)
def render_field_to_html(object, field, request):
    """Turn a field's current value into an XHTML snippet.

    This is the default adapter for IFieldHTMLRenderer.
    """
    return _default_html_renderer


def register_versioned_request_utility(interface, version):
    """Registers a marker interface as a utility for version lookup.

    This function registers the given interface class as the
    IWebServiceVersion utility for the given version string.
    """
    alsoProvides(interface, IWebServiceVersion)
    getSiteManager().registerUtility(
        interface, IWebServiceVersion, name=version
    )


class LazrPageTemplateFile(TrustedAppPT, PageTemplateFile):
    "A page template class for generating web service-related documents."
    pass


class ResourceJSONEncoder(simplejson.encoder.JSONEncoderForHTML):
    """A JSON encoder for JSON-exposable resources like entry resources.

    This class works with simplejson to encode objects as JSON if they
    implement IJSONPublishable. All EntryResource subclasses, for
    instance, should implement IJSONPublishable.
    """

    def __init__(self, *args, **kwargs):
        self.media_type = kwargs.pop("media_type", HTTPResource.JSON_TYPE)
        super().__init__(*args, **kwargs)

    def default(self, obj):
        """Convert the given object to a simple data structure."""
        if isProxy(obj):
            # We have a security-proxied version of a built-in
            # type. We create a new version of the type by copying the
            # proxied version's content. That way the container is not
            # security proxied (and simplejson will know what do do
            # with it), but the content will still be security
            # wrapped.
            underlying_object = removeSecurityProxy(obj)
            if isinstance(underlying_object, list):
                return list(obj)
            if isinstance(underlying_object, tuple):
                return tuple(obj)
            if isinstance(underlying_object, dict):
                return dict(obj)
        request = get_current_web_service_request()
        if queryMultiAdapter((obj, request), IEntry):
            obj = EntryResource(obj, request)

        return IJSONPublishable(obj).toDataForJSON(self.media_type)


@implementer(IJSONPublishable)
@adapter(BaseItem)
class JSONItem:
    """JSONPublishable adapter for lazr.enum."""

    def __init__(self, context):
        self.context = context

    def toDataForJSON(self, media_type):
        """See `ISJONPublishable`"""
        return str(self.context.title)


@implementer(IJSONPublishable)
@adapter(IDate)
class JSONDate:
    """JSONPublishable adapter for date/datetime."""

    def __init__(self, context):
        self.context = context

    def toDataForJSON(self, media_type):
        """See `IJSONPublishable`."""
        return self.context.isoformat()


@implementer(IHTTPResource)
class RedirectResource(URLDereferencingMixin):
    """A resource that redirects to another URL."""

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def __call__(self):
        url = self.url
        self.request.response.setStatus(301)
        self.request.response.setHeader("Location", url)

    @property
    def context(self):
        return self.dereference_url_as_object(self.url)


@implementer(IHTTPResource)
class HTTPResource:
    """See `IHTTPResource`."""

    # Some interesting media types.
    WADL_TYPE = "application/vnd.sun.wadl+xml"
    JSON_TYPE = "application/json"
    JSON_PLUS_XHTML_TYPE = "application/json;include=lp_html"
    XHTML_TYPE = "application/xhtml+xml"

    # This misspelling of the WADL media type was used for a while,
    # and lazr.restful still supports it to avoid breaking clients
    # that depend on it.
    DEPRECATED_WADL_TYPE = "application/vd.sun.wadl+xml"

    # A preparsed template file for WADL representations of resources.
    WADL_TEMPLATE = LazrPageTemplateFile("templates/wadl-resource.pt")

    # All resources serve WADL and JSON representations. Only entry
    # resources serve XHTML representations and JSON+XHTML representations.
    SUPPORTED_CONTENT_TYPES = [WADL_TYPE, DEPRECATED_WADL_TYPE, JSON_TYPE]

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.etags_by_media_type = {}

    def __call__(self):
        """See `IHTTPResource`."""
        pass

    def getRequestMethod(self, request=None):
        """Return the HTTP method of the provided (or current) request.

        This is usually the actual HTTP method, but it might be
        overridden by a value for X-HTTP-Method-Override.

        :return: The HTTP method to use.
        """
        if request is None:
            request = self.request
        override = request.headers.get("X-HTTP-Method-Override")
        if override is not None and request.method == "POST":
            # POST is the only HTTP method for which we respect
            # X-HTTP-Method-Override.
            return override
        return request.method

    def handleConditionalGET(self):
        """Handle a possible conditional GET request.

        This method has side effects. If the resource provides a
        generated ETag, it sets this value as the "ETag" response
        header. If the "ETag" request header matches the generated
        ETag, it sets the response code to 304 ("Not Modified").

        :return: The media type to serve. If this value is None, the
            incoming ETag matched the generated ETag and there is no
            need to serve anything else.
        """
        incoming_etags = self._parseETags("If-None-Match")

        media_type = self.getPreferredSupportedContentType()
        existing_etag = self.getETag(media_type)
        if existing_etag is not None:
            self.request.response.setHeader("ETag", existing_etag)
            if existing_etag in incoming_etags:
                # The client already has this representation.
                # No need to send it again.
                self.request.response.setStatus(304)  # Not Modified
                media_type = None
        return media_type

    def handleConditionalWrite(self):
        """Handle a possible conditional PUT or PATCH request.

        This method has side effects. If the write operation should
        not continue, because the incoming ETag doesn't match the
        generated ETag, it sets the response code to 412 ("Precondition
        Failed"). Whether or not the two ETags 'match' depends on the
        resource-specific implementation, but by default two ETags
        only 'match' if they are identical.

        If the PUT or PATCH request is being tunneled through POST
        with X-HTTP-Method-Override, the media type of the incoming
        representation will be obtained from X-Content-Type-Override
        instead of Content-Type, should X-C-T-O be provided.

        :return: The media type of the incoming representation. If
            this value is None, the incoming ETag didn't match the
            generated ETag and the incoming representation should be
            ignored.
        """
        media_type = self.request.headers.get("X-Content-Type-Override")
        if media_type is not None:
            if self.request.method != "POST":
                # X-C-T-O should not be used unless the underlying
                # method is POST. Set response code 400 ("Bad
                # Request").
                self.request.response.setStatus(400)
                return None
        else:
            media_type = self.request.headers.get(
                "Content-Type", self.JSON_TYPE
            )

        incoming_etags = self._parseETags("If-Match")
        if len(incoming_etags) == 0:
            # This is not a conditional write.
            return media_type
        existing_etag = self.getETag(media_type)
        if self._etagMatchesForWrite(existing_etag, incoming_etags):
            # The conditional write can continue.
            return media_type
        # The resource has changed since the client requested it.
        # Don't let the write go through. Set response code 412
        # ("Precondition Failed")
        self.request.response.setStatus(412)
        return None

    def _etagMatchesForWrite(self, existing_etag, incoming_etags):
        """Perform an ETag match to see if conditional write is OK.

        By default, we match the full ETag strings against each other.
        """
        return existing_etag in incoming_etags

    def _getETagCores(self, cache=None):
        """Calculate the core ETag for a representation.

        :return: a list of strings that will be used to calculate the
            full ETag. If None is returned, no ETag at all will be
            calculated for the given resource and media type.
        """
        return None

    def getETag(self, media_type, cache=None):
        """Calculate the ETag for an entry.

        An ETag is derived from a 'core' string conveying information
        about the representation itself, plus information about the
        content type and the current Launchpad revision number. The
        resulting string is hashed, and there's your ETag.

        :arg unmarshalled_field_values: A dict mapping field names to
            unmarshalled values, obtained during some other operation
            such as the construction of a representation.
        """
        # Try to find a cached value.
        if media_type == self.JSON_PLUS_XHTML_TYPE:
            # The JSON+HTML representation will never change
            # unless the JSON representation also changes or the
            # software is upgraded. Use the same ETag for both.
            media_type = self.JSON_TYPE
        etag = self.etags_by_media_type.get(media_type)
        if etag is not None:
            return etag

        # We calculate the ETag core by delegating to the subclass.
        etag_cores = self._getETagCores(cache)

        if etag_cores is None:
            return None

        core_hashes = []
        for core in etag_cores:
            hash_object = hashlib.sha1()
            hash_object.update(core)
            core_hashes.append(hash_object)

        # Append the media type, so that web browsers won't treat
        # different representations of a resource interchangeably.
        core_hashes[-1].update(("\0" + media_type).encode())

        etag = '"%s"' % "-".join(core.hexdigest() for core in core_hashes)
        self.etags_by_media_type[media_type] = etag
        return etag

    def implementsPOST(self):
        """Returns True if this resource will respond to POST.

        Right now this means the resource has defined one or more
        custom POST operations.
        """
        adapters = list(
            getAdapters((self.context, self.request), IResourcePOSTOperation)
        )
        return len(adapters) > 0

    def implementsDELETE(self):
        """Returns True if this resource will respond to DELETE."""
        adapters = list(
            getAdapters((self.context, self.request), IResourceDELETEOperation)
        )
        assert len(adapters) < 2, (
            "%s has more than one registered DELETE "
            "handler." % self.context.__class__
        )
        return len(adapters) > 0

    def toWADL(self):
        """Represent this resource as a WADL application.

        The WADL document describes the capabilities of this resource.
        """
        namespace = self.WADL_TEMPLATE.pt_getContext()
        namespace["context"] = self
        return self.WADL_TEMPLATE.pt_render(namespace)

    def getPreferredSupportedContentType(self):
        """Of the content types we serve, which would the client prefer?

        The web service supports WADL, XHTML, and JSON
        representations. If no supported media type is requested, JSON
        is the default. This method determines whether the client
        would rather have WADL, XHTML, or JSON.
        """
        content_types = self.getPreferredContentTypes()
        winner = None
        for media_type in self.SUPPORTED_CONTENT_TYPES:
            try:
                pos = content_types.index(media_type)
                if winner is None or pos < winner[1]:
                    winner = (media_type, pos)
            except ValueError:
                pass
        if winner is None:
            return self.JSON_TYPE
        else:
            return winner[0]

    def getPreferredContentTypes(self):
        """Find which content types the client prefers to receive."""
        accept_header = self.request.form.pop(
            "ws.accept", None
        ) or self.request.get("HTTP_ACCEPT")
        return parse_accept_style_header(accept_header)

    def _parseETags(self, header_name):
        """Extract a list of ETags from a header and parse the list.

        RFC2616 allows multiple comma-separated ETags.

        If the compensate_for_mod_compress_etag_modification value is set,
        ETags like '"foo"-gzip' and '"foo-gzip"' will be transformed into
        '"foo"'.
        """
        header = self.request.getHeader(header_name)
        if header is None:
            return []
        utility = getUtility(IWebServiceConfiguration)
        strip_gzip_from_etag = (
            utility.compensate_for_mod_compress_etag_modification
        )
        etags = []
        # We're kind of cheating, because entity tags can technically
        # have commas in them, but none of our tags contain commas, so
        # this will work.
        for etag in header.split(","):
            etag = etag.strip()
            if strip_gzip_from_etag:
                if etag.endswith("-gzip"):
                    etag = etag[:-5]
                elif etag.endswith('-gzip"'):
                    etag = etag[:-6] + '"'
            etags.append(etag)
        return etags

    def _parseContentDispositionHeader(self, value):
        """Parse a Content-Disposition header.

        :return: a 2-tuple (disposition-type, disposition-params).
        disposition-params is a dict mapping parameter names to values.
        """
        disposition = None
        params = {}
        if value is None:
            return (disposition, params)
        pieces = value.split(";")
        if len(pieces) > 1:
            disposition = pieces[0].strip()
        for name_value in pieces[1:]:
            name_and_value = name_value.split("=", 2)
            if len(name_and_value) == 2:
                name = name_and_value[0].strip()
                value = name_and_value[1].strip()
                # Strip quotation marks if present. RFC2183 gives
                # guidelines for when to quote these values, but it's
                # very likely that a client will quote even short
                # filenames, and unlikely that a filename will
                # actually begin and end with quotes.
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
            else:
                name = name_and_value
                value = None
            params[name] = value
        return (disposition, params)


class WebServiceBatchNavigator(BatchNavigator):
    """A batch navigator that speaks to web service clients.

    This batch navigator differs from others in the names of the query
    variables it expects. This class expects the starting point to be
    contained in the query variable "ws.start" and the size of the
    batch to be contained in the query variable "ws.size". When this
    navigator serves links, it includes query variables by those
    names.
    """

    start_variable_name = "ws.start"
    batch_variable_name = "ws.size"

    @property
    def default_batch_size(self):
        return getUtility(IWebServiceConfiguration).default_batch_size

    @property
    def max_batch_size(self):
        return getUtility(IWebServiceConfiguration).max_batch_size


class BatchingResourceMixin:

    """A mixin for resources that need to batch lists of entries."""

    # TODO: determine real need for __init__ and super() call

    def total_size_link(self, navigator):
        """Return the URL to fetch to find out the collection's total size.

        If this is None, the total size will be included inline.

        :param navigator: A BatchNavigator object for the current batch.
        """
        return None

    def get_total_size(self, entries):
        """Get the number of items in entries.

        :return: a JSON string representing the number of objects in the list
        """
        if not hasattr(entries, "__len__"):
            entries = IFiniteSequence(entries)

        return simplejson.dumps(len(entries))

    def batch(self, entries, request):
        """Prepare a batch from a (possibly huge) list of entries.

        :return: a JSON string representing a hash:

        'entries' contains a list of EntryResource objects for the
          entries that actually made it into this batch
        'total_size' contains the total size of the list.
        'total_size_link' contains a link to the total size of the list.
        'next_url', if present, contains a URL to get the next batch
         in the list.
        'prev_url', if present, contains a URL to get the previous batch
         in the list.
        'start' contains the starting index of this batch

        Only one of 'total_size' or 'total_size_link' will be present.

        Note that the JSON string will be missing its final curly
        brace. This is in case the caller wants to add some additional
        keys to the JSON hash. It's the caller's responsibility to add
        a '}' to the end of the string returned from this method.
        """
        if not hasattr(entries, "__len__"):
            entries = IFiniteSequence(entries)
        navigator = WebServiceBatchNavigator(entries, request)

        view_permission = getUtility(IWebServiceConfiguration).view_permission
        batch = {"start": navigator.batch.start}
        # If this is the last batch, then total() is easy to
        # calculate. Let's use it and save the client from having to
        # ask for the total size of the collection.
        if navigator.batch.nextBatch() is None:
            total_size_link = None
        else:
            total_size_link = self.total_size_link(navigator)
        if total_size_link is None:
            total_size = navigator.batch.total()
            if total_size < 0:
                # lazr.batchnavigator uses -1 for an empty list.
                # We want to use 0.
                total_size = 0
            batch["total_size"] = total_size
        else:
            batch["total_size_link"] = total_size_link
        next_url = navigator.nextBatchURL()
        if next_url != "":
            batch["next_collection_link"] = next_url
        prev_url = navigator.prevBatchURL()
        if prev_url != "":
            batch["prev_collection_link"] = prev_url
        json_string = simplejson.dumps(batch, cls=ResourceJSONEncoder)

        # String together a bunch of entry representations, possibly
        # obtained from a representation cache.
        resources = [
            EntryResource(entry, request)
            for entry in navigator.batch
            if checkPermission(view_permission, entry)
        ]
        entry_strings = [
            resource._representation(HTTPResource.JSON_TYPE)
            for resource in resources
        ]
        json_string = (
            json_string[:-1]
            + ', "entries": ['
            + (", ".join(entry_strings) + "]")
        )
        # The caller is responsible for tacking on the final curly brace.
        return json_string


class CustomOperationResourceMixin:

    """A mixin for resources that implement a collection-entry pattern."""

    def __init__(self, context, request):
        """A basic constructor."""
        # Like all mixin classes, this class is designed to be used
        # with multiple inheritance. That requires defining __init__
        # to call the next constructor in the chain, which means using
        # super() even though this class itself has no superclass.
        super().__init__(context, request)

    def handleCustomGET(self, operation_name):
        """Execute a custom search-type operation triggered through GET.

        This is used by both EntryResource and CollectionResource.

        :param operation_name: The name of the operation to invoke.
        :return: The result of the operation: either a string or an
        object that needs to be serialized to JSON.
        """
        if not isinstance(operation_name, str):
            self.request.response.setStatus(400)
            return "Expected a single operation: %r" % (operation_name,)

        try:
            operation = getMultiAdapter(
                (self.context, self.request),
                IResourceGETOperation,
                name=operation_name,
            )
        except ComponentLookupError:
            self.request.response.setStatus(400)
            return "No such operation: " + operation_name

        show = self.request.form.get("ws.show")
        if show == "total_size":
            operation.total_size_only = True
        return operation()

    def handleCustomPOST(self, operation_name):
        """Execute a custom write-type operation triggered through POST.

        This is used by both EntryResource and CollectionResource.

        :param operation_name: The name of the operation to invoke.
        :return: The result of the operation: either a string or an
        object that needs to be serialized to JSON.
        """
        if not isinstance(operation_name, str):
            self.request.response.setStatus(400)
            return "Expected a single operation: %r" % (operation_name,)

        try:
            operation = getMultiAdapter(
                (self.context, self.request),
                IResourcePOSTOperation,
                name=operation_name,
            )
        except ComponentLookupError:
            self.request.response.setStatus(400)
            return "No such operation: " + operation_name
        return operation()

    def do_POST(self):
        """Invoke a custom operation.

        XXX leonardr 2008-04-01 bug=210265:
        The standard meaning of POST (ie. when no custom operation is
        specified) is "create a new subordinate resource."  Code
        should eventually go into CollectionResource that implements
        POST to create a new entry inside the collection.
        """
        operation_name = self.request.form.get("ws.op")
        if operation_name is None:
            self.request.response.setStatus(400)
            return "No operation name given."
        del self.request.form["ws.op"]
        return self.handleCustomPOST(operation_name)

    def do_DELETE(self):
        """Invoke a destructor operation."""
        try:
            operation = getMultiAdapter(
                (self.context, self.request), IResourceDELETEOperation
            )
        except ComponentLookupError:
            # This should never happen because implementsDELETE()
            # makes sure there is a registered
            # IResourceDELETEOperation.
            self.request.response.setStatus(405)
            return "DELETE not supported."
        return operation()


class FieldUnmarshallerMixin:

    """A class that needs to unmarshall field values."""

    # The representation value used when the client doesn't have
    # authorization to see the real value.
    REDACTED_VALUE = "tag:launchpad.net:2008:redacted"

    def __init__(self, context, request):
        """A basic constructor."""
        # Like all mixin classes, this class is designed to be used
        # with multiple inheritance. That requires defining __init__
        # to call the next constructor in the chain, which means using
        # super() even though this class itself has no superclass.
        super().__init__(context, request)
        self._unmarshalled_field_cache = {}

    def _unmarshallField(self, field_name, field, detail=NORMAL_DETAIL):
        """See what a field would look like in a generic representation.

        :return: a 2-tuple (representation_name, representation_value).
        """
        cached_value = MISSING
        if detail is NORMAL_DETAIL:
            cached_value = self._unmarshalled_field_cache.get(
                field_name, MISSING
            )
        if cached_value is not MISSING:
            return cached_value[0]

        field = field.bind(self.context)
        marshaller = getMultiAdapter((field, self.request), IFieldMarshaller)
        try:
            if IUnmarshallingDoesntNeedValue.providedBy(marshaller):
                value = None
                flag = IUnmarshallingDoesntNeedValue
            else:
                value = getattr(self.entry, field.__name__)
                flag = None
            if detail is NORMAL_DETAIL:
                repr_value = marshaller.unmarshall(self.entry, value)
            elif detail is CLOSEUP_DETAIL:
                repr_value = marshaller.unmarshall_to_closeup(
                    self.entry, value
                )
            else:
                raise AssertionError("Invalid level of detail specified")
        except Unauthorized:
            # Either the client doesn't have permission to see
            # this field, or it doesn't have permission to read
            # its current value. Rather than denying the client
            # access to the resource altogether, use our special
            # 'redacted' tag: URI for the field's value.
            repr_value = self.REDACTED_VALUE
            value = None
            flag = Unauthorized

        unmarshalled = (marshaller.representation_name, repr_value)

        if detail is NORMAL_DETAIL:
            self._unmarshalled_field_cache[field_name] = (
                unmarshalled,
                (field, value, flag),
            )
        return unmarshalled

    def _field_with_html_renderer(self, field_name, field):
        """Find an IFieldHTMLRenderer for the given field.

        :return: A 3-tuple (name, value, renderer). 'name' and 'value'
          are the unmarshalled field name and JSON-ready
          value. 'renderer' is an object capable of turning the
          JSON-ready value into an HTML value.
        """
        name, value = self._unmarshallField(field_name, field)
        try:
            # Try to get a renderer for this particular field.
            renderer = getMultiAdapter(
                (self.entry.context, field, self.request),
                IFieldHTMLRenderer,
                name=field.__name__,
            )
        except ComponentLookupError:
            # There's no field-specific renderer. Look up an
            # IFieldHTMLRenderer for this _type_ of field.
            field = field.bind(self.entry.context)
            renderer = getMultiAdapter(
                (self.entry.context, field, self.request), IFieldHTMLRenderer
            )
        return name, value, renderer

    def unmarshallFieldToHTML(self, field_name, field):
        """See what a field would look like in an HTML representation.

        This is usually similar to the value of _unmarshallField(),
        but it might contain some custom HTML weirdness.

        :return: a 2-tuple (representation_name, representation_value).
        """
        name, value, renderer = self._field_with_html_renderer(
            field_name, field
        )
        return name, renderer(value)


class ReadOnlyResource(HTTPResource):
    """A resource that serves a string in response to GET."""

    def __init__(self, context, request):
        """A basic constructor."""
        # This class is designed to be used with mixins. That means
        # defining __init__ to call the next constructor in the chain,
        # even though there's no other code in __init__.
        super().__init__(context, request)

    def __call__(self):
        """Handle a GET or (if implemented) POST request."""
        result = ""
        method = self.getRequestMethod()
        if method == "GET":
            result = self.do_GET()
        elif method == "POST" and self.implementsPOST():
            result = self.do_POST()
        else:
            allow_string = "GET"
            if self.implementsPOST():
                allow_string += " POST"
            self.request.response.setStatus(405)
            self.request.response.setHeader("Allow", allow_string)
        return result


class ReadWriteResource(HTTPResource):
    """A resource that responds to GET, PUT, and PATCH."""

    def __init__(self, context, request):
        """A basic constructor."""
        # This class is designed to be used with mixins. That means
        # defining __init__ to call the next constructor in the chain,
        # even though there's no other code in __init__.
        super().__init__(context, request)

    def __call__(self):
        """Handle a GET, PUT, or PATCH request."""
        result = b""
        method = self.getRequestMethod()
        try:
            if method == "GET":
                result = self.do_GET()
            elif method in ["PUT", "PATCH"]:
                media_type = self.handleConditionalWrite()
                if media_type is not None:
                    stream = self.request.bodyStream
                    representation = stream.getCacheStream().read()
                    if method == "PUT":
                        result = self.do_PUT(media_type, representation)
                    else:
                        result = self.do_PATCH(media_type, representation)
            elif method == "POST" and self.implementsPOST():
                result = self.do_POST()
            elif method == "DELETE" and self.implementsDELETE():
                result = self.do_DELETE()
            else:
                allow_string = "GET PUT PATCH"
                if self.implementsPOST():
                    allow_string += " POST"
                if self.implementsDELETE():
                    allow_string += " DELETE"
                self.request.response.setStatus(405)
                self.request.response.setHeader("Allow", allow_string)
        except Exception as e:
            exception_info = sys.exc_info()
            try:
                view = getMultiAdapter((e, self.request), name="index.html")
                try:
                    ws_view = IWebServiceExceptionView(view)
                except TypeError:
                    # There's a view for this exception, but it's not one we
                    # can understand.  It was probably designed for a web
                    # application rather than a web service.  We'll re-raise
                    # the exception, let the publisher look up the view, and
                    # hopefully handle it better.  Note the careful
                    # reraising that ensures the original traceback is
                    # preserved.
                    raise exception_info[1] from None
            finally:
                del exception_info

            self.request.response.setStatus(ws_view.status)
            if ws_view.status // 100 == 4:
                # This exception corresponds to a client-side error
                result = ws_view()
            else:
                # This exception corresponds to a server-side error
                # (or some weird attempt to handle redirects or normal
                # status codes using exceptions). Let the publisher
                # handle it. (No need for carefuly reraising here, since there
                # is only one exception in flight we just use a bare raise to
                # reraise the original exception.)
                raise
        return result


class EntryHTMLView:
    """An HTML view of an entry."""

    # A preparsed template file for HTML representations of the resource.
    HTML_TEMPLATE = LazrPageTemplateFile("templates/html-resource.pt")

    def __init__(self, context, request):
        """Initialize with respect to a data object and request."""
        self.context = context
        self.request = request
        self.resource = EntryResource(context, request)

    def __call__(self):
        """Send the entry data through an HTML template."""
        namespace = self.HTML_TEMPLATE.pt_getContext()
        names_and_values = self.resource.toDataStructure(
            HTTPResource.XHTML_TYPE
        ).items()
        data = [
            {"name": name, "value": decode_value(value)}
            for name, value in names_and_values
        ]
        namespace["context"] = sorted(data, key=itemgetter("name"))
        return self.HTML_TEMPLATE.pt_render(namespace)


class EntryManipulatingResource(ReadWriteResource):
    """A resource that manipulates some aspect of an entry."""

    def __init__(self, context, request):
        # This class is designed to be used with mixins. That means
        # defining __init__ to call the next constructor in the chain,
        # even though there's no other code in __init__.
        super().__init__(context, request)

    def processAsJSONDocument(self, media_type, representation):
        """Process an incoming representation as a JSON document."""
        if not media_type.startswith(self.JSON_TYPE):
            self.request.response.setStatus(415)
            return None, "Expected a media type of %s." % self.JSON_TYPE
        try:
            h = simplejson.loads(representation.decode("utf-8"))
        except ValueError:
            self.request.response.setStatus(400)
            return None, "Entity-body was not a well-formed JSON document."
        return h, None

    def applyChanges(self, changeset, media_type=None):
        """Apply a dictionary of key-value pairs as changes to an entry.

        :param changeset: A dictionary. Should come from an incoming
        representation.

        :return: If there was an error, a string error message to be
        propagated to the client.
        """
        media_type = media_type or self.JSON_TYPE
        changeset = copy.copy(changeset)
        validated_changeset = []
        errors = []

        # Some fields aren't part of the schema, so they're handled
        # separately.
        modified_read_only_attribute = (
            "%s: You tried to modify a " "read-only attribute."
        )
        if "self_link" in changeset:
            if changeset["self_link"] != absoluteURL(
                self.entry.context, self.request
            ):
                errors.append(modified_read_only_attribute % "self_link")
            del changeset["self_link"]

        if "web_link" in changeset:
            browser_request = IWebBrowserOriginatingRequest(self.request, None)
            if browser_request is not None:
                existing_web_link = absoluteURL(
                    self.entry.context, browser_request
                )
                if changeset["web_link"] != existing_web_link:
                    errors.append(modified_read_only_attribute % "web_link")
                del changeset["web_link"]

        if "resource_type_link" in changeset:
            if changeset["resource_type_link"] != self.type_url:
                errors.append(
                    modified_read_only_attribute % "resource_type_link"
                )
            del changeset["resource_type_link"]

        if "http_etag" in changeset:
            if changeset["http_etag"] != self.getETag(media_type):
                errors.append(modified_read_only_attribute % "http_etag")
            del changeset["http_etag"]

        if "lp_html" in changeset:
            if media_type == self.JSON_PLUS_XHTML_TYPE:
                # The HTML portion of the representation is read-only,
                # so ignore it.
                del changeset["lp_html"]

        # For every field in the schema, see if there's a corresponding
        # field in the changeset.
        for name, field in get_entry_fields_in_write_order(self.entry):
            field = field.bind(self.entry.context)
            marshaller = getMultiAdapter(
                (field, self.request), IFieldMarshaller
            )
            repr_name = marshaller.representation_name
            if repr_name not in changeset:
                # The client didn't try to set a value for this field.
                continue

            # Obtain the current value of the field, as it would be
            # shown in an outgoing representation. This gives us an easy
            # way to see if the client changed the value.
            try:
                current_value = marshaller.unmarshall(
                    self.entry, getattr(self.entry, name)
                )
            except Unauthorized:
                # The client doesn't have permission to see the old
                # value. That doesn't necessarily mean they can't set
                # it to a new value, but it does mean we have to
                # assume they're changing it rather than see for sure
                # by comparing the old value to the new.
                current_value = self.REDACTED_VALUE

            # The client tried to set a value for this field. Marshall
            # it, validate it, and (if it's different from the current
            # value) move it from the client changeset to the
            # validated changeset.
            original_value = changeset.pop(repr_name)
            if original_value == current_value == self.REDACTED_VALUE:
                # The client can't see the field's current value, and
                # isn't trying to change it. Skip to the next field.
                continue

            try:
                value = marshaller.marshall_from_json_data(original_value)
            except (ValueError, ValidationError) as e:
                errors.append("%s: %s" % (repr_name, e))
                continue

            if ICollectionField.providedBy(field):
                # This is a collection field, so the most we can do is set an
                # error message if the new value is not identical to the
                # current one.
                if value != current_value:
                    errors.append(
                        "%s: You tried to modify a collection "
                        "attribute." % repr_name
                    )
                continue

            if IBytes.providedBy(field):
                # We don't modify Bytes fields from the Entry that contains
                # them, but we may tell users how to do so if they attempt
                # to change them.  The encode call is because
                # BytesFieldMarshaller.unmarshall returns a link to the byte
                # storage resource as a str, but
                # BytesFieldMarshaller.marshall_from_json_data returns
                # bytes.
                if value != current_value.encode():
                    if field.readonly:
                        errors.append(modified_read_only_attribute % repr_name)
                    else:
                        errors.append(
                            "%s: To modify this field you need to send a PUT "
                            "request to its URI (%s)."
                            % (repr_name, current_value)
                        )
                continue

            # If the new value is an object, make sure it provides the correct
            # interface.
            if value is not None and IReference.providedBy(field):
                # XXX leonardr 2008-04-12 spec=api-wadl-description:
                # This should be moved into the
                # ObjectLookupFieldMarshaller, once we make it
                # possible for Vocabulary fields to specify a schema
                # class the way IReference fields can.
                if value is not None and not field.schema.providedBy(value):
                    errors.append(
                        "%s: Your value points to the "
                        "wrong kind of object" % repr_name
                    )
                    continue

            # Obtain the current value of the field.  This gives us an easy
            # way to see if the client changed the value.
            current_value = getattr(self.entry, name)

            change_this_field = True
            # Read-only attributes can't be modified. It's okay to specify a
            # value for an attribute that can't be modified, but the new value
            # must be the same as the current value.  This makes it possible
            # to GET a document, modify one field, and send it back.
            if field.readonly:
                change_this_field = False
                if value != current_value:
                    errors.append(modified_read_only_attribute % repr_name)
                    continue

            if change_this_field is True and value != current_value:
                try:
                    # Do any field-specific validation.
                    field.validate(value)
                except ConstraintNotSatisfied as e:
                    # Try to get a string error message out of
                    # the exception; otherwise use a generic message
                    # instead of whatever object the raise site
                    # thought would be a good idea.
                    if len(e.args) > 0 and isinstance(e.args[0], str):
                        error = e.args[0]
                    else:
                        error = "Constraint not satisfied."
                    errors.append("%s: %s" % (repr_name, error))
                    continue
                except RequiredMissing:
                    error = "Missing required value."
                    errors.append("%s: %s" % (repr_name, error))
                except (ValueError, ValidationError) as e:
                    error = str(e)
                    if error == "":
                        error = "Validation error"
                    errors.append("%s: %s" % (repr_name, error))
                    continue
                validated_changeset.append((field, value))
        # If there are any fields left in the changeset, they're
        # fields that don't correspond to some field in the
        # schema. They're all errors.
        for invalid_field in changeset.keys():
            errors.append(
                "%s: You tried to modify a nonexistent "
                "attribute." % invalid_field
            )

        # If there were errors, display them and send a status of 400.
        if len(errors) > 0:
            self.request.response.setStatus(400)
            self.request.response.setHeader("Content-type", "text/plain")
            return "\n".join(errors)

        # Store the entry's current URL so we can see if it changes.
        original_url = absoluteURL(self.entry.context, self.request)

        if len(validated_changeset) > 0:
            # The representation will actually change.

            # Make a snapshot of the entry to use in a notification event.
            entry_before_modification = Snapshot(
                self.entry.context, providing=providedBy(self.entry.context)
            )

            # Make the changes, in the same order obtained from
            # get_entry_fields_in_write_order.
            for field, value in validated_changeset:
                field.set(self.entry, value)

            # ETags will need to be recalculated.
            self.etags_by_media_type = {}

            # Send a notification event.
            event = ObjectModifiedEvent(
                object=self.entry.context,
                object_before_modification=entry_before_modification,
                edited_fields=[field for field, value in validated_changeset],
            )
            notify(event)

            # The changeset contained new values for some of this object's
            # fields, and the notification event may have changed others.
            # Clear out any fields that changed.
            for name, cached in list(self._unmarshalled_field_cache.items()):
                cached, (field, old_value, flag) = cached
                if flag is IUnmarshallingDoesntNeedValue:
                    continue
                force_clear = False
                try:
                    new_value = getattr(self.entry, field.__name__)
                except Unauthorized:
                    new_value = old_value
                    if flag is not Unauthorized:
                        force_clear = True
                if force_clear or new_value != old_value:
                    del self._unmarshalled_field_cache[name]

        self._applyChangesPostHook()

        new_url = absoluteURL(self.entry.context, self.request)
        if new_url == original_url:
            # The resource did not move. Serve a new representation of
            # it. This might not necessarily be a representation of
            # the whole entry!
            self.request.response.setStatus(209)
            media_type = self.getPreferredSupportedContentType()
            self.request.response.setHeader("Content-type", media_type)
            return self._representation(media_type).encode()
        else:
            # The object moved. Serve a redirect to its new location.
            # This might not necessarily be the location of the entry!
            self.request.response.setStatus(301)
            self.request.response.setHeader(
                "Location", absoluteURL(self.context, self.request)
            )
            # RFC 2616 says the body of a 301 response, if present,
            # SHOULD be a note linking to the new object.
            return ""

    def _applyChangesPostHook(self):
        """A hook method called near the end of applyChanges.

        This method is called after the changes have been applied, but
        before the new representation is created.
        """
        pass


@implementer(IEntryFieldResource, IJSONPublishable)
class EntryFieldResource(FieldUnmarshallerMixin, EntryManipulatingResource):
    """An individual field of an entry."""

    SUPPORTED_CONTENT_TYPES = [HTTPResource.JSON_TYPE, HTTPResource.XHTML_TYPE]

    def __init__(self, context, request):
        """Initialize with respect to a context and request."""
        super().__init__(context, request)
        self.entry = self.context.entry

    def do_GET(self):
        """Create a representation of a single field."""
        media_type = self.handleConditionalGET()
        if media_type is None:
            # The conditional GET succeeded. Serve nothing.
            return b""
        else:
            self.request.response.setHeader("Content-Type", media_type)
            return self._representation(media_type).encode()

    def do_PUT(self, media_type, representation):
        """Overwrite the field's existing value with a new value."""
        value, error = self.processAsJSONDocument(media_type, representation)
        if value is None:
            return value, error
        changeset = {self.context.name: value}
        return self.applyChanges(changeset, media_type)

    do_PATCH = do_PUT

    def _getETagCores(self, cache=None):
        """Calculate the ETag for an entry field.

        The core of the ETag is the field value itself.

        :arg cache: is ignored.
        """
        value = self._unmarshallField(self.context.name, self.context.field)[1]

        # Append the revision number, because the algorithm for
        # generating the representation might itself change across
        # versions.
        revno = getUtility(IWebServiceConfiguration).code_revision
        return [core.encode() for core in [revno, str(value)]]

    def _representation(self, media_type):
        """Create a representation of the field value."""
        if media_type == self.JSON_TYPE:
            name, value = self._unmarshallField(
                self.context.name, self.context.field, CLOSEUP_DETAIL
            )
            return simplejson.dumps(value)
        elif media_type == self.XHTML_TYPE:
            name, value = self.unmarshallFieldToHTML(
                self.context.name, self.context.field
            )
            return decode_value(value)
        else:
            raise AssertionError(
                "No representation implementation for media type %s"
                % media_type
            )


@implementer(IEntryField, ILocation)
class EntryField:
    """A schema field bound by name to a particular entry."""

    def __init__(self, entry, field, name):
        """Initialize with respect to a named field of an entry."""
        self.entry = entry
        self.field = field.bind(entry)
        self.name = name

        # ILocation implementation
        self.__parent__ = self.entry.context
        self.__name__ = self.name


@adapter(EntryField, IHTTPRequest)
@implementer(IAbsoluteURL)
class EntryFieldURL(AbsoluteURL):
    """An IAbsoluteURL adapter for EntryField objects."""

    def __init__(self, entryfield, request):
        self.context = entryfield
        self.request = request


def make_entry_etag_cores(field_details):
    """Given the details of an entry's fields, calculate its ETag cores.

    :arg field_details: A list of field names and relevant field information,
    in particular whether or not the field is writable and its current value.
    """
    unwritable_values = []
    writable_values = []
    for name, details in field_details:
        if details["writable"]:
            # The client can write to this value.
            bucket = writable_values
        else:
            # The client can't write to this value (it might be read-only or
            # it might just be non-web-service writable.
            bucket = unwritable_values
        bucket.append(decode_value(details["value"]))

    unwritable = "\0".join(unwritable_values).encode()
    writable = "\0".join(writable_values).encode()
    return [unwritable, writable]


@implementer(IEntryResource, IJSONPublishable)
class EntryResource(
    CustomOperationResourceMixin,
    FieldUnmarshallerMixin,
    EntryManipulatingResource,
):
    """An individual object, published to the web."""

    SUPPORTED_CONTENT_TYPES = [
        HTTPResource.WADL_TYPE,
        HTTPResource.DEPRECATED_WADL_TYPE,
        HTTPResource.XHTML_TYPE,
        HTTPResource.JSON_TYPE,
        HTTPResource.JSON_PLUS_XHTML_TYPE,
    ]

    def __init__(self, context, request):
        """Associate this resource with a specific object and request."""
        super().__init__(context, request)
        self.entry = getMultiAdapter((context, request), IEntry)

    def handleCustomPOST(self, operation_name):
        """See `CustomOperationResourceMixin`."""
        original_url = absoluteURL(self.entry.context, self.request)
        value = super().handleCustomPOST(operation_name)
        # We don't know what the custom operation might have done.
        # Remove this object from the representation cache, just to be
        # safe.
        cache = self._representation_cache
        if cache is not None:
            cache.delete(self.context)
        new_url = absoluteURL(self.entry.context, self.request)
        if original_url != new_url:
            # The object moved. Serve a redirect to its new location.
            # This might not necessarily be the location of the entry!
            self.request.response.setStatus(301)
            self.request.response.setHeader(
                "Location", absoluteURL(self.context, self.request)
            )
            return ""
        return value

    def _getETagCores(self, unmarshalled_field_values=None):
        """Calculate the ETag for an entry.

        :arg unmarshalled_field_values: A dict mapping field names to
        unmarshalled values, obtained during some other operation such
        as the construction of a representation.
        """
        if unmarshalled_field_values is None:
            unmarshalled_field_values = {}

        field_details = []
        for name, field in getFieldsInOrder(self.entry.schema):
            details = {}
            # Add in any values provided by the caller.
            # The value of the field is either passed in, or extracted.
            details["value"] = unmarshalled_field_values.get(
                name, self._unmarshallField(name, field)[1]
            )

            # The client can write to this field.
            details["writable"] = self.isModifiableField(field, True)

            field_details.append((name, details))

        return make_entry_etag_cores(field_details)

    def _etagMatchesForWrite(self, existing_etag, incoming_etags):
        """Make sure no other client has modified this resource.

        For a conditional read to succeed, the entire ETag must
        match. But for a conditional write to succeed, only the second
        half of the ETag must match. This prevents spurious 412 errors
        on conditional writes where the only fields that changed are
        read-only fields that can't possibly cause a conflict.
        """
        incoming_write_portions = map(extract_write_portion, incoming_etags)
        existing_write_portion = extract_write_portion(existing_etag)
        return existing_write_portion in incoming_write_portions

    def toDataForJSON(self, media_type=None):
        """Turn the object into a simple data structure."""
        return self.toDataStructure(media_type or self.JSON_TYPE)

    def toDataStructure(self, media_type):
        """Turn the object into a simple data structure.

        In this case, a dictionary containing all fields defined by
        the resource interface.

        The values in the dictionary may differ depending on the value
        of media_type.
        """
        data = OrderedDict()
        data["self_link"] = absoluteURL(self.context, self.request)
        if self.adapter_utility.publish_web_link:
            # Objects in the web service correspond to pages on some website.
            # Provide the link to the corresponding page on the website.
            browser_request = IWebBrowserOriginatingRequest(self.request)
            data["web_link"] = absoluteURL(self.context, browser_request)
        data["resource_type_link"] = self.type_url
        unmarshalled_field_values = {}
        html_renderings = {}
        for name, field in getFieldsInOrder(self.entry.schema):
            if media_type.startswith(self.JSON_TYPE):
                (
                    repr_name,
                    repr_value,
                    html_renderer,
                ) = self._field_with_html_renderer(name, field)
                if (
                    media_type == self.JSON_PLUS_XHTML_TYPE
                    and html_renderer != _default_html_renderer
                ):
                    # This field has an unusual HTML renderer.
                    if repr_value == self.REDACTED_VALUE:
                        # The data is redacted, so the HTML
                        # representation of that data should also
                        # be redacted.
                        html_value = self.REDACTED_VALUE
                    else:
                        html_value = html_renderer(repr_value)
                    html_renderings[repr_name] = html_value
            elif media_type == self.XHTML_TYPE:
                repr_name, repr_value = self.unmarshallFieldToHTML(name, field)
            else:
                raise AssertionError(
                    "Cannot create data structure for media type %s"
                    % media_type
                )
            data[repr_name] = repr_value
            unmarshalled_field_values[name] = repr_value

        if len(html_renderings) > 0:
            data["lp_html"] = html_renderings
        elif media_type == self.JSON_PLUS_XHTML_TYPE:
            # The client requested application/json;include=lp_html,
            # but there's no HTML to deliver. Set the Content-Type to
            # regular application/json.
            self.request.response.setHeader("Content-Type", self.JSON_TYPE)
        etag = self.getETag(media_type, unmarshalled_field_values)
        data["http_etag"] = etag
        return data

    def toXHTML(self):
        """Represent this resource as an XHTML document."""
        view = getMultiAdapter(
            (self.context, self.request), name="lazr.restful.EntryResource"
        )
        return view()

    def processAsJSONHash(self, media_type, representation):
        """Process an incoming representation as a JSON hash.

        :param media_type: The specified media type of the incoming
        representation.

        :representation: The incoming representation:

        :return: A tuple (dictionary, error). 'dictionary' is a Python
        dictionary corresponding to the incoming JSON hash. 'error' is
        an error message if the incoming representation could not be
        processed. If there is an error, this method will set an
        appropriate HTTP response code.
        """

        value, error = self.processAsJSONDocument(media_type, representation)
        if value is None:
            return value, error
        if not isinstance(value, dict):
            self.request.response.setStatus(400)
            return None, "Expected a JSON hash."
        return value, None

    def do_GET(self):
        """Render an appropriate representation of the entry."""
        # Handle a custom operation, probably a search.
        operation_name = self.request.form.pop("ws.op", None)
        if operation_name is not None:
            result = self.handleCustomGET(operation_name)
            if isinstance(result, (bytes, str)):
                # The custom operation took care of everything and
                # just needs this string served to the client.
                return result
        else:
            # No custom operation was specified. Implement a standard
            # GET, which serves a JSON or WADL representation of the
            # entry.
            media_type = self.handleConditionalGET()
            if media_type is None:
                # The conditional GET succeeded. Serve nothing.
                return b""
            else:
                self.request.response.setHeader("Content-Type", media_type)
                return self._representation(media_type).encode()

    def do_PUT(self, media_type, representation):
        """Modify the entry's state to match the given representation.

        A PUT is just like a PATCH, except the given representation
        must be a complete representation of the entry.
        """
        changeset, error = self.processAsJSONHash(media_type, representation)
        if error is not None:
            return error

        # Make sure the representation includes values for all
        # writable attributes.
        #
        # Get the fields ordered by schema order so that we always
        # evaluate them in the same order. This is needed to predict
        # errors when testing.
        for name, field in getFieldsInOrder(self.entry.schema):
            if not self.isModifiableField(field, True):
                continue
            field = field.bind(self.context)
            marshaller = getMultiAdapter(
                (field, self.request), IFieldMarshaller
            )
            repr_name = marshaller.representation_name
            if (
                changeset.get(repr_name) is None
                and getattr(self.entry, name) is not None
            ):
                # This entry has a value for the attribute, but the
                # entity-body of the PUT request didn't make any assertion
                # about the attribute. The resource's behavior under HTTP
                # is undefined; we choose to send an error.
                self.request.response.setStatus(400)
                return (
                    "You didn't specify a value for the attribute '%s'."
                    % repr_name
                )

        return self.applyChanges(changeset, media_type)

    def do_PATCH(self, media_type, representation):
        """Apply a JSON patch to the entry."""
        changeset, error = self.processAsJSONHash(media_type, representation)
        if error is not None:
            return error
        return self.applyChanges(changeset, media_type)

    def _applyChangesPostHook(self):
        """See `EntryManipulatingResource`."""
        # Also remove the modified object from the representation
        # cache. This ensures a 209 status code will be accompanied
        # with a brand new representation.
        cache = self._representation_cache
        if cache is not None:
            cache.delete(self.context)

    @property
    def type_url(self):
        """The URL to the resource type for this resource."""
        return "%s#%s" % (
            absoluteURL(
                self.request.publication.getApplication(self.request),
                self.request,
            ),
            self.adapter_utility.singular_type,
        )

    @property
    def adapter_utility(self):
        """An EntryAdapterUtility for this resource."""
        return EntryAdapterUtility(self.entry.__class__)

    @property
    def redacted_fields(self):
        """Names the fields the current user doesn't have permission to see."""
        failures = []
        orig_interfaces = self.entry._orig_interfaces
        for name, field in getFieldsInOrder(self.entry.schema):
            try:
                # Can we view the field's value? We check the
                # permission directly using the Zope permission
                # checker, because doing it indirectly by fetching the
                # value may have very slow side effects such as
                # database hits.
                try:
                    tagged_values = field.getTaggedValue(
                        "lazr.restful.exported"
                    )
                    original_name = tagged_values["original_name"]
                except KeyError:
                    # This field has no tagged values, or is missing
                    # the 'original_name' value. Its entry class was
                    # probably created by hand rather than by tagging
                    # an interface. In that case, it's the
                    # programmer's responsibility to set
                    # 'original_name' if the web service field name
                    # differs from the underlying interface's field
                    # name. Since 'original_name' is not present, assume the
                    # names are the same.
                    original_name = name
                context = orig_interfaces[name](self.context)
                try:
                    checker = getChecker(context)
                except TypeError:
                    # This is more expensive than using a Zope checker, but
                    # there is no checker, so either there is no permission
                    # control on this object, or permission control is
                    # implemented some other way. Also note that we use
                    # getattr() on self.entry rather than self.context because
                    # some of the fields in entry.schema will be provided by
                    # adapters rather than directly by self.context.
                    getattr(self.entry, name)
                else:
                    checker.check(context, original_name)
            except Unauthorized:
                # This is an expensive operation that will make this
                # request more expensive still, but it happens
                # relatively rarely.
                repr_name, repr_value = self._unmarshallField(name, field)
                failures.append(repr_name)
        return failures

    def isModifiableField(self, field, is_external_client):
        """Returns true if this field's value can be changed.

        Collection fields, and fields that are not part of the web
        service interface, are never modifiable. Read-only fields are
        not modifiable by external clients.

        :param is_external_client: Whether the code trying to modify
        the field is an external client. Read-only fields cannot be
        directly modified from external clients, but they might change
        as side effects of other changes.
        """
        if ICollectionField.providedBy(field) or field.__name__.startswith(
            "_"
        ):
            return False
        if field.readonly:
            return not is_external_client
        return True

    def _representation(self, media_type):
        """Return a representation of this entry, of the given media type."""

        if media_type in [self.WADL_TYPE, self.DEPRECATED_WADL_TYPE]:
            return self.toWADL()
        elif media_type in (self.JSON_TYPE, self.JSON_PLUS_XHTML_TYPE):
            cache = self._representation_cache
            if cache is None:
                representation = None
            else:
                representation = cache.get(
                    self.context, media_type, self.request.version
                )

            redacted_fields = self.redacted_fields
            if representation is None:
                # Either there is no active cache, or the representation
                # wasn't in the cache.
                representation = simplejson.dumps(
                    self, cls=ResourceJSONEncoder, media_type=media_type
                )
                # If there's an active cache, and this representation
                # doesn't contain any redactions, store it in the
                # cache.
                if cache is not None and len(redacted_fields) == 0:
                    cache.set(
                        self.context,
                        self.JSON_TYPE,
                        self.request.version,
                        representation,
                    )
            else:
                # We have a representation, but we might not be able
                # to use it as-is.

                # First, check to see if the user can see this
                # representation at all. If absoluteURL raises
                # Unauthorized, they can't see it--they shouldn't even
                # know its URL.
                absoluteURL(self.context, self.request)

                if len(redacted_fields) != 0:
                    # The user can see parts of this representation
                    # but not other parts. We need to deserialize it,
                    # redact certain fields, and reserialize
                    # it. Hopefully this is faster than generating the
                    # representation from scratch!
                    json = simplejson.loads(representation)
                    for field in redacted_fields:
                        json[field] = self.REDACTED_VALUE
                    # There's no need to use the ResourceJSONEncoder,
                    # because we loaded the cached representation
                    # using the standard decoder.
                    representation = simplejson.dumps(json)
            return representation
        elif media_type == self.XHTML_TYPE:
            return self.toXHTML()
        else:
            raise AssertionError(
                "No representation implementation for media type %s"
                % media_type
            )

    @property
    def _representation_cache(self):
        """Return the representation cache, or None if missing/disabled."""
        try:
            cache = getUtility(IRepresentationCache)
        except ComponentLookupError:
            # There's no representation cache.
            return None
        config = getUtility(IWebServiceConfiguration)
        if config.enable_server_side_representation_cache:
            return cache
        return None


@implementer(ICollectionResource)
class CollectionResource(
    BatchingResourceMixin, CustomOperationResourceMixin, ReadOnlyResource
):
    """A resource that serves a list of entry resources."""

    def __init__(self, context, request):
        """Associate this resource with a specific object and request."""
        super().__init__(context, request)
        if ICollection.providedBy(context):
            self.collection = context
        else:
            self.collection = getMultiAdapter((context, request), ICollection)

    def do_GET(self):
        """Fetch a collection and render it as JSON."""
        # Handle a custom operation, probably a search.
        operation_name = self.request.form.pop("ws.op", None)
        if operation_name is not None:
            result = self.handleCustomGET(operation_name)
            if isinstance(result, (bytes, str)):
                # The custom operation took care of everything and
                # just needs this string served to the client.
                return result
        else:
            # No custom operation was specified. Implement a standard
            # GET, which serves a JSON or WADL representation of the
            # collection.
            entries = self.collection.find()
            if entries is None:
                raise NotFound(self, self.collection_name)

            media_type = self.getPreferredSupportedContentType()
            if media_type in [self.DEPRECATED_WADL_TYPE, self.WADL_TYPE]:
                result = self.toWADL().encode("utf-8")
                self.request.response.setHeader("Content-Type", media_type)
                return result

            result = self.batch(entries) + "}"

        self.request.response.setHeader("Content-type", self.JSON_TYPE)
        return result

    def batch(self, entries=None, request=None):
        """Return a JSON representation of a batch of entries.

        :param entries: (Optional) A precomputed list of entries to batch.
        :param request: (Optional) The current request.
        """
        if entries is None:
            entries = self.collection.find()
        if request is None:
            request = self.request
        result = super().batch(entries, request)
        result += ', "resource_type_link" : ' + simplejson.dumps(self.type_url)
        return result

    @property
    def type_url(self):
        "The URL to the resource type for the object."

        if IScopedCollection.providedBy(self.collection):
            # Scoped collection. The type URL depends on what type of
            # entry the collection holds.
            schema = self.context.relationship.value_type.schema
            adapter = EntryAdapterUtility.forSchemaInterface(
                schema, self.request
            )
            return adapter.entry_page_type_link
        else:
            # Top-level collection.
            schema = self.collection.entry_schema
            adapter = EntryAdapterUtility.forEntryInterface(
                schema, self.request
            )
            return adapter.collection_type_link


@implementer(IServiceRootResource, IJSONPublishable)
class ServiceRootResource(HTTPResource):
    """A resource that responds to GET by describing the service."""

    # A preparsed template file for WADL representations of the root.
    WADL_TEMPLATE = LazrPageTemplateFile("templates/wadl-root.pt")

    def __init__(self):
        """Initialize the resource.

        The service root constructor is different from other
        HTTPResource constructors because Zope initializes the object
        with no request or context, and then passes the request in
        when it calls the service root object.
        """
        # We're not calling the superclass constructor because
        # it assumes it's being called in the context of a particular
        # request.
        # pylint:disable-msg=W0231
        self.etags_by_media_type = {}

    @property
    def request(self):
        """Fetch the current web service request."""
        return get_current_web_service_request()

    def _getETagCores(self, cache=None):
        """Calculate an ETag for a representation of this resource.

        The service root resource changes only when the software
        itself changes.
        """
        revno = getUtility(IWebServiceConfiguration).code_revision
        return [revno.encode()]

    def __call__(self, REQUEST=None):
        """Handle a GET request."""
        method = self.getRequestMethod(REQUEST)
        if method == "GET":
            result = self.do_GET()
        else:
            REQUEST.response.setStatus(405)
            REQUEST.response.setHeader("Allow", "GET")
            result = ""
        return result

    def setCachingHeaders(self):
        "How long should the client cache this service root?"
        user_agent = self.request.getHeader("User-Agent", "")
        if user_agent.startswith("Python-httplib2"):
            # XXX leonardr 20100412
            # bug=http://code.google.com/p/httplib2/issues/detail?id=97
            #
            # A client with a User-Agent of "Python/httplib2" (such as
            # old versions of lazr.restfulclient) gives inconsistent
            # results when a resource is served with both ETag and
            # Cache-Control. We check for that User-Agent and omit the
            # Cache-Control headers if it makes a request.
            return
        config = getUtility(IWebServiceConfiguration)
        caching_policy = config.caching_policy
        if self.request.version == config.active_versions[-1]:
            max_age = caching_policy[-1]
        else:
            max_age = caching_policy[0]
        if max_age > 0:
            self.request.response.setHeader(
                "Cache-Control", "max-age=%d" % max_age
            )
            # Also set the Date header so that client-side caches will
            # have something to work from.
            self.request.response.setHeader("Date", formatdate(time.time()))

    def do_GET(self):
        """Describe the capabilities of the web service."""
        media_type = self.handleConditionalGET()
        self.setCachingHeaders()
        if media_type is None:
            # The conditional GET succeeded. Serve nothing.
            return b""
        elif media_type in [self.WADL_TYPE, self.DEPRECATED_WADL_TYPE]:
            result = self.toWADL()
        elif media_type == self.JSON_TYPE:
            # Serve a JSON map containing links to all the top-level
            # resources.
            result = simplejson.dumps(self, cls=ResourceJSONEncoder)

        self.request.response.setHeader("Content-Type", media_type)
        return result.encode("utf-8")

    def toWADL(self):
        # Find all resource types.
        site_manager = getGlobalSiteManager()
        entry_classes = []
        collection_classes = []
        singular_names = {}
        plural_names = {}

        # Determine the name of the earliest version.
        # We'll be using this later.
        config = getUtility(IWebServiceConfiguration)
        earliest_version = config.active_versions[0]

        for registration in sorted(site_manager.registeredAdapters()):
            provided = registration.provided
            if IInterface.providedBy(provided):
                if provided.isOrExtends(IEntry) and IEntry.implementedBy(
                    registration.factory
                ):
                    # The implementedBy check is necessary because
                    # some IEntry adapters aren't classes with
                    # schemas; they're functions. We can ignore these
                    # functions because their return value will be one
                    # of the classes with schemas, which we do describe.

                    # Make sure we have a registration relevant to
                    # this version. A given entry may have one
                    # registration for every web service version.
                    schema, version_marker = registration.required

                    if (
                        version_marker is IWebServiceClientRequest
                        and self.request.version != earliest_version
                    ):
                        # We are generating WADL for some version
                        # other than the earliest version, and this is
                        # a registration for the earliest version. We
                        # can ignore it.
                        #
                        # We need this special test because the normal
                        # test (below) is useless when
                        # version_marker is
                        # IWebServiceClientRequest. Since all request
                        # objects provide IWebServiceClientRequest
                        # directly, it will always show up in
                        # providedBy(self.request).
                        continue
                    if version_marker not in providedBy(self.request):
                        continue

                    # Make sure that no other entry class is using this
                    # class's singular or plural names.
                    adapter = EntryAdapterUtility.forSchemaInterface(
                        schema, self.request
                    )

                    singular = adapter.singular_type
                    assert (
                        singular not in singular_names
                    ), "Both %s and %s expose the singular name '%s'." % (
                        singular_names[singular].__name__,
                        schema.__name__,
                        singular,
                    )
                    singular_names[singular] = schema

                    plural = adapter.plural_type
                    assert (
                        plural not in plural_names
                    ), "Both %s and %s expose the plural name '%s'." % (
                        plural_names[plural].__name__,
                        schema.__name__,
                        plural,
                    )
                    plural_names[plural] = schema

                    entry_classes.append(registration.factory)
                elif (
                    provided.isOrExtends(ICollection)
                    and ICollection.implementedBy(registration.factory)
                    and not IScopedCollection.implementedBy(
                        registration.factory
                    )
                ):
                    # See comment above re: implementedBy check.
                    # We omit IScopedCollection because those are handled
                    # by the entry classes.
                    collection_classes.append(registration.factory)

        namespace = self.WADL_TEMPLATE.pt_getContext()
        namespace["service"] = self
        namespace["request"] = self.request
        namespace["entries"] = sorted_named_things(entry_classes)
        namespace["collections"] = sorted_named_things(collection_classes)
        return self.WADL_TEMPLATE.pt_render(namespace)

    def toDataForJSON(self, media_type):
        """Return a map of links to top-level collection resources.

        A top-level resource is one that adapts a utility.  Currently
        top-level entry resources (should there be any) are not
        represented.
        """
        type_url = "%s#%s" % (
            absoluteURL(
                self.request.publication.getApplication(self.request),
                self.request,
            ),
            "service-root",
        )
        data_for_json = {"resource_type_link": type_url}
        publications = self.getTopLevelPublications()
        for link_name, publication in publications.items():
            data_for_json[link_name] = absoluteURL(publication, self.request)
        return data_for_json

    def getTopLevelPublications(self):
        """Return a mapping of top-level link names to published objects."""
        top_level_resources = {}
        site_manager = getGlobalSiteManager()
        # First, collect the top-level collections.
        for registration in site_manager.registeredAdapters():
            provided = registration.provided
            if IInterface.providedBy(provided):
                # XXX sinzui 2008-09-29 bug=276079:
                # Top-level collections need a marker interface
                # so that so top-level utilities are explicit.
                if provided.isOrExtends(
                    ICollection
                ) and ICollection.implementedBy(registration.factory):
                    try:
                        utility = getUtility(registration.required[0])
                    except ComponentLookupError:
                        # It's not a top-level resource.
                        continue
                    entry_schema = registration.factory.entry_schema
                    if isinstance(entry_schema, property):
                        # It's not a top-level resource.
                        continue
                    adapter = EntryAdapterUtility.forEntryInterface(
                        entry_schema, self.request
                    )
                    link_name = "%s_collection_link" % adapter.plural_type
                    top_level_resources[link_name] = utility
        # Now, collect the top-level entries.
        for utility in getAllUtilitiesRegisteredFor(ITopLevelEntryLink):
            link_name = "%s_link" % utility.link_name
            top_level_resources[link_name] = utility

        return top_level_resources

    @property
    def type_url(self):
        "The URL to the resource type for this resource."
        adapter = self.adapter_utility

        return "%s#%s" % (
            absoluteURL(
                self.request.publication.getApplication(self.request),
                self.request,
            ),
            adapter.singular_type,
        )


@implementer(IEntry)
class Entry:
    """An individual entry."""

    def __init__(self, context, request):
        """Associate the entry with some database model object."""
        self.context = context
        self.request = request


@implementer(ICollection)
class Collection:
    """A collection of entries."""

    def __init__(self, context, request):
        """Associate the entry with some database model object."""
        self.context = context
        self.request = request


@implementer(IScopedCollection)
@adapter(Interface, Interface, IWebServiceLayer)
class ScopedCollection:
    """A collection associated with some parent object."""

    def __init__(self, context, collection, request):
        """Initialize the scoped collection.

        :param context: The object to which the collection is scoped.
        :param collection: The scoped collection.
        """
        self.context = context
        self.collection = collection
        self.request = request
        # Unknown at this time. Should be set by our call-site.
        self.relationship = None

    @property
    def entry_schema(self):
        """The schema for the entries in this collection."""
        # We are given a model schema (IFoo). Look up the
        # corresponding entry schema (IFooEntry).
        model_schema = self.relationship.value_type.schema
        request_interface = getUtility(
            IWebServiceVersion, name=self.request.version
        )
        return (
            getGlobalSiteManager()
            .adapters.lookup((model_schema, request_interface), IEntry)
            .schema
        )

    def find(self):
        """See `ICollection`."""
        return self.collection


class RESTUtilityBase:
    def _service_root_url(self):
        """Return the URL to the service root."""
        request = get_current_web_service_request()
        return absoluteURL(
            request.publication.getApplication(request), request
        )


class UnknownEntryAdapter(Exception):
    """Exception that signals no adaper could be found for an interface."""

    def __init__(self, adapted_interface_name, version):
        self.adapted_interface_name = adapted_interface_name
        self.version = version
        self.whence = ""

    def __str__(self):
        message = (
            "No IEntry adapter found for %s (web service version: %s)."
            % (self.adapted_interface_name, self.version)
        )
        if self.whence:
            message += "  " + self.whence
        return message


class EntryAdapterUtility(RESTUtilityBase):
    """Useful information about an entry's presence in the web service.

    This includes the links to entry's WADL resource type, and the
    resource type for a page of these entries.
    """

    @classmethod
    def forSchemaInterface(cls, entry_interface, request):
        """Create an entry adapter utility, given a schema interface.

        A schema interface is one that can be annotated to produce a
        subclass of IEntry.
        """
        request_interface = getUtility(
            IWebServiceVersion, name=request.version
        )
        entry_class = getGlobalSiteManager().adapters.lookup(
            (entry_interface, request_interface), IEntry
        )
        if entry_class is None:
            raise UnknownEntryAdapter(
                entry_interface.__name__, request.version
            )
        return EntryAdapterUtility(entry_class)

    @classmethod
    def forEntryInterface(cls, entry_interface, request):
        """Create an entry adapter utility, given a subclass of IEntry."""
        registrations = getGlobalSiteManager().registeredAdapters()
        # There should be one IEntry subclass registered for every
        # version of the web service. We'll go through the appropriate
        # IEntry registrations looking for one associated with the
        # same IWebServiceVersion interface we find on the 'request'
        # object.
        entry_classes = [
            registration.factory
            for registration in registrations
            if (
                IInterface.providedBy(registration.provided)
                and registration.provided.isOrExtends(IEntry)
                and entry_interface.implementedBy(registration.factory)
                and registration.required[1].providedBy(request)
            )
        ]
        assert (
            not len(entry_classes) > 1
        ), "%s provides more than one IEntry subclass for version %s." % (
            entry_interface.__name__,
            request.version,
        )
        assert (
            not len(entry_classes) < 1
        ), "%s does not provide any IEntry subclass for version %s." % (
            entry_interface.__name__,
            request.version,
        )
        return EntryAdapterUtility(entry_classes[0])

    def __init__(self, entry_class):
        """Initialize with a class that implements IEntry."""
        self.entry_class = entry_class

    @property
    def entry_interface(self):
        """The IEntry subclass implemented by this entry type."""
        interfaces = implementedBy(self.entry_class)
        entry_ifaces = [
            interface for interface in interfaces if interface.extends(IEntry)
        ]
        if len(entry_ifaces) != 1:
            raise AssertionError(
                "There must be one and only one IEntry implementation "
                "for %s, found %s"
                % (
                    self.entry_class,
                    ", ".join(
                        interface.__name__ for interface in entry_ifaces
                    ),
                )
            )
        return entry_ifaces[0]

    def _get_tagged_value(self, tag):
        """Return a tagged value from the entry interface."""
        return self.entry_interface.getTaggedValue(LAZR_WEBSERVICE_NAME)[tag]

    @property
    def publish_web_link(self):
        """Return true if this entry should have a web_link."""
        # If we can't adapt a web service request to a website
        # request, we shouldn't publish a web_link for *any* entry.
        web_service_request = get_current_web_service_request()
        website_request = IWebBrowserOriginatingRequest(
            web_service_request, None
        )
        return website_request is not None and self._get_tagged_value(
            "publish_web_link"
        )

    @property
    def singular_type(self):
        """Return the singular name for this object type."""
        return self._get_tagged_value("singular")

    @property
    def plural_type(self):
        """Return the plural name for this object type."""
        return self._get_tagged_value("plural")

    @property
    def type_link(self):
        """The URL to the type definition for this kind of entry."""
        return "%s#%s" % (self._service_root_url(), self.singular_type)

    @property
    def collection_type_link(self):
        """The definition of a top-level collection of this kind of object."""
        return "%s#%s" % (self._service_root_url(), self.plural_type)

    @property
    def entry_page_type(self):
        """The definition of a collection of this kind of object."""
        return "%s-page-resource" % self.singular_type

    @property
    def entry_page_type_link(self):
        "The URL to the definition of a collection of this kind of object."
        return "%s#%s" % (self._service_root_url(), self.entry_page_type)

    @property
    def entry_page_representation_id(self):
        "The name of the description of a colleciton of this kind of object."
        return "%s-page" % self.singular_type

    @property
    def entry_page_representation_link(self):
        "The URL to the description of a collection of this kind of object."
        return "%s#%s" % (
            self._service_root_url(),
            self.entry_page_representation_id,
        )

    @property
    def full_representation_link(self):
        """The URL to the description of the object's full representation."""
        return "%s#%s-full" % (self._service_root_url(), self.singular_type)


def get_entry_fields_in_write_order(entry):
    """Return the entry's fields in the order they should be written to.

    The ordering is intended to 1) be deterministic for a given schema
    and 2) minimize the chance of conflicts. Fields that are just
    fields come before fields (believed to be) controlled by
    mutators. Within each group, fields are returned in the order they
    appear in the schema.

    :param entry: An object that provides IEntry.
    :return: A list of 2-tuples (field name, field object)
    """
    non_mutator_fields = []
    mutator_fields = []
    field_implementations = entry.__class__.__dict__
    for name, field in getFieldsInOrder(entry.schema):
        if name.startswith("_"):
            # This field is not part of the web service interface.
            continue

        # If this field is secretly a subclass of lazr.delegates
        # Passthrough (but not a direct instance of Passthrough), put
        # it at the end -- it's probably controlled by a mutator.
        implementation = field_implementations[name]
        if (
            issubclass(implementation.__class__, Passthrough)
            and implementation.__class__ is not Passthrough
        ):
            mutator_fields.append((name, field))
        else:
            non_mutator_fields.append((name, field))
    return non_mutator_fields + mutator_fields
