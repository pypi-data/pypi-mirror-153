# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Base classes for one-off HTTP operations."""

import simplejson

from zope.component import getMultiAdapter, getUtility, queryMultiAdapter
from zope.event import notify
from zope.interface import Attribute, implementer, providedBy
from zope.interface.interfaces import IInterface
from zope.schema import Field
from zope.schema.interfaces import (
    IField,
    RequiredMissing,
    ValidationError,
    WrongType,
)
from zope.security.proxy import isinstance as zope_isinstance

from lazr.lifecycle.event import ObjectModifiedEvent
from lazr.lifecycle.snapshot import Snapshot

from lazr.restful.interfaces import (
    ICollection,
    IFieldMarshaller,
    IResourceDELETEOperation,
    IResourceGETOperation,
    IResourcePOSTOperation,
    IWebServiceConfiguration,
)
from lazr.restful.interfaces import ICollectionField, IReference
from lazr.restful.utils import is_total_size_link_active
from lazr.restful._resource import (
    BatchingResourceMixin,
    CollectionResource,
    ResourceJSONEncoder,
)


__all__ = [
    "IObjectLink",
    "ObjectLink",
    "ResourceOperation",
    "ResourceGETOperation",
    "ResourceDELETEOperation",
    "ResourcePOSTOperation",
]


class ResourceOperation(BatchingResourceMixin):
    """A one-off operation associated with a resource."""

    JSON_TYPE = "application/json"
    send_modification_event = False

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.total_size_only = False

    def total_size_link(self, navigator):
        """Return a link to the total size of a collection."""
        # If the version we're being asked for is equal to or later
        # than the version in which we started exposing
        # total_size_link, then include it; otherwise include
        # total_size.
        config = getUtility(IWebServiceConfiguration)
        if not is_total_size_link_active(self.request.version, config):
            # This is a named operation that includes the total size
            # inline rather than with a link.
            return None
        if not IResourceGETOperation.providedBy(self):
            # Only GET operations can have their total size split out into
            # a link, because only GET operations are safe.
            return None
        base = str(self.request.URL)
        query = navigator.getCleanQueryString()
        if query != "":
            query += "&"
        return base + "?" + query + "ws.show=total_size"

    def __call__(self):
        values, errors = self.validate()
        if len(errors) > 0:
            self.request.response.setStatus(400)
            self.request.response.setHeader("Content-type", "text/plain")
            return "\n".join(errors)

        if self.send_modification_event:
            snapshot = Snapshot(
                self.context, providing=providedBy(self.context)
            )

        response = self.call(**values)

        if self.send_modification_event:
            event = ObjectModifiedEvent(
                object=self.context,
                object_before_modification=snapshot,
                edited_fields=None,
            )
            notify(event)
        return self.encodeResult(response)

    def encodeResult(self, result):
        """Encode the result of a custom operation into a string.

        This method is responsible for turning the return value of a
        custom operation into a string that can be served . It's also
        responsible for setting the Content-Type header and the status
        code.
        """
        if (
            self.request.response.getHeader("Content-Type") is not None
            or self.request.response.getStatus() != 599
        ):
            # The operation took care of everything and just needs
            # this object served to the client.
            return result

        # The similar patterns in the two branches below suggest some deeper
        # symmetry that should be extracted.
        if queryMultiAdapter((result, self.request), ICollection):
            # If the result is a web service collection, serve only one
            # batch of the collection.
            collection = getMultiAdapter((result, self.request), ICollection)
            resource = CollectionResource(collection, self.request)
            if self.total_size_only:
                result = resource.get_total_size(collection)
            else:
                result = resource.batch() + "}"
        elif self.should_batch(result):
            if self.total_size_only:
                result = self.get_total_size(result)
            else:
                result = self.batch(result, self.request) + "}"
        else:
            # Serialize the result to JSON. Any embedded entries will be
            # automatically serialized.
            try:
                result = simplejson.dumps(result, cls=ResourceJSONEncoder)
            except TypeError:
                raise TypeError(
                    "Could not serialize object %s to JSON." % result
                )

        self.request.response.setStatus(200)
        self.request.response.setHeader("Content-Type", self.JSON_TYPE)
        return result

    def should_batch(self, result):
        """Whether the given response data should be batched."""
        if not IResourceGETOperation.providedBy(self):
            # Only GET operations have meaningful return values.
            return False

        if ICollectionField.providedBy(self.return_type):
            # An operation defined as returning a collection always
            # has its response batched.
            return True

        if zope_isinstance(result, (bytes, str, dict, set, list, tuple)):
            # Ordinary Python data structures generally are not
            # batched.
            return False

        if IReference.providedBy(self.return_type):
            # Single references can't be iterable.
            return False

        try:
            iter(result)
            # Objects that have iterators but aren't ordinary data structures
            # tend to be result-set objects. Batch them.
            return True
        except TypeError:
            pass

        # Any other objects (eg. Entries) are not batched.
        return False

    def validate(self):
        """Validate incoming arguments against the operation schema.

        :return: A tuple (values, errors). 'values' is a dictionary of
        validated, preprocessed values to be used as parameters when
        invoking the operation. 'errors' is a list of validation errors.
        """
        validated_values = {}
        errors = []

        # Take incoming string key-value pairs from the HTTP request.
        # Transform them into objects that will pass field validation,
        # and that will be useful when the operation is invoked.
        missing = object()
        for field in self.params:
            name = field.__name__
            field = field.bind(self.context)
            if (
                self.request.get(name, missing) is missing
                and not field.required
            ):
                value = field.default
            else:
                marshaller = getMultiAdapter(
                    (field, self.request), IFieldMarshaller
                )
                try:
                    value = marshaller.marshall_from_request(
                        self.request.form.get(name)
                    )
                except ValueError as e:
                    errors.append("%s: %s" % (name, e))
                    continue
            try:
                field.validate(value)
            except RequiredMissing:
                errors.append("%s: Required input is missing." % name)
            except ValidationError as e:
                errors.append("%s: %s" % (name, e))
            else:
                validated_values[name] = value
        return (validated_values, errors)

    def call(self, **kwargs):
        """Actually invoke the operation."""
        raise NotImplementedError


@implementer(IResourceGETOperation)
class ResourceGETOperation(ResourceOperation):
    """See `IResourceGETOperation`."""


@implementer(IResourceDELETEOperation)
class ResourceDELETEOperation(ResourceOperation):
    """See `IResourceDELETEOperation`."""


@implementer(IResourcePOSTOperation)
class ResourcePOSTOperation(ResourceOperation):
    """See `IResourcePOSTOperation`."""


class IObjectLink(IField):
    """Field containing a link to an object."""

    schema = Attribute(
        "schema", "The Interface of the Object on the other end of the link."
    )


@implementer(IObjectLink)
class ObjectLink(Field):
    """A reference to an object."""

    def __init__(self, schema, **kw):
        if not IInterface.providedBy(schema):
            raise WrongType

        self.schema = schema
        super().__init__(**kw)
