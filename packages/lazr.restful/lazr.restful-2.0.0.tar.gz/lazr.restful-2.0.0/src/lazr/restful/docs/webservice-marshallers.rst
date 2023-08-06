LAZR's field marshallers
************************

LAZR defines an interface for converting between the values that
come in on an HTTP request, and the object values appropriate for schema
fields. This is similar to Zope's widget interface, but much smaller.

To test the various marshallers we create a stub request and
application root.

    >>> from lazr.restful.testing.webservice import WebServiceTestPublication
    >>> from lazr.restful.simple import Request
    >>> from lazr.restful.example.base.root import (
    ...     CookbookServiceRootResource)
    >>> request = Request("", {'HTTP_HOST': 'cookbooks.dev'})
    >>> request.annotations[request.VERSION_ANNOTATION] = '1.0'
    >>> application = CookbookServiceRootResource()
    >>> request.setPublication(WebServiceTestPublication(application))
    >>> request.processInputs()

We also define some helpers to print values in a way that is unambiguous
across Python versions.

    >>> def pprint_dict(d):
    ...     print('{', end='')
    ...     print(
    ...         ', '.join(
    ...             '%r: %r' % (key, value)
    ...             for key, value in sorted(d.items())),
    ...         end='')
    ...     print('}')

IFieldMarshaller and SimpleFieldMarshaller
==========================================

There is a SimpleFieldMarshaller class that provides a good base to
implement that interface.

    >>> from zope.interface.verify import verifyObject
    >>> from lazr.restful.interfaces import IFieldMarshaller
    >>> from lazr.restful.marshallers import SimpleFieldMarshaller
    >>> from zope.schema import Text

    >>> field = Text(__name__='field_name')
    >>> marshaller = SimpleFieldMarshaller(field, request)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

representation_name
===================

The representation_name attribute is used to retrieve the name under
which the field should be stored in the JSON representation. In the
simple case, it's the same name as the field.

    >>> marshaller.representation_name
    'field_name'

marshall_from_json_data()
=========================

The marshall_from_json_data() method is used during PUT and PATCH
requests to transform the value provided in the JSON representation to a
value in the underlying schema field. In SimpleFieldMarshaller
implementation, the value is returned unchanged.

    >>> marshaller.marshall_from_json_data("foo")
    'foo'
    >>> marshaller.marshall_from_json_data(4)
    4
    >>> print(marshaller.marshall_from_json_data("unicode\u2122"))
    unicode™
    >>> marshaller.marshall_from_json_data("")
    ''
    >>> print(marshaller.marshall_from_json_data(None))
    None

marshall_from_request()
=======================

The marshall_from_request() method is used during operation invocation
to transform a value submitted via the query string or form-encoded POST
data into a value the will be accepted by the underlying schema field.

SimpleFieldMarshaller tries first to parse the value as a JSON-encoded
string, the resulting value is passed on to marshall_from_json_data().

    >>> print(marshaller.marshall_from_request("null"))
    None
    >>> marshaller.marshall_from_request("true")
    True
    >>> marshaller.marshall_from_request("false")
    False
    >>> marshaller.marshall_from_request('["True", "False"]')
    ['True', 'False']
    >>> marshaller.marshall_from_request("1")
    1
    >>> marshaller.marshall_from_request("-10.5")
    -10.5
    >>> marshaller.marshall_from_request('"a string"')
    'a string'
    >>> marshaller.marshall_from_request('"false"')
    'false'
    >>> marshaller.marshall_from_request('"null"')
    'null'

Invalid JSON-encoded strings are interpreted as string literals and
passed on directly to marshall_from_json_data(). That's for the
convenience of web clients, they don't need to encode string values in
quotes, or can pass lists using multiple key-value pairs.

    >>> marshaller.marshall_from_request("a string")
    'a string'
    >>> marshaller.marshall_from_request('False')
    'False'
    >>> marshaller.marshall_from_request("")
    ''
    >>> marshaller.marshall_from_request(' ')
    ' '
    >>> marshaller.marshall_from_request('\n')
    '\n'
    >>> marshaller.marshall_from_request(['value1', 'value2'])
    ['value1', 'value2']

