# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Marshallers for fields used in HTTP resources."""

__all__ = [
    "AbstractCollectionFieldMarshaller",
    "BoolFieldMarshaller",
    "BytesFieldMarshaller",
    "CollectionFieldMarshaller",
    "DateTimeFieldMarshaller",
    "DictFieldMarshaller",
    "FloatFieldMarshaller",
    "IntFieldMarshaller",
    "ObjectLookupFieldMarshaller",
    "SetFieldMarshaller",
    "SimpleFieldMarshaller",
    "SimpleVocabularyLookupFieldMarshaller",
    "TextFieldMarshaller",
    "TokenizedVocabularyFieldMarshaller",
    "URLDereferencingMixin",
    "VocabularyLookupFieldMarshaller",
]

from collections import OrderedDict
from datetime import datetime
from io import BytesIO
import re
from urllib.parse import unquote

import pytz
import simplejson

from zope.datetime import (
    DateTimeError,
    DateTimeParser,
)
from zope.component import (
    getMultiAdapter,
    getUtility,
)
from zope.interface import implementer
from zope.publisher.interfaces import NotFound
from zope.schema import Field
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL

from lazr.uri import (
    URI,
    InvalidURIError,
)

from lazr.restful.interfaces import (
    IFieldMarshaller,
    IUnmarshallingDoesntNeedValue,
    IServiceRootResource,
    IWebServiceConfiguration,
)


class URLDereferencingMixin:
    """A mixin for any class that dereferences URLs into objects."""

    def dereference_url(self, url):
        """Look up a resource in the web service by URL.

        Representations and custom operations use URLs to refer to
        resources in the web service. When processing an incoming
        representation or custom operation it's often necessary to see
        which object a URL refers to. This method calls the URL
        traversal code to dereference a URL into a published object.

        :param url: The URL to a resource.
        :raise NotFound: If the URL does not designate a
            published object.
        """
        config = getUtility(IWebServiceConfiguration)
        if config.use_https:
            site_protocol = "https"
            default_port = "443"
        else:
            site_protocol = "http"
            default_port = "80"
        full_request_host = self.request.get("HTTP_HOST", "localhost")
        if ":" in full_request_host:
            request_host, request_port = full_request_host.split(":", 2)
        else:
            request_host = full_request_host
            request_port = default_port

        if not isinstance(url, str):
            raise ValueError(
                "got '%s', expected string: %r" % (type(url).__name__, url)
            )
        if url.startswith("/"):
            # It's a relative URI. Resolve it relative to the root of this
            # version of the web service.
            service_root = getUtility(IServiceRootResource)
            root_uri = absoluteURL(service_root, self.request)
            uri = URI(root_uri).append(url[1:])
        else:
            uri = URI(url)
        protocol = uri.scheme
        host = uri.host
        port = uri.port or default_port
        path = uri.path
        query = uri.query
        fragment = uri.fragment

        url_host_and_http_host_are_identical = (
            host == request_host and port == request_port
        )
        if (
            not url_host_and_http_host_are_identical
            or protocol != site_protocol
            or query is not None
            or fragment is not None
        ):
            raise NotFound(self, url, self.request)

        path_parts = [unquote(part) for part in path.split("/")]
        path_parts.pop(0)
        path_parts.reverse()
        environ = {"PATH_INFO": path, "HTTP_HOST": full_request_host}
        server_url = self.request.get("SERVER_URL")
        if server_url is not None:
            environ["SERVER_URL"] = server_url
        else:
            environ["SERVER_URL"] = "%s://%s" % (
                site_protocol,
                full_request_host,
            )
        request = config.createRequest(BytesIO(), environ)
        request.setTraversalStack(path_parts)
        root = request.publication.getApplication(self.request)
        return request.traverse(root)

    def dereference_url_as_object(self, url):
        """Look up a data model object in the web service by URL."""
        try:
            resource = self.dereference_url(url)
        except NotFound:
            # The URL doesn't correspond to any real object.
            raise ValueError('No such object "%s".' % url)
        except InvalidURIError:
            raise ValueError('"%s" is not a valid URI.' % url)
        # We looked up the URL and got the thing at the other end of
        # the URL: a resource. But internally, a resource isn't a
        # valid value for any schema field. Instead we want the object
        # that serves as a resource's context. Any time we want to get
        # to the object underlying a resource, we need to strip its
        # security proxy.
        return removeSecurityProxy(resource).context


