# Copyright 2008-2009 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.restful
#
# lazr.restful is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.restful is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.restful.  If not, see <http://www.gnu.org/licenses/>.
"""Interfaces for different kinds of HTTP resources."""

# Pylint doesn't grok zope interfaces.
# pylint: disable-msg=E0211,E0213

__all__ = [
    "IByteStorage",
    "IByteStorageResource",
    "ICollection",
    "ICollectionResource",
    "IEntry",
    "IEntryField",
    "IEntryFieldResource",
    "IEntryResource",
    "IFieldHTMLRenderer",
    "IFieldMarshaller",
    "IFileLibrarian",
    "IHTTPResource",
    "INotificationsProvider",
    "IJSONPublishable",
    "IJSONRequestCache",
    "IRepresentationCache",
    "IResourceOperation",
    "IResourceGETOperation",
    "IResourceDELETEOperation",
    "IResourcePOSTOperation",
    "IScopedCollection",
    "IServiceRootResource",
    "ITopLevelEntryLink",
    "ITraverseWithGet",
    "IUnmarshallingDoesntNeedValue",
    "IWebServiceConfiguration",
    "IWebBrowserInitiatedRequest",
    "LAZR_WEBSERVICE_NAME",
    "LAZR_WEBSERVICE_NS",
    "IWebBrowserOriginatingRequest",
    "IWebServiceClientRequest",
    "IWebServiceExceptionView",
    "IWebServiceLayer",
    "IWebServiceVersion",
]

from textwrap import dedent
from zope.schema import (
    Bool,
    Dict,
    Int,
    List,
    Text,
    TextLine,
)
from zope.interface import (
    Attribute,
    Interface,
)

# These two should really be imported from zope.interface, but
# the import fascist complains because they are not in __all__ there.
from zope.interface.interface import invariant
from zope.interface.exceptions import Invalid
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import (
    IBrowserRequest,
    IDefaultBrowserLayer,
)
from lazr.batchnavigator.interfaces import InvalidBatchSizeError

# Constants for periods of time
HOUR = 3600  # seconds

# The namespace prefix for LAZR web service-related tags.
LAZR_WEBSERVICE_NS = "lazr.restful"

# The namespace for LAZR web service tags having to do with the names
# of things.
LAZR_WEBSERVICE_NAME = "%s.name" % LAZR_WEBSERVICE_NS


class IHTTPResource(Interface):
    """An object published through HTTP."""

    def __call__():
        """Publish the object."""

    def getETag(media_type):
        "An ETag for this resource's current state."


class IJSONPublishable(Interface):
    """An object that can be published as a JSON data structure."""

    def toDataForJSON(media_type):
        """Return a representation that can be turned into JSON.

        The representation must consist entirely of simple data
        structures and IJSONPublishable objects.

        :param media_type: The media type that the data will be
        converted to. This will be application/json, obviously, but it
        may include parameters.
        """


class IServiceRootResource(IHTTPResource):
    """A service root object that also acts as a resource."""

    def getTopLevelPublications(request):
        """Return a mapping of top-level link names to published objects."""


class IEntryResource(IHTTPResource):
    """A resource that represents an individual object."""

    def do_GET():
        """Retrieve this entry.

        :return: A string representation.
        """

    def do_PATCH(representation):
        """Update this entry.

        Try to update the entry to the field and values sent by the client.

        :param representation: A JSON representation of the field and values
            that should be modified.
        :return: None or an error message describing validation errors. The
            HTTP status code should be set appropriately.
        """

    def getContext():
        """Return the underlying entry for this resource."""


class IEntryFieldResource(IHTTPResource):
    """A resource that represents one of an entry's fields."""

    def do_GET():
        """Retrieve the value of the field.

        :return: A string representation.
        """


class ICollectionResource(IHTTPResource):
    """A resource that represents a collection of entry resources."""

    def do_GET():
        """Retrieve this collection.

        :return: A string representation.
        """