unmarshall() and variants
=========================

The unmarshall() method is used to convert the field's value to a value
that can be serialized to JSON as part of an entry representation.  The
first parameter is the entry that the value is part of. That is used by
fields that transform the value into a URL, see the CollectionField
marshaller for an example. The second one is the value to convert.  In
the SimpleFieldMarshaller implementation, the value is returned
unchanged.

    >>> print(marshaller.unmarshall(None, 'foo'))
    foo
    >>> print(marshaller.unmarshall(None, None))
    None

When a more detailed representation is needed, unmarshall_to_closeup()
can be called. By default, this returns the same data as unmarshall(),
but specific marshallers may send more detailed information.

    >>> marshaller.unmarshall_to_closeup(None, 'foo')
    'foo'


Marshallers for basic data types
================================

Bool
----

The marshaller for a Bool field checks that the JSON value is either
True or False. A ValueError is raised when its not the case.

    >>> from zope.configuration import xmlconfig
    >>> zcmlcontext = xmlconfig.string("""
    ... <configure xmlns="http://namespaces.zope.org/zope">
    ...   <include package="lazr.restful" file="ftesting.zcml" />
    ... </configure>
    ... """)

    >>> from zope.component import getMultiAdapter
    >>> from zope.schema import Bool
    >>> field = Bool()
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

    >>> marshaller.marshall_from_json_data(True)
    True
    >>> marshaller.marshall_from_json_data(False)
    False
    >>> marshaller.marshall_from_json_data("true")
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected bool: 'true'
    >>> marshaller.marshall_from_json_data(1)
    Traceback (most recent call last):
      ...
    ValueError: got 'int', expected bool: 1

None is passed through though.

    >>> print(marshaller.marshall_from_json_data(None))
    None

Booleans are encoded using the standard JSON representation of 'true' or
'false'.

    >>> marshaller.marshall_from_request("true")
    True
    >>> marshaller.marshall_from_request("false")
    False

    >>> marshaller.marshall_from_request('True')
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected bool: 'True'

Int
---

The marshaller for an Int field checks that the JSON value is an
integer. A ValueError is raised when its not the case.

    >>> from zope.schema import Int
    >>> field = Int()
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

    >>> marshaller.marshall_from_json_data(-10)
    -10
    >>> marshaller.marshall_from_json_data("-10")
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected int: '-10'

None is passed through though.

    >>> print(marshaller.marshall_from_json_data(None))
    None

Integers are encoded using strings when in a request.

    >>> marshaller.marshall_from_request("4")
    4
    >>> marshaller.marshall_from_request("-4")
    -4

It raises a ValueError if the value cannot be converted to an integer.

    >>> marshaller.marshall_from_request("foo")
    Traceback (most recent call last):
    ...
    ValueError: got 'str', expected int: 'foo'

    >>> marshaller.marshall_from_request("4.62")
    Traceback (most recent call last):
    ...
    ValueError:  got 'float', expected int: 4.62...

Note that python octal and hexadecimal syntax isn't supported.

(This would 13 in octal notation.)

    >>> marshaller.marshall_from_request("015")
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected int: '015'

    >>> marshaller.marshall_from_request("0x04")
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected int: '0x04'

Float
-----

The marshaller for a Float field checks that the JSON value is indeed a
float.  A ValueError is raised when it's not the case.

    >>> from zope.schema import Float
    >>> field = Float()
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

    >>> marshaller.marshall_from_json_data(1.0)
    1.0
    >>> marshaller.marshall_from_json_data(-1.0)
    -1.0
    >>> marshaller.marshall_from_json_data("true")
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected float, int: 'true'

None is passed through though.

    >>> print(marshaller.marshall_from_json_data(None))
    None