@implementer(IFieldMarshaller)
class SimpleFieldMarshaller:
    """A marshaller that returns the same value it's served.

    This implementation is meant to be subclassed.
    """

    # Set this to type or tuple of types that the JSON value must be of.
    _type = None

    def __init__(self, field, request):
        self.field = field
        self.request = request

    def marshall_from_json_data(self, value):
        """See `IFieldMarshaller`.

        When value is None, return None, otherwise call
        _marshall_from_json_data().
        """
        if value is None:
            return None
        return self._marshall_from_json_data(value)

    def marshall_from_request(self, value):
        """See `IFieldMarshaller`.

        Try to decode value as a JSON-encoded string and pass it on to
        _marshall_from_request() if it's not None. If value isn't a
        JSON-encoded string, interpret it as string literal.
        """
        if value != "":
            try:
                v = value
                if isinstance(v, bytes):
                    v = v.decode("utf8")  # assume utf8
                elif not isinstance(v, str):
                    v = str(v)
                value = simplejson.loads(v)
            except (ValueError, TypeError):
                # Pass the value as is. This saves client from having to encode
                # strings.
                pass
        if value is None:
            return None
        return self._marshall_from_request(value)

    def _marshall_from_request(self, value):
        """Hook method to marshall a non-null JSON value.

        Default is to just call _marshall_from_json_data() with the value.
        """
        return self._marshall_from_json_data(value)

    def _marshall_from_json_data(self, value):
        """Hook method to marshall a no-null value.

        Default is to return the value unchanged.
        """
        if self._type is not None:
            if not isinstance(value, self._type):
                if isinstance(self._type, (tuple, list)):
                    expected_name = ", ".join(
                        a_type.__name__ for a_type in self._type
                    )
                else:
                    expected_name = self._type.__name__
                raise ValueError(
                    "got '%s', expected %s: %r"
                    % (type(value).__name__, expected_name, value)
                )
        return value

    @property
    def representation_name(self):
        """See `IFieldMarshaller`.

        Return the field name as is.
        """
        return self.field.__name__

    def unmarshall(self, entry, value):
        """See `IFieldMarshaller`.

        Return the value as is.
        """
        return value

    def unmarshall_to_closeup(self, entry, value):
        """See `IFieldMarshaller`.

        Return the value as is.
        """
        return self.unmarshall(entry, value)


class BoolFieldMarshaller(SimpleFieldMarshaller):
    """A marshaller that transforms its value into an integer."""

    _type = bool


class IntFieldMarshaller(SimpleFieldMarshaller):
    """A marshaller that transforms its value into an integer."""

    _type = int


class FloatFieldMarshaller(SimpleFieldMarshaller):
    """A marshaller that transforms its value into an integer."""

    _type = (float, int)

    def _marshall_from_json_data(self, value):
        """See `SimpleFieldMarshaller`.

        Converts the value to a float.
        """
        return float(super()._marshall_from_json_data(value))