class IResourceOperation(Interface):
    """A one-off operation invokable on a resource."""

    def __call__():
        """Invoke the operation and create the HTTP response.

        :returns: If the result is a string, it's assumed that the
        Content-Type was set appropriately, and the result is returned
        as is. Otherwise, the result is serialized to JSON and served
        as application/json.
        """

    send_modification_event = Attribute(
        "Whether or not to send out an event when this operation completes."
    )


class IResourceGETOperation(IResourceOperation):
    """A one-off operation invoked through GET.

    This might be a search or lookup operation.
    """

    return_type = Attribute(
        "The type of the resource returned by this operation, if any."
    )


class IResourceDELETEOperation(IResourceOperation):
    """A destructor operation invoked through DELETE.

    This should be an operation that deletes an entry.
    """


class IResourcePOSTOperation(IResourceOperation):
    """A one-off operation invoked through POST.

    This should be an operation that modifies the data set.
    """


class IEntry(Interface):
    """An entry, exposed as a resource by an IEntryResource."""

    schema = Attribute("The schema describing the data fields on this entry.")

    @invariant
    def schemaIsProvided(value):
        """Make sure that the entry also provides its schema."""
        if not value.schema.providedBy(value):
            raise Invalid(
                "%s doesn't provide its %s schema."
                % (type(value).__name__, value.schema.__name__)
            )


class ICollection(Interface):
    """A collection, driven by an ICollectionResource."""

    entry_schema = Attribute("The schema for this collection's entries.")

    def find():
        """Retrieve all entries in the collection under the given scope.

        :return: A list of IEntry objects.
        """


class IScopedCollection(ICollection):

    relationship = Attribute(
        "The relationship between an entry and a " "collection."
    )
    collection = Attribute("The collection scoped to an entry.")


class IFieldHTMLRenderer(Interface):
    """An interface that renders generic strings as HTML representations.

    This can be a callable class, or a function that returns another
    function.
    """

    def __call__(value):
        """Render the given string as HTML."""


class IWebServiceExceptionView(Interface):
    """The view that defines how errors are related to API clients."""

    status = Attribute("The HTTP status code to return.")


class IEntryField(Interface):
    """An individual field of an entry."""

    entry = Attribute("The entry whose field this is.")

    field = Attribute("The field, bound to the entry.")


class ITopLevelEntryLink(Interface):
    """A link to a special entry.

    For instance, an alias for the currently logged-in user.

    The link will be present in the representation of the service root
    resource.
    """

    link_name = Attribute(
        "The name of the link to this entry in the "
        "representation of the service root resource. "
        "'_link' will be automatically appended."
    )

    entry_type = Attribute(
        "The interface defined by the entry on the " "other end of the link."
    )


class IWebBrowserOriginatingRequest(Interface):
    """A browser request to an object also published on the web service.

    A web framework may define an adapter for this interface, allowing
    the web service to include, as part of an entry's representation,
    a link to that same entry as found on the website.
    """


class INotificationsProvider(Interface):
    """A response object which contains notifications.

    A web framework may define an adapter for this interface, allowing
    the web service to provide notifications to be sent to the client.
    """

    notifications = Attribute(
        dedent(
            """\
        A list of namedtuples (level, message) which can be used by the
        caller to display extra information about the completed request.
        'level' matches the standard logging levels:

        DEBUG = logging.DEBUG     # a debugging message
        INFO = logging.INFO       # simple confirmation of a change
        WARNING = logging.WARNING # action will not be successful unless...
        ERROR = logging.ERROR     # the previous action did not succeed
        """
        )
    )


class IWebServiceClientRequest(IBrowserRequest):
    """Interface for requests to the web service."""

    version = Attribute(
        "The version of the web service that the client " "requested."
    )


class IWebServiceLayer(IWebServiceClientRequest, IDefaultBrowserLayer):
    """Marker interface for registering views on the web service."""


class IWebServiceVersion(Interface):
    """Used to register IWebServiceClientRequest subclasses as utilities.

    Every version of a web service must register a subclass of
    IWebServiceClientRequest as an IWebServiceVersion utility, with a
    name that's the web service version name. For instance:

    registerUtility(IWebServiceClientRequestBeta,
                    IWebServiceVersion, name="beta")
    """

    pass