And integers are automatically converted to a float.

    >>> marshaller.marshall_from_json_data(1)
    1.0

Floats are encoded using the standard JSON representation.

    >>> marshaller.marshall_from_request("1.2")
    1.2
    >>> marshaller.marshall_from_request("-1.2")
    -1.2
    >>> marshaller.marshall_from_request("-1")
    -1.0

    >>> marshaller.marshall_from_request('True')
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected float, int: 'True'

Datetime
--------

The marshaller for a Datetime field checks that the JSON value is indeed a
parsable datetime stamp.

    >>> from zope.schema import Datetime
    >>> field = Datetime()
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

    >>> marshaller.marshall_from_json_data('2009-07-07T13:15:00+0000')
    datetime.datetime(2009, 7, 7, 13, 15, tzinfo=<UTC>)

    >>> marshaller.marshall_from_json_data('2009-07-07T13:30:00-0000')
    datetime.datetime(2009, 7, 7, 13, 30, tzinfo=<UTC>)

    >>> marshaller.marshall_from_json_data('2009-07-07T13:45:00Z')
    datetime.datetime(2009, 7, 7, 13, 45, tzinfo=<UTC>)

    >>> marshaller.marshall_from_json_data('2009-07-08T14:30:00')
    datetime.datetime(2009, 7, 8, 14, 30, tzinfo=<UTC>)

    >>> marshaller.marshall_from_json_data('2009-07-09')
    datetime.datetime(2009, 7, 9, 0, 0, tzinfo=<UTC>)

The time zone must be UTC. An error is raised if is it clearly not UTC.

    >>> marshaller.marshall_from_json_data('2009-07-25T13:15:00+0500')
    Traceback (most recent call last):
      ...
    ValueError: Time not in UTC.

    >>> marshaller.marshall_from_json_data('2009-07-25T13:30:00-0200')
    Traceback (most recent call last):
      ...
    ValueError: Time not in UTC.

A ValueError is raised when the value is not parsable.

    >>> marshaller.marshall_from_json_data("now")
    Traceback (most recent call last):
      ...
    ValueError: Value doesn't look like a date.

    >>> marshaller.marshall_from_json_data('20090708')
    Traceback (most recent call last):
      ...
    ValueError: Value doesn't look like a date.

    >>> marshaller.marshall_from_json_data(20090708)
    Traceback (most recent call last):
      ...
    ValueError: Value doesn't look like a date.

The unmarshall() method returns the ISO 8601 representation of the value.

    >>> marshaller.unmarshall(
    ...     None, marshaller.marshall_from_json_data('2009-07-07T13:45:00Z'))
    '2009-07-07T13:45:00+00:00'

Date
----

The marshaller for a Date field checks that the JSON value is indeed a
parsable date.

    >>> from zope.schema import Date
    >>> field = Date()
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

    >>> marshaller.marshall_from_json_data('2009-07-09')
    datetime.date(2009, 7, 9)

The marshaller extends the Datetime marshaller. It will parse a datetime
stamp and return a date.

    >>> marshaller.marshall_from_json_data('2009-07-07T13:15:00+0000')
    datetime.date(2009, 7, 7)

The unmarshall() method returns the ISO 8601 representation of the value.

    >>> marshaller.unmarshall(
    ...     None, marshaller.marshall_from_json_data('2009-07-09'))
    '2009-07-09'

Text
----

The marshaller for IText field checks that the value is a unicode
string. A ValueError is raised when that's not the case.

    >>> from zope.schema import Text
    >>> field = Text()
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

    >>> marshaller.marshall_from_json_data("Test")
    'Test'
    >>> marshaller.marshall_from_json_data(1.0)
    Traceback (most recent call last):
      ...
    ValueError: got 'float', expected str: 1.0
    >>> marshaller.marshall_from_json_data(b'Test')
    Traceback (most recent call last):
      ...
    ValueError: got 'bytes', expected str: b'Test'