class BytesFieldMarshaller(SimpleFieldMarshaller):
    """FieldMarshaller for IBytes field."""

    _type = bytes
    _type_error_message = "not a string: %r"

    @property
    def representation_name(self):
        """See `IFieldMarshaller`.

        Represent as a link to another resource.
        """
        return "%s_link" % self.field.__name__

    def unmarshall(self, entry, bytestorage):
        """See `IFieldMarshaller`.

        Marshall as a link to the byte storage resource.
        """
        return "%s/%s" % (
            absoluteURL(entry.context, self.request),
            self.field.__name__,
        )

    def marshall_from_request(self, value):
        """See `IFieldMarshaller`.

        Reads the data from file-like object, and converts non-strings into
        one.  This overrides `marshall_from_request` rather than
        implementing the `_marshall_from_request` hook method because we
        need to suppress the default JSON-decoding behaviour: binary data
        can't be marshalled via JSON without additional encoding that we
        don't do, and lazr.restfulclient doesn't JSON-encode binary fields.
        """
        if value is None:
            return None
        if hasattr(value, "seek"):
            value.seek(0)
            value = value.read()
        elif not isinstance(value, (bytes, str)):
            value = str(value).encode()
        else:
            # Leave string conversion to _marshall_from_json_data.
            pass
        return self._marshall_from_json_data(value)

    def _marshall_from_json_data(self, value):
        """See `SimpleFieldMarshaller`.

        Convert all strings to byte strings.
        """
        if isinstance(value, str):
            value = value.encode()
        return super()._marshall_from_json_data(value)


class TextFieldMarshaller(SimpleFieldMarshaller):
    """FieldMarshaller for IText fields."""

    _type = str
    _type_error_message = "not a unicode string: %r"

    def _marshall_from_request(self, value):
        """See `SimpleFieldMarshaller`.

        Converts the value to unicode.
        """
        value = str(value)
        # multipart/form-data encoding of text fields is required (RFC 2046
        # section 4.1.1) to use CRLF for line breaks.  Normalize to
        # Unix-style LF.
        value = re.sub(r"\r\n?", "\n", value)
        return super()._marshall_from_request(value)


class FixedVocabularyFieldMarshaller(SimpleFieldMarshaller):
    """A marshaller for vocabulary fields whose vocabularies are fixed."""

    def __init__(self, field, request, vocabulary):
        """Initialize with respect to a field.

        :vocabulary: This argument is ignored; field.vocabulary is the
            same object. This argument is passed because the
            VocabularyLookupFieldMarshaller uses the vocabulary as
            part of a multiadapter lookup of the appropriate
            marshaller.
        """
        super().__init__(field, request)

    def unmarshall_to_closeup(self, entry, value):
        """Describe all values, not just the selected value."""
        unmarshalled = []
        for item in self.field.vocabulary:
            item_dict = {"token": item.token, "title": item.title}
            if value and value.title == item.title:
                item_dict["selected"] = True
            unmarshalled.append(item_dict)
        return unmarshalled


class TokenizedVocabularyFieldMarshaller(FixedVocabularyFieldMarshaller):
    """A marshaller that looks up value using a token in a vocabulary."""

    def __init__(self, field, request, vocabulary):
        super().__init__(field, request, vocabulary)

    def _marshall_from_json_data(self, value):
        """See `SimpleFieldMarshaller`.

        Looks up the value as a token in the vocabulary.
        """
        try:
            return self.field.vocabulary.getTermByToken(str(value)).value
        except LookupError:
            raise ValueError("%r isn't a valid token" % value)


class DateTimeFieldMarshaller(SimpleFieldMarshaller):
    """A marshaller that transforms its value into a datetime object."""

    def _marshall_from_json_data(self, value):
        """Parse the value as a datetime object."""
        try:
            value = DateTimeParser().parse(value)
            (
                year,
                month,
                day,
                hours,
                minutes,
                secondsAndMicroseconds,
                timezone,
            ) = value
            seconds = int(secondsAndMicroseconds)
            microseconds = int(
                round((secondsAndMicroseconds - seconds) * 1000000)
            )
            if timezone not in ["Z", "+0000", "-0000"]:
                raise ValueError("Time not in UTC.")
            return datetime(
                year,
                month,
                day,
                hours,
                minutes,
                seconds,
                microseconds,
                pytz.utc,
            )
        except DateTimeError:
            raise ValueError("Value doesn't look like a date.")
        except TypeError:
            # JSON will serialize '20090131' as a number
            raise ValueError("Value doesn't look like a date.")

    def unmarshall(self, entry, value):
        """See `IFieldMarshaller`.

        Represent the datetime in ISO 8601 format.
        """
        return None if value is None else value.isoformat()