class IJSONRequestCache(Interface):
    """A cache of objects exposed as URLs or JSON representations."""

    links = Attribute("Objects whose links need to be exposed.")
    objects = Attribute(
        "Objects whose JSON representations need " "to be exposed."
    )


class IByteStorage(Interface):
    """A sequence of bytes stored on the server.

    The bytestream is expected to have a URL other than the one used
    by the web service.
    """

    alias_url = Attribute("The external URL to the byte stream.")
    filename = Attribute("Filename for the byte stream.")
    is_stored = Attribute(
        "Whether or not there's a previously created "
        "external byte stream here."
    )

    def createStored(mediaType, representation, filename=None):
        """Create a new stored bytestream.

        :param filename: The name of the file being stored. If None,
        the name of the storage field is used instead.
        """

    def deleteStored():
        """Delete an existing stored bytestream."""


class IByteStorageResource(IHTTPResource):
    """A resource that represents an external binary file."""

    def do_GET():
        """Redirect the client to the externally hosted file."""

    def do_PUT(media_type, representation):
        """Update the stored bytestream.

        :param media_type: The media type of the proposed new bytesteram.
        :param representation: The proposed new bytesteram.
        :return: None or an error message describing validation errors. The
            HTTP status code should be set appropriately.
        """

    def do_DELETE():
        """Delete the stored bytestream."""


class IFileLibrarian(Interface):
    """A class for managing uploaded files."""

    def get(key):
        """Retrieve a file by key."""

    def put(representation, filename):
        """Store a file in the librarian."""

    def delete(key):
        """Delete a file from the librarian."""


class IFieldMarshaller(Interface):
    """A mapper between schema fields and their representation on the wire."""

    representation_name = Attribute(
        "The name to use for this field within the representation."
    )

    def marshall_from_json_data(value):
        """Transform the given data value into an object.

        This is used in PATCH/PUT requests when modifying the field, to get
        the actual value to use from the data submitted via JSON.

        :param value: A value obtained by deserializing a string into
            a JSON data structure.

        :return: The value that should be used to update the field.

        """

    def marshall_from_request(value):
        """Return the value to use based on the request submitted value.

        This is used by operation where the data comes from either the
        query string or the form-encoded POST data.

        :param value: The value submitted as part of the request.

        :return: The value that should be used to update the field.
        """

    def unmarshall(entry, value):
        """Transform an object value into a value suitable for JSON.

        :param entry: The entry whose field this is.
        :value: The object value of the field.

        :return: A value that can be serialized as part of a JSON hash.
        """

    def unmarshall_to_closeup(entry, value):
        """Transform an object value into a detailed JSON-ready value.

        :param entry: The entry whose field this is.
        :value: The object value of the field.

        :return: A value that can be serialized as the representation of
            a field resource.
        :rtype: Any object that can be serialized to JSON. Usually a
            string.
        """


