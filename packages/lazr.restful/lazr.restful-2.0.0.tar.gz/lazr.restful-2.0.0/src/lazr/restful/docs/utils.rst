Various utility functions
*************************

VersionedDict
=============

This class is a stack of named dicts that can be treated as a single
dict. When a new dict is pushed onto the stack, it's populated with
copies of values from the previous top of the stack.

A VersionedDict starts out empty and unusable. It can't be treated
as a dict because there are no real dicts in the stack.

    >>> from lazr.restful.utils import VersionedDict
    >>> stack = VersionedDict()

    >>> stack.is_empty
    True

    >>> stack.dict_names
    []

    >>> sorted(stack.items())
    Traceback (most recent call last):
    ...
    IndexError: Stack is empty

    >>> stack.pop()
    Traceback (most recent call last):
    ...
    IndexError: pop from empty list

    >>> stack['key'] = 'value'
    Traceback (most recent call last):
    ...
    IndexError: Stack is empty

    >>> stack['key']
    Traceback (most recent call last):
    ...
    KeyError: 'key'
    >>> print(stack.get('key'))
    None
    >>> print(stack.get('key', 'default'))
    default

    >>> del stack['key']
    Traceback (most recent call last):
    ...
    IndexError: Stack is empty

To use a VersionedDict you must push a named dict onto the
stack. Now it acts just like a regular dict.

    >>> stack.push('dict #1')
    >>> stack['key'] = 'value'
    >>> print(stack['key'])
    value
    >>> print(stack.get('key', 'default'))
    value

    >>> 'key' in stack
    True

    >>> sorted(stack.items())
    [('key', 'value')]

You can pop a named dict off a stack: you'll get back a named tuple
with 'version' and 'object' attributes. The 'object' is the
dictionary.

    >>> pair = stack.pop()
    >>> print(pair.version)
    dict #1
    >>> print(pair.object)
     {'key': 'value'}

    >>> stack.push('dict #1')
    >>> stack['key'] = 'value'
    >>> stack['key2'] = {'key' : 'value'}

Push a second named dict onto the stack, and things start to get
interesting. The second dict is initialized with a deep copy of the
objects in the first.

    >>> stack.push('dict #2')
    >>> print(stack['key'])
    value
    >>> print(stack['key2'])
    {'key': 'value'}

Every dict is initialized with a deep copy of the one below it.

    >>> stack['key'] = 'Second dict value'
    >>> stack.push('dict #3')
    >>> sorted(stack.items())
    [('key', 'Second dict value'), ('key2', {'key': 'value'})]

You can modify the objects in the dict at the top of the stack...

    >>> stack['key2'] = "Third dict value"
    >>> sorted(stack.items())
    [('key', 'Second dict value'), ('key2', 'Third dict value')]

...without affecting the objects in the dicts below.

    >>> ignore = stack.pop()
    >>> sorted(stack.items())
    [('key', 'Second dict value'), ('key2', {'key': 'value'})]

You can find the dict for a given name with dict_for_name():

    >>> for key, value in sorted(stack.dict_for_name('dict #1').items()):
    ...     print("%s: %s" % (key, value))
    key: value
    key2: {'key': 'value'}

You can rename a version with rename_version():

    >>> stack.rename_version('dict #2', 'Renamed dict')
    >>> stack.dict_names
    ['dict #1', 'Renamed dict']

Suppressing the copy operation
------------------------------

When you push a named dictionary onto the stack you can tell
VersionedDict not to copy in values from the next lowest dictionary
in the stack.

    >>> print(stack['key'])
    Second dict value

    >>> stack.push("An empty dictionary", empty=True)
    >>> sorted(stack.items())
    []

The dictionary that defines 'key' and 'key2' is still there...

    >>> stack.dict_names
    ['dict #1', 'Renamed dict', 'An empty dictionary']

...but 'key' and 'key2' are no longer accessible.

    >>> stack['key']
    Traceback (most recent call last):
    ...
    KeyError: 'key'

    >>> stack['key2']
    Traceback (most recent call last):
    ...
    KeyError: 'key2'

    >>> stack['key'] = 'Brand new value'
    >>> print(stack['key'])
    Brand new value

If you pop the formerly empty dictionary off the stack...

    >>> pair = stack.pop()
    >>> print(pair.version)
    An empty dictionary
    >>> print(pair.object)
    {'key': 'Brand new value'}

...'key' and 'key2' are visible again.

    >>> sorted(stack.items())
    [('key', 'Second dict value'), ('key2', {'key': 'value'})]


implement_from_dict
===================

This function takes an interface and a dictionary, and returns a class
that implements as much of the interface as possible.

    >>> from zope.schema import TextLine
    >>> from zope.interface import Interface
    >>> class ITwoFields(Interface):
    ...     field_1 = TextLine(title="field 1", default="field_1 default")
    ...     field_2 = TextLine(title="field 2")
    ...     def a_method():
    ...         pass