class DateFieldMarshaller(DateTimeFieldMarshaller):
    """A marshaller that transforms its value into a date object."""

    def _marshall_from_json_data(self, value):
        """Parse the value as a datetime.date object."""
        super_class = super()
        date_time = super_class._marshall_from_json_data(value)
        return date_time.date()


class AbstractCollectionFieldMarshaller(SimpleFieldMarshaller):
    """A marshaller for AbstractCollections.

    It looks up the marshaller for its value-type, to handle its contained
    elements.
    """

    # The only valid JSON representation is a list.
    _type = list
    _type_error_message = "not a list: %r"

    def __init__(self, field, request):
        """See `SimpleFieldMarshaller`.

        This also looks for the appropriate marshaller for value_type.
        """
        super().__init__(field, request)
        self.value_marshaller = getMultiAdapter(
            (field.value_type or Field(), request), IFieldMarshaller
        )

    def _marshall_from_json_data(self, value):
        """See `SimpleFieldMarshaller`.

        Marshall every elements of the list using the appropriate
        marshaller.
        """
        value = super()._marshall_from_json_data(value)

        # In AbstractCollection subclasses, _type contains the type object,
        # which can be used as a factory.
        return self._python_collection_factory(
            self.value_marshaller.marshall_from_json_data(item)
            for item in value
        )

    def _marshall_from_request(self, value):
        """See `SimpleFieldMarshaller`.

        If the value isn't a list, transform it into a one-element list. That
        allows web client to submit one-element list of strings
        without having to JSON-encode it.

        Additionally, all items in the list are marshalled using the
        appropriate `IFieldMarshaller` for the value_type.
        """
        if not isinstance(value, list):
            value = [value]
        return self._python_collection_factory(
            self.value_marshaller.marshall_from_request(item) for item in value
        )

    @property
    def _python_collection_factory(self):
        """Create the appropriate python collection from a list."""
        # In AbstractCollection subclasses, _type contains the type object,
        # which can be used as a factory.
        return self.field._type

    def unmarshall(self, entry, value):
        """See `SimpleFieldMarshaller`.

        The collection is unmarshalled into a list and all its items are
        unmarshalled using the appropriate FieldMarshaller.
        """
        if value is None:
            return value

        return [
            self.value_marshaller.unmarshall(entry, item) for item in value
        ]


class SetFieldMarshaller(AbstractCollectionFieldMarshaller):
    """Marshaller for sets."""

    @property
    def _python_collection_factory(self):
        return set


class DictFieldMarshaller(SimpleFieldMarshaller):
    """A marshaller for Dicts.

    It looks up the marshallers for its (key-type, value-type), to handle its
    contained name/value pairs.
    """

    _type = dict
    _type_error_message = "not a dict: %r"

    def __init__(self, field, request):
        """See `SimpleFieldMarshaller`.

        This also looks for the appropriate marshaller for key_type and
        value_type. If key_type or value_type are not specified, the default
        field marshaller is used.
        """
        super().__init__(field, request)
        self.key_marshaller = getMultiAdapter(
            (field.key_type or Field(), request), IFieldMarshaller
        )
        self.value_marshaller = getMultiAdapter(
            (field.value_type or Field(), request), IFieldMarshaller
        )

    def _marshall_from_request(self, value):
        """See `IFieldMarshaller`.

        All items in the dict are marshalled using the appropriate
        `IFieldMarshaller` for the key_type, value_type.

        When coming in via HTML request parameters, the dict is sent as a list
        of comma separated "key,value" strings.
        If the value isn't a list or dict, transform it into a one-element
        list. That allows web client to submit one-element list of strings
        without having to JSON-encode it.
        """
        if not isinstance(value, list) and not isinstance(value, dict):
            value = [value]
        if isinstance(value, list):
            try:
                value = dict(nv.split(",", 2) for nv in value)
            except ValueError:
                raise ValueError("got '%s', list of name,value pairs" % value)
        return {
            self.key_marshaller.marshall_from_json_data(
                key
            ): self.value_marshaller.marshall_from_json_data(val)
            for key, val in value.items()
        }

    def _marshall_from_json_data(self, value):
        """See `SimpleFieldMarshaller`.

        Marshall the items in the dict using the appropriate
        (key,value) marshallers.

        The incoming value may be a list of name,value pairs in which case
        we convert to a dict first.
        """
        if isinstance(value, list):
            value = dict(value)
        # Call super to check for errors and raise a ValueError if necessary.
        value = super()._marshall_from_json_data(value)
        return {
            self.key_marshaller.marshall_from_json_data(
                key
            ): self.value_marshaller.marshall_from_json_data(val)
            for key, val in value.items()
        }

    def unmarshall(self, entry, value):
        """See `SimpleFieldMarshaller`.

        The value is unmarshalled into a dict and all its items are
        unmarshalled using the appropriate FieldMarshaller.
        """
        if value is None:
            return value
        # Use an ordered dict so that fields using this marshaller have a
        # stable ETag.
        return OrderedDict(
            (
                self.key_marshaller.unmarshall(entry, key),
                self.value_marshaller.unmarshall(entry, val),
            )
            for key, val in value.items()
        )