class IWebServiceConfiguration(Interface):
    """A group of configuration settings for a web service.

    These are miscellaneous strings that may differ in different web
    services.
    """

    caching_policy = List(
        value_type=Int(),
        default=[7 * 24 * HOUR, 1 * HOUR],
        title="The web service caching policy.",
        description="""A list of two numbers, each to be used in the
        'max-age' field of the Cache-Control header. The first number is
        used when serving the service root for any web service version
        except the latest one. The second number is used when serving the
        service root for the latest version (which probably changes more
        often).""",
    )

    enable_server_side_representation_cache = Bool(
        title="Enable the server-side representation cache.",
        default=True,
        description="""If this is false, the server-side representation
        cache will not be used, even if one is registered.""",
    )

    service_description = TextLine(
        title="Service description",
        description="""A human-readable description of the web service.

        The description may contain HTML, but if it does, it must be a
        valid XHTML fragment.
        """,
        default="",
    )

    view_permission = TextLine(
        title="View permission",
        default="zope.View",
        description="The permission to use when checking object visibility.",
    )

    path_override = TextLine(
        title="Web service path override",
        default="api",
        description="The path component for Ajax clients to use when making "
        "HTTP requests to the web service from their current virtual host. "
        "The use of this path component (/api/foo instead of /foo) will "
        "ensure that the request is processed as a web service request "
        "instead of a website request.",
    )

    use_https = Bool(
        title="Web service is secured",
        default=True,
        description="Whether or not requests to the web service are secured "
        "through SSL.",
    )

    hostname = TextLine(
        title="The hostname to be used in generated URLs.",
        description="You only need to specify this if you're using the "
        "RootResourceAbsoluteURL class from lazr.restful.simple. This is "
        "the hostname of the lazr.restful application.",
    )

    port = Int(
        title="The TCP port on which the web service is running.",
        description="Used in generated URLs.",
        default=0,
    )

    service_root_uri_prefix = TextLine(
        title="Any URL prefix necessary for the service root.",
        default="",
        description="If your web service is not located at the root of "
        "its domain (for instance, it's rooted at "
        "http://foo.com/web-service/ instead of http://api.foo/com/, "
        "put the URL prefix here. (In the example case, the URL prefix "
        "is 'web-service/').",
    )

    active_versions = List(
        value_type=TextLine(),
        default=[],
        title="The active versions of the web service.",
        description="""A list of names of active versions of this
        web service. They might be version numbers, names such as
        "beta", or the date a particular version was finalized.

        Newer versions should show up later in the list than earlier
        versions. It's recommended that the last version, located at
        the end of the list, be a floating development version called
        something like 'trunk' or 'devel': effectively an alias for
        "the most up-to-date code".

        This list must contain at least one version name.""",
    )

    version_descriptions = Dict(
        key_type=TextLine(),
        value_type=Text(),
        title="Human-readable descriptions of the web service versions.",
        description="""A dictionary mapping version names to
        human-readable descriptions. The descriptions should describe
        what distinguishes this version from other versions, and
        mention if/when the version will be removed.

        The descriptions may contain HTML, but if they do, they must be
        valid XHTML fragments.
        """,
        default={},
    )

    require_explicit_versions = Bool(
        default=False,
        description="""If true, each exported field and named
        operation must explicitly declare the first version in which
        it appears. If false, fields and operations are published in
        all versions.""",
    )

    last_version_with_mutator_named_operations = TextLine(
        default=None,
        description="""In earlier versions of lazr.restful, mutator methods
        were also published as named operations. This redundant
        behavior is no longer enabled by default, but this setting
        allows for backwards compatibility.

        Mutator methods will also be published as named operations in
        the version you specify here, and in any previous versions. In
        all subsequent versions, they will not be published as named
        operations.""",
    )

    first_version_with_total_size_link = TextLine(
        default=None,
        description="""In earlier versions of lazr.restful collections
        included a total_size field, now they include a total_size_link
        instead. Setting this value determines in which version the new
        behavior takes effect.""",
    )

    code_revision = TextLine(
        default="",
        description="""A string designating the current revision
        number of the code running the webservice. This may be a
        revision number from version control, or a hand-chosen version
        number.""",
    )

    show_tracebacks = Bool(
        title="Show tracebacks to end-users",
        default=True,
        description="Whether or not to show tracebacks in an HTTP response "
        "for a request that raised an exception.",
    )

    default_batch_size = Int(
        title="The default batch size to use when serving a collection",
        default=50,
        description="When the client requests a collection and doesn't "
        "specify how many entries they want, this many entries will be "
        "served them in the first page.",
    )

    max_batch_size = Int(
        title="The maximum batch size",
        default=300,
        description="When the client requests a batch of entries from "
        "a collection, they will not be allowed to request more entries "
        "in the batch than this.",
    )

    compensate_for_mod_compress_etag_modification = Bool(
        title="Accept incoming ETags that appear to have been modified "
        "in transit by Apache's mod_compress.",
        default=False,
        description="""When mod_compress compresses an outgoing
        representation, it (correctly) modifies the ETag. But when
        that ETag comes back in on a conditional GET or PUT request,
        mod_compress does _not_ transparently remove the modification,
        because it can't be sure which HTTP intermediary was
        responsible for modifying the ETag on the way out.

        Setting this value to True will tell lazr.restful that
        mod_compress is in use. lazr.restful knows what mod_compress
        does to outgoing ETags, and if this value is set, it will
        strip the modification from incoming ETags that appear to have
        been modified by mod_compress.

        Specifically: if lazr.restful generates an etag '"foo"',
        mod_compress will change it to '"foo"-gzip' or '"foo-gzip"',
        depending on the version. If this value is set to False,
        lazr.restful will not recognize '"foo"-gzip' or '"foo-gzip"'
        as being equivalent to '"foo"'. If this value is set to True,
        lazr.restful will treat all three strings the same way.

        This is a hacky solution, but until Apache issue 39727 is
        resolved, it's the best way to get the performance
        improvements of content-encoding in a real setup with multiple
        layers of HTTP intermediary. (An earlier attempt to use
        transfer-encoding instead of content-encoding failed because
        HTTP intermediaries strip the TE header.)
        """,
    )

    def createRequest(body_instream, environ):
        """A factory method that creates a request for the web service.

        It should have the correct publication set for the application.

        :param body_instream: A file-like object containing the request
            input stream.
        :param environ: A dict containing the request environment.
        """

    def get_request_user():
        """The user who made the current web service request.

        'User' here has whatever meaning it has in your application. This
        value will be fed back into your code.
        """

    def checkRequest(context, required_scopes):
        """Check whether the current request may call a particular method.

        Authenticated users may be limited to certain scopes, in which case
        they will only be able to use methods with corresponding `@scoped`
        decorators.  This method is called to check whether a call to a
        method on `context` tagged with `required_scopes` should be allowed.
        The return value is ignored; it only matters whether this raises a
        `zope.security.interfaces.Unauthorized` exception.

        For compatibility, if this method is unimplemented, it is treated as
        if it did not raise an exception.

        :param context: The context object.
        :param required_scopes: A list of scope names for this method, or
            None if the method is unscoped.
        :raises zope.security.interfaces.Unauthorized: if the call should
            not be allowed.
        """