None is passed through though.

    >>> print(marshaller.marshall_from_json_data(None))
    None

When coming from the request, everything is interpreted as a unicode
string:

    >>> marshaller.marshall_from_request('a string')
    'a string'
    >>> marshaller.marshall_from_request(['a', 'b'])
    "['a', 'b']"
    >>> marshaller.marshall_from_request('true')
    'True'
    >>> marshaller.marshall_from_request('')
    ''

Except that 'null' still returns None.

    >>> print(marshaller.marshall_from_request('null'))
    None

Line breaks coming from the request are normalized to LF.

    >>> marshaller.marshall_from_request('abc\r\n\r\ndef\r\n')
    'abc\n\ndef\n'
    >>> marshaller.marshall_from_request('abc\n\ndef\n')
    'abc\n\ndef\n'
    >>> marshaller.marshall_from_request('abc\r\rdef\r')
    'abc\n\ndef\n'

Bytes
-----

Since there is no way to represent a bytes string in JSON, all strings
are converted to a byte string using UTF-8 encoding. If the value isn't
a string, a ValueError is raised.

    >>> from zope.schema import Bytes
    >>> field = Bytes(__name__='data')
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

    >>> marshaller.marshall_from_json_data("Test")
    b'Test'
    >>> marshaller.marshall_from_json_data('int\xe9ressant')
    b'int\xc3\xa9ressant'
    >>> marshaller.marshall_from_json_data(1.0)
    Traceback (most recent call last):
      ...
    ValueError: got 'float', expected ...: 1.0

Again, except for None which is passed through.

    >>> print(marshaller.marshall_from_json_data(None))
    None

When coming over the request, the value is also converted into a UTF-8
encoded string, with no JSON decoding.

    >>> marshaller.marshall_from_request("Test")
    b'Test'
    >>> marshaller.marshall_from_request('int\xe9ressant')
    b'int\xc3\xa9ressant'
    >>> marshaller.marshall_from_request(b'1.0')
    b'1.0'
    >>> marshaller.marshall_from_request(b'"not JSON"')
    b'"not JSON"'

Since multipart/form-data can be used to upload data, file-like objects
are read.

    >>> from io import BytesIO
    >>> marshaller.marshall_from_request(BytesIO(b'A line of data'))
    b'A line of data'

Bytes field used in an entry are stored in the librarian, so their
representation name states that it's a link.

    >>> marshaller.representation_name
    'data_link'

And the unmarshall() method returns a link that will serve the file.

    >>> from lazr.restful import EntryResource
    >>> from lazr.restful.example.base.interfaces import ICookbookSet
    >>> from zope.component import getUtility
    >>> entry_resource = EntryResource(
    ...     getUtility(ICookbookSet).get('Everyday Greens'), request)