@implementer(IUnmarshallingDoesntNeedValue)
class CollectionFieldMarshaller(SimpleFieldMarshaller):
    """A marshaller for collection fields."""

    @property
    def representation_name(self):
        """See `IFieldMarshaller`.

        Make it clear that the value is a link to a collection.
        """
        return "%s_collection_link" % self.field.__name__

    def unmarshall(self, entry, value):
        """See `IFieldMarshaller`.

        This returns a link to the scoped collection.
        """
        return "%s/%s" % (
            absoluteURL(entry.context, self.request),
            self.field.__name__,
        )


def VocabularyLookupFieldMarshaller(field, request):
    """A marshaller that uses the underlying vocabulary.

    This is just a factory function that does another adapter lookup
    for a marshaller, one that can take into account the vocabulary
    in addition to the field type (presumably Choice) and the request.
    """
    return getMultiAdapter(
        (field, request, field.vocabulary), IFieldMarshaller
    )


class SimpleVocabularyLookupFieldMarshaller(FixedVocabularyFieldMarshaller):
    """A marshaller for vocabulary lookup by title."""

    def __init__(self, field, request, vocabulary):
        """Initialize the marshaller with the vocabulary it'll use."""
        super().__init__(field, request, vocabulary)
        self.vocabulary = vocabulary

    def _marshall_from_json_data(self, value):
        """Find an item in the vocabulary by title."""
        valid_titles = []
        for item in self.field.vocabulary.items:
            if item.title == value:
                return item
            valid_titles.append(item.title)
        raise ValueError(
            'Invalid value "%s". Acceptable values are: %s'
            % (value, ", ".join(valid_titles))
        )

    def unmarshall(self, entry, value):
        if value is None:
            return None
        return value.title


class ObjectLookupFieldMarshaller(
    SimpleFieldMarshaller, URLDereferencingMixin
):
    """A marshaller that turns URLs into data model objects.

    This marshaller can be used with a IChoice field (initialized
    with a vocabulary) or with an IReference field (no vocabulary).
    """

    def __init__(self, field, request, vocabulary=None):
        super().__init__(field, request)
        self.vocabulary = vocabulary

    @property
    def representation_name(self):
        """See `IFieldMarshaller`.

        Make it clear that the value is a link to an object, not an object.
        """
        return "%s_link" % self.field.__name__

    def unmarshall(self, entry, value):
        """See `IFieldMarshaller`.

        Represent an object as the URL to that object
        """
        repr_value = None
        if value is not None:
            repr_value = absoluteURL(value, self.request)
        return repr_value

    def _marshall_from_json_data(self, value):
        """See `IFieldMarshaller`.

        Look up the data model object by URL.
        """
        return self.dereference_url_as_object(value)