class IUnmarshallingDoesntNeedValue(Interface):
    """A marker interface for unmarshallers that work without values.

    Most marshallers transform the value they're given, but some work
    entirely on the field name. If they use this marker interface
    we'll save time because we won't have to calculate the value.
    """


class IWebBrowserInitiatedRequest(Interface):
    """A marker interface for requests initiated by a web browser.

    Web browsers are broken in subtle ways that interact in complex
    ways with the parts of HTTP used in web services. It's useful to
    know when a request was initiated by a web browser so that
    responses can be tweaked for their benefit.
    """


class ITraverseWithGet(IPublishTraverse):
    """A marker interface for a class that uses get() for traversal.

    This is a simple way to handle traversal.
    """

    def get(request, name):
        """Traverse to a sub-object."""


class IRepresentationCache(Interface):
    """A cache for resource representations.

    Register an object as the utility for this interface and
    lazr.restful will use that object to cache resource
    representations. If no object is registered as the utility,
    representations will not be cached.

    This is designed to be used with memcached, but you can plug in
    other key-value stores. Note that this cache is intended to store
    string representations, not deserialized JSON objects or anything
    else.
    """

    def get(object, media_Type, version, default=None):
        """Retrieve a representation from the cache.

        :param object: An IEntry--the object whose representation you want.
        :param media_type: The media type of the representation to get.
        :param version: The version of the web service for which to
            fetch a representation.
        :param default: The object to return if no representation is
            cached for this object.

        :return: A string representation, or `default`.
        """
        pass

    def set(object, media_type, version, representation):
        """Add a representation to the cache.

        :param object: An IEntry--the object whose representation this is.
        :param media_type: The media type of the representation.
        :param version: The version of the web service in which this
            representation should be stored.
        :param representation: The string representation to store.
        """
        pass

    def delete(object):
        """Remove *all* of an object's representations from the cache.

        This means representations for every (supported) media type
        and every version of the web service. Currently the only
        supported media type is 'application/json'.

        :param object: An IEntry--the object being represented.
        """
        pass


InvalidBatchSizeError.__lazr_webservice_error__ = 400