(The value would be the BytesStorage instance used to store the
content, but it's not needed.)

    >>> marshaller.unmarshall(entry_resource, None)
    'http://.../cookbooks/Everyday%20Greens/data'

ASCIILine
---------

ASCIILine is a subclass of Bytes but is marshalled like text.

    >>> from zope.schema import ASCIILine
    >>> field = ASCIILine(__name__='field')
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

Unicode objects remain Unicode objects.

    >>> marshaller.marshall_from_json_data("Test")
    'Test'

Note that the marshaller accepts character values where bit 7 is set.

    >>> print(marshaller.marshall_from_json_data('int\xe9ressant'))
    intéressant

Non-string values like floats are rejected.

    >>> marshaller.marshall_from_json_data(1.0)
    Traceback (most recent call last):
      ...
    ValueError: got 'float', expected str: 1.0

None is passed through.

    >>> print(marshaller.marshall_from_json_data(None))
    None

When coming from the request, everything is interpreted as a unicode
string:

    >>> marshaller.marshall_from_request('a string')
    'a string'
    >>> marshaller.marshall_from_request(['a', 'b'])
    "['a', 'b']"
    >>> marshaller.marshall_from_request('true')
    'True'
    >>> marshaller.marshall_from_request('')
    ''
    >>> print(marshaller.marshall_from_request('int\xe9ressant'))
    intéressant
    >>> marshaller.marshall_from_request('1.0')
    '1.0'

But again, 'null' is returned as None.

    >>> print(marshaller.marshall_from_request('null'))
    None

Unlike a Bytes field, an ASCIILine field used in an entry is stored
as an ordinary attribute, hence its representation name is the attribute
name itself.

    >>> marshaller.representation_name
    'field'

Choice marshallers
==================

The marshaller for a Choice is chosen based on the Choice's
vocabulary.

    >>> from zope.schema import Choice

Choice for IVocabularyTokenized
-------------------------------

The default marshaller will use the vocabulary getTermByToken to
retrieve the value to use. It raises an error if the value isn't in the
vocabulary.

    >>> field = Choice(__name__='simple', values=[10, 'a value', True])
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True
    >>> marshaller.marshall_from_json_data(10)
    10
    >>> marshaller.marshall_from_json_data("a value")
    'a value'
    >>> marshaller.marshall_from_json_data(True)
    True
    >>> marshaller.marshall_from_request('true')
    True
    >>> marshaller.marshall_from_request('a value')
    'a value'
    >>> marshaller.marshall_from_request('10')
    10

    >>> marshaller.marshall_from_json_data('100')
    Traceback (most recent call last):
      ...
    ValueError: '100' isn't a valid token

None is always returned unchanged.

    >>> print(marshaller.marshall_from_json_data(None))
    None

Since this marshaller's Choice fields deal with small, fixed
vocabularies, their unmarshall_to_closeup() implementations to
describe the vocabulary as a whole.

    >>> for token in marshaller.unmarshall_to_closeup(None, '10'):
    ...     print(sorted(token.items()))
    [('title', None), ('token', '10')]
    [('title', None), ('token', 'a value')]
    [('title', None), ('token', 'True')]

And None is handled correctly.

    >>> for token in marshaller.unmarshall_to_closeup(None, None):
    ...     print(sorted(token.items()))
    [('title', None), ('token', '10')]
    [('title', None), ('token', 'a value')]
    [('title', None), ('token', 'True')]

Unicode Exceptions Sidebar
--------------------------

Because tracebacks with high-bit characters in them end up being displayed
like "ValueError: <unprintable ValueError object>" we'll use a helper to
display them the way we want.

    >>> def show_ValueError(callable, *args):
    ...     try:
    ...         callable(*args)
    ...     except ValueError as e:
    ...         print('ValueError:', str(e))


Choice of EnumeratedTypes
-------------------------

The JSON representation of the enumerated value is its title.  A string
that corresponds to one of the values is marshalled to the appropriate
value. A string that doesn't correspond to any enumerated value results
in a helpful ValueError.

    >>> from lazr.restful.example.base.interfaces import Cuisine
    >>> field = Choice(vocabulary=Cuisine)
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

    >>> marshaller.marshall_from_json_data("Dessert")
    <Item Cuisine.DESSERT, Dessert>

    >>> show_ValueError(marshaller.marshall_from_json_data, "NoSuchCuisine")
    ValueError: Invalid value "NoSuchCuisine". Acceptable values are: ...

    >>> show_ValueError(marshaller.marshall_from_json_data, "dessert")
    ValueError: Invalid value "dessert". Acceptable values are: ...

None is returned unchanged:

    >>> print(marshaller.marshall_from_json_data(None))
    None

This marshaller is for a Choice field describing a small, fixed
vocabularies. Because the vocabulary is small, its
unmarshall_to_closeup() implementation can describe the whole
vocabulary.

    >>> from operator import itemgetter
    >>> for cuisine in sorted(
    ...         marshaller.unmarshall_to_closeup(None, "Triaged"),
    ...         key=itemgetter("token")):
    ...     print(sorted(cuisine.items()))
    [('title', 'American'), ('token', 'AMERICAN')]
    ...
    [('title', 'Vegetarian'), ('token', 'VEGETARIAN')]


Objects
-------

An object is marshalled to its URL.

    >>> from lazr.restful.fields import Reference
    >>> from lazr.restful.example.base.interfaces import ICookbook
    >>> reference_field = Reference(schema=ICookbook)
    >>> reference_marshaller = getMultiAdapter(
    ...     (reference_field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, reference_marshaller)
    True

    >>> from lazr.restful.example.base.root import COOKBOOKS
    >>> cookbook = COOKBOOKS[0]
    >>> cookbook_url = reference_marshaller.unmarshall(None, cookbook)
    >>> print(cookbook_url)
    http://.../cookbooks/Mastering%20the%20Art%20of%20French%20Cooking

A URL is unmarshalled to the underlying object.

    >>> cookbook = reference_marshaller.marshall_from_json_data(cookbook_url)
    >>> print(cookbook.name)
    Mastering the Art of French Cooking

    >>> reference_marshaller.marshall_from_json_data("not a url")
    Traceback (most recent call last):
    ...
    ValueError: "not a url" is not a valid URI.

    >>> reference_marshaller.marshall_from_json_data(4)
    Traceback (most recent call last):
    ...
    ValueError: got 'int', expected string: 4

    >>> print(reference_marshaller.marshall_from_json_data(None))
    None

Relative URLs
~~~~~~~~~~~~~

Relative URLs are interpreted as would be expected:

    >>> cookbook = reference_marshaller.marshall_from_json_data(
    ...     '/cookbooks/Everyday%20Greens')
    >>> print(cookbook.name)
    Everyday Greens

Redirections
~~~~~~~~~~~~

Objects may have multiple URLs, with non-canonical forms redirecting to
canonical forms.  The object marshaller accepts URLs that redirect, provided
that the redirected-to resource knows how to find the ultimate target
object.

    >>> cookbook = reference_marshaller.marshall_from_json_data(
    ...     '/cookbooks/featured')
    >>> print(cookbook.name)
    Mastering the Art of French Cooking

    >>> from lazr.restful.interfaces import IWebServiceConfiguration
    >>> webservice_configuration = getUtility(IWebServiceConfiguration)
    >>> webservice_configuration.use_https = True
    >>> cookbook = reference_marshaller.marshall_from_json_data(
    ...     '/cookbooks/featured')
    >>> print(cookbook.name)
    Mastering the Art of French Cooking
    >>> webservice_configuration.use_https = False

Collections
-----------

The most complicated kind of marshaller is one that manages a
collection of objects associated with some other object. The generic
collection marshaller will take care of marshalling to the proper
collection type, and of marshalling the individual items using the
marshaller for its value_type. Dictionaries may specify separate
marshallers for their keys and values. If no key and/or value marshallers
are specified, the default SimpleFieldMarshaller is used.

    >>> from zope.schema import Dict, List, Tuple, Set
    >>> list_of_strings_field = List(value_type=Text())
    >>> from lazr.restful.example.base.interfaces import Cuisine
    >>> tuple_of_ints_field = Tuple(value_type=Int())
    >>> list_of_choices_field = List(
    ...     value_type=Choice(vocabulary=Cuisine))
    >>> simple_list_field = List()
    >>> set_of_choices_field = Set(
    ...  value_type=Choice(vocabulary=Cuisine)).bind(None)
    >>> dict_of_choices_field = Dict(
    ...     key_type=Text(),
    ...     value_type=Choice(vocabulary=Cuisine))
    >>> simple_dict_field = Dict()

    >>> list_marshaller = getMultiAdapter(
    ...     (list_of_strings_field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, list_marshaller)
    True

    >>> simple_list_marshaller = getMultiAdapter(
    ...     (simple_list_field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, simple_list_marshaller)
    True
    >>> verifyObject(
    ...     IFieldMarshaller, simple_list_marshaller.value_marshaller)
    True

    >>> tuple_marshaller = getMultiAdapter(
    ...     (tuple_of_ints_field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, tuple_marshaller)
    True

    >>> choice_list_marshaller = getMultiAdapter(
    ...     (list_of_choices_field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, choice_list_marshaller)
    True

    >>> set_marshaller = getMultiAdapter(
    ...     (set_of_choices_field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, set_marshaller)
    True

    >>> dict_marshaller = getMultiAdapter(
    ...     (dict_of_choices_field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, dict_marshaller)
    True
    >>> verifyObject(IFieldMarshaller, dict_marshaller.key_marshaller)
    True
    >>> verifyObject(IFieldMarshaller, dict_marshaller.value_marshaller)
    True

    >>> simple_dict_marshaller = getMultiAdapter(
    ...     (simple_dict_field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, simple_dict_marshaller)
    True
    >>> verifyObject(IFieldMarshaller, simple_dict_marshaller.key_marshaller)
    True
    >>> verifyObject(
    ...     IFieldMarshaller, simple_dict_marshaller.value_marshaller)
    True

For sequences, the only JSON representation for the collection itself is a
list, since that's the only sequence type available in JSON. Anything else
will raise a ValueError.

    >>> list_marshaller.marshall_from_json_data(["Test"])
    ['Test']

    >>> list_marshaller.marshall_from_json_data("Test")
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected list: 'Test'

For dicts, we support marshalling from sequences of (name, value) pairs as
well as from dicts or even strings which are interpreted as single element
lists.

    >>> pprint_dict(
    ...     dict_marshaller.marshall_from_json_data({"foo": "Vegetarian"}))
    {'foo': <Item Cuisine.VEGETARIAN, Vegetarian>}

    >>> pprint_dict(
    ...     dict_marshaller.marshall_from_json_data([("foo", "Vegetarian")]))
    {'foo': <Item Cuisine.VEGETARIAN, Vegetarian>}

    >>> pprint_dict(dict_marshaller.marshall_from_request("foo,Vegetarian"))
    {'foo': <Item Cuisine.VEGETARIAN, Vegetarian>}

If we attempt to marshall something other than one of the above data formats,
a ValueError will be raised.

    >>> dict_marshaller.marshall_from_json_data("Test")
    Traceback (most recent call last):
      ...
    ValueError: got 'str', expected dict: 'Test'

    >>> dict_marshaller.marshall_from_request("Test")
    Traceback (most recent call last):
      ...
    ValueError: got '['Test']', list of name,value pairs

None is passed through though.

    >>> print(list_marshaller.marshall_from_json_data(None))
    None

    >>> print(dict_marshaller.marshall_from_json_data(None))
    None

ValueError is also raised if one of the value in the list doesn't
validate against the more specific marshaller.

    >>> list_marshaller.marshall_from_json_data(['Text', 1, 2])
    Traceback (most recent call last):
      ...
    ValueError: got 'int', expected str: 1

    >>> show_ValueError(choice_list_marshaller.marshall_from_request,
    ...     ['Vegetarian', 'NoSuchChoice'])
    ValueError: Invalid value "NoSuchChoice"...

ValueError is also raised if one of the keys or values in the dict doesn't
validate against the more specific marshaller.

    >>> dict_marshaller.marshall_from_json_data({1: "Vegetarian"})
    Traceback (most recent call last):
      ...
    ValueError: got 'int', expected str: 1

    >>> show_ValueError(dict_marshaller.marshall_from_request,
    ...     {'foo': 'NoSuchChoice'})
    ValueError: Invalid value "NoSuchChoice"...

The return type is correctly typed to the concrete collection.

    >>> tuple_marshaller.marshall_from_json_data([1, 2, 3])
    (1, 2, 3)
    >>> marshalled_set = set_marshaller.marshall_from_json_data(
    ...     ['Vegetarian', 'Dessert'])
    >>> print(type(marshalled_set).__name__)
    set
    >>> sorted(marshalled_set)
    [<Item Cuisine.VEGETARIAN, Vegetarian>, <Item Cuisine.DESSERT, Dessert>]

    >>> result = choice_list_marshaller.marshall_from_request(
    ...     ['Vegetarian', 'General'])
    >>> print(type(result).__name__)
    list
    >>> result
    [<Item Cuisine.VEGETARIAN, Vegetarian>, <Item Cuisine.GENERAL, General>]

    >>> marshalled_dict = dict_marshaller.marshall_from_json_data(
    ...     {'foo': 'Vegetarian', 'bar': 'General'})
    >>> print(type(marshalled_dict).__name__)
    dict
    >>> pprint_dict(marshalled_dict)
    {'bar': <Item Cuisine.GENERAL, General>,
     'foo': <Item Cuisine.VEGETARIAN, Vegetarian>}

When coming from the request, either a list or a JSON-encoded
representation is accepted. The normal request rules for the
underlying type are then followed. When marshalling dicts, the
list elements are name,value strings which are pulled apart and
used to populate the dict.

    >>> list_marshaller.marshall_from_request(['1', '2'])
    ['1', '2']
    >>> list_marshaller.marshall_from_request('["1", "2"]')
    ['1', '2']

    >>> pprint_dict(
    ...     dict_marshaller.marshall_from_request('["foo,Vegetarian"]'))
    {'foo': <Item Cuisine.VEGETARIAN, Vegetarian>}

    >>> tuple_marshaller.marshall_from_request(['1', '2'])
    (1, 2)

Except that 'null' still returns None.

    >>> print(list_marshaller.marshall_from_request('null'))
    None

    >>> print(dict_marshaller.marshall_from_request('null'))
    None

Also, as a convenience for web client, so that they don't have to JSON
encode single-element list, non-list value are promoted into a
single-element list.

    >>> tuple_marshaller.marshall_from_request('1')
    (1,)

    >>> list_marshaller.marshall_from_request('test')
    ['test']

The unmarshall() method will return a list containing the unmarshalled
representation of each its members.

    >>> sorted(set_marshaller.unmarshall(None, marshalled_set))
    ['Dessert', 'Vegetarian']

    >>> unmarshalled = dict_marshaller.unmarshall(None, marshalled_dict)
    >>> print(type(unmarshalled).__name__)
    OrderedDict
    >>> for key, value in sorted(unmarshalled.items()):
    ...     print('%s: %s' % (key, value))
    bar: General
    foo: Vegetarian

The unmarshall() method will return None when given None.

    >>> print(dict_marshaller.unmarshall(None, None))
    None

    >>> print(list_marshaller.unmarshall(None, None))
    None

    >>> print(set_marshaller.unmarshall(None, None))
    None

    >>> print(tuple_marshaller.unmarshall(None, None))
    None

CollectionField
---------------

Since CollectionField are really a list of references to other
objects, and they are exposed using a dedicated CollectionResource,
the marshaller for this kind of field is simpler.  Let's do an example
with a collection of IRecipe objects associated with some
ICookbook. (This might be the list of recipes in the cookbook, or
something like that.)

    >>> from lazr.restful.fields import CollectionField
    >>> from lazr.restful.example.base.interfaces import IRecipe
    >>> field = CollectionField(
    ...     __name__='recipes', value_type=Reference(schema=IRecipe))
    >>> marshaller = getMultiAdapter((field, request), IFieldMarshaller)
    >>> verifyObject(IFieldMarshaller, marshaller)
    True

Instead of serving the actual collection, collection marshallers serve
a URL to that collection.

    >>> marshaller.unmarshall(entry_resource, ["recipe 1", "recipe 2"])
    'http://.../cookbooks/Everyday%20Greens/recipes'

They also annotate the representation name of the field, so that
clients know this is a link to a collection-type resource.

    >>> marshaller.representation_name
    'recipes_collection_link'