Values present in the dictionary become methods and attributes of the
implementing class.

    >>> from lazr.restful.utils import implement_from_dict
    >>> def result(self):
    ...     return "result"
    >>> implementation = implement_from_dict(
    ...     'TwoFields', ITwoFields,
    ...     {'field_1': 'foo', 'field_2': 'bar', 'a_method': result})

    >>> print(implementation.__name__)
    TwoFields
    >>> ITwoFields.implementedBy(implementation)
    True
    >>> print(implementation.field_1)
    foo
    >>> print(implementation.field_2)
    bar
    >>> print(implementation().a_method())
    result

If one of the interface's attributes is not defined in the dictionary,
but the interface's definition of that attribute includes a default
value, the generated class will define an attribute with the default
value.

    >>> implementation = implement_from_dict(
    ...     'TwoFields', ITwoFields, {})

    >>> print(implementation.field_1)
    field_1 default

If an attribute is not present in the dictionary and its interface
definition does not include a default value, the generated class will
not define that attribute.

    >>> implementation.field_2
    Traceback (most recent call last):
    ...
    AttributeError: type object 'TwoFields' has no attribute 'field_2'

    >>> implementation.a_method
    Traceback (most recent call last):
    ...
    AttributeError: type object 'TwoFields' has no attribute 'a_method'

The 'superclass' argument lets you specify a superclass for the
generated class.

    >>> class TwoFieldsSuperclass:
    ...     def a_method(self):
    ...         return "superclass result"

    >>> implementation = implement_from_dict(
    ...     'TwoFields', ITwoFields, {}, superclass=TwoFieldsSuperclass)

    >>> print(implementation().a_method())
    superclass result

make_identifier_safe
====================

LAZR provides a way of converting an arbitrary string into a similar
string that can be used as a Python identifier.

    >>> from lazr.restful.utils import make_identifier_safe
    >>> print(make_identifier_safe("already_a_valid_IDENTIFIER_444"))
    already_a_valid_IDENTIFIER_444

    >>> print(make_identifier_safe("!starts_with_punctuation"))
    _starts_with_punctuation

    >>> print(make_identifier_safe("_!contains!pu-nc.tuation"))
    __contains_pu_nc_tuation

    >>> print(make_identifier_safe("contains\nnewline"))
    contains_newline

    >>> print(make_identifier_safe(""))
    _

    >>> print(make_identifier_safe(None))
    Traceback (most recent call last):
    ...
    ValueError: Cannot make None value identifier-safe.

camelcase_to_underscore_separated
=================================

LAZR provides a way of converting TextThatIsWordSeparatedWithInterCaps
to text_that_is_word_separated_with_underscores.

    >>> from lazr.restful.utils import camelcase_to_underscore_separated
    >>> camelcase_to_underscore_separated('lowercase')
    'lowercase'
    >>> camelcase_to_underscore_separated('TwoWords')
    'two_words'
    >>> camelcase_to_underscore_separated('twoWords')
    'two_words'
    >>> camelcase_to_underscore_separated('ThreeLittleWords')
    'three_little_words'
    >>> camelcase_to_underscore_separated('UNCLE')
    'u_n_c_l_e'
    >>> camelcase_to_underscore_separated('_StartsWithUnderscore')
    '__starts_with_underscore'

safe_hasattr()
==============

LAZR provides a safe_hasattr() that doesn't hide exception from the
caller. This behaviour of the builtin hasattr() is annoying because it
makes problems harder to diagnose.

(The builtin hasattr() is fixed as of Python 3.2.)

    >>> import sys
    >>> import warnings
    >>> from lazr.restful.utils import safe_hasattr

    >>> class Oracle:
    ...     @property
    ...     def is_full_moon(self):
    ...         return full_moon
    >>> oracle = Oracle()
    >>> with warnings.catch_warnings(record=True):
    ...     safe_hasattr(oracle, 'is_full_moon')
    Traceback (most recent call last):
      ...
    NameError: name 'full_moon' is not defined

    >>> full_moon = True
    >>> hasattr(oracle, 'is_full_moon')
    True
    >>> with warnings.catch_warnings(record=True) as warnings_log:
    ...     safe_hasattr(oracle, 'is_full_moon')
    True
    >>> print(warnings_log[0].message)
    safe_hasattr is deprecated; use the hasattr builtin instead.

    >>> hasattr(oracle, 'weather')
    False
    >>> with warnings.catch_warnings(record=True) as warnings_log:
    ...     safe_hasattr(oracle, 'weather')
    False
    >>> print(warnings_log[0].message)
    safe_hasattr is deprecated; use the hasattr builtin instead.

smartquote()
============

smartquote() converts pairs of inch marks (") in a string to typographical
quotation marks.

    >>> from lazr.restful.utils import smartquote
    >>> print(smartquote(''))
    >>> print(smartquote('foo "bar" baz'))
    foo “bar” baz
    >>> print(smartquote('foo "bar baz'))
    foo “bar baz
    >>> print(smartquote('foo bar" baz'))
    foo bar” baz
    >>> print(smartquote('""foo " bar "" baz""'))
    ""foo " bar "" baz""
    >>> print(smartquote('" foo "'))
    " foo "
    >>> print(smartquote('"foo".'))
    “foo”.
    >>> print(smartquote('a lot of "foo"?'))
    a lot of “foo”?
