Web Service API Declarations
****************************

You can easily create a web service by tagging your content interfaces
with some decorators. From this tagging the web service API will be
created automatically.

Exporting the data model
========================

The LAZR Web Service data model consists of entries and collection (see
webservice.txt for all the details). Entries support the IEntry
interface and are basically a single resource exported. Think something
like a bug, a person, an article, etc. Collections are a set of
resources of the same types, think something like the set of bugs,
persons, teams, articles, etc.

Exporting entries
=================

Only entries are exported as data. You can mark that one of your content
interface is exported on the web service as an entry, by using the
exported_as_webservice_entry() declaration.

You can mark the fields that should be part of the entry data model by
using the exported() wrapper. It takes an optional 'exported_as' parameter
that can be used to change the name under which the field will be
exported.

For example, here we declare that the IBook interface is exported as an
entry on the  web service. It exports the title, author, and base_price
field, but not the inventory_number field.

    >>> from zope.interface import Interface
    >>> from zope.schema import Text, TextLine, Float, List
    >>> from lazr.restful.declarations import (
    ...     exported,
    ...     exported_as_webservice_entry,
    ...     )
    >>> @exported_as_webservice_entry()
    ... class IBook(Interface):
    ...     """A simple book data model."""
    ...
    ...     title = exported(TextLine(title='The book title'))
    ...
    ...     author = exported(TextLine(title="The book's author."))
    ...
    ...     base_price = exported(Float(
    ...         title="The regular price of the book."),
    ...         exported_as='price')
    ...
    ...     inventory_number = TextLine(title='The inventory part number.')

These declarations add tagged values to the original interface elements.
The tags are in the lazr.restful namespace and are dictionaries of
elements.

    >>> from collections.abc import Mapping
    >>> from pprint import pformat
    >>> def print_export_tag(element):
    ...     """Print the content of the 'lazr.restful.exported' tag."""
    ...     def format_value(value):
    ...         if isinstance(value, Mapping):
    ...             return pformat(dict(value), width=40)
    ...         else:
    ...             return repr(value)
    ...     tag = element.queryTaggedValue('lazr.restful.exported')
    ...     if tag is None:
    ...         print("tag 'lazr.restful.exported' is not present")
    ...     else:
    ...         print("\n".join(
    ...             "%s: %s" %(key, format_value(value))
    ...             for key, value in sorted(tag.items())))
    >>> print_export_tag(IBook)
    _as_of_was_used: False
    contributes_to: None
    exported: True
    plural_name: 'books'
    publish_web_link: True
    singular_name: 'book'
    type: 'entry'
    >>> print_export_tag(IBook['title'])
    as: 'title'
    original_name: 'title'
    type: 'field'
    >>> print_export_tag(IBook['author'])
    as: 'author'
    original_name: 'author'
    type: 'field'
    >>> print_export_tag(IBook['base_price'])
    as: 'price'
    original_name: 'base_price'
    type: 'field'
    >>> print_export_tag(IBook['inventory_number'])
    tag 'lazr.restful.exported' is not present

Only IField can be exported as entry fields.

    >>> from zope.interface import Attribute
    >>> @exported_as_webservice_entry()
    ... class Foo(Interface):
    ...     not_a_field = exported(Attribute('A standard attribute'))
    Traceback (most recent call last):
      ...
    TypeError: exported() can only be used on IFields.

Object fields cannot be exported because they cause validation problems.

    >>> from zope.schema import Object
    >>> @exported_as_webservice_entry()
    ... class UsesIObject(Interface):
    ...     object = exported(Object(schema=Interface))
    Traceback (most recent call last):
    TypeError: Object exported; use Reference instead.

Instead you should use Reference, a subclass of Object designed to
avoid the validation problems.

    >>> from lazr.restful.fields import Reference
    >>> @exported_as_webservice_entry()
    ... class UsesIReference(Interface):
    ...     object = exported(Reference(schema=Interface))

In the same vein, exported_as_webservice_entry() can only be used on
Interface.

    >>> @exported_as_webservice_entry()
    ... class NotAnInterface:
    ...     pass
    Traceback (most recent call last):
      ...
    TypeError: exported_as_webservice_entry() can only be used on an
    interface.

publish_web_link
----------------

If each webservice entry corresponds to some page on a website,
lazr.restful will publish a web_link for each entry, pointing to the
corresponding website page. For a given entry type, you can suppress
this by passing in False for the `publish_web_link` argument to
`exported_as_webservice_entry`.

    >>> from zope.interface import Attribute
    >>> @exported_as_webservice_entry(publish_web_link=False)
    ... class INotOnTheWebsite(Interface):
    ...     field = exported(TextLine(title="A field."))
    >>> print_export_tag(INotOnTheWebsite)
    _as_of_was_used: False
    contributes_to: None
    ...
    publish_web_link: False
    ...

Exporting a collection
======================

Collections scoped to an entry are exported simply by using
exported() on the CollectionField containing the scoped collection
items:

    >>> class ISimpleComment(Interface):
    ...     """A simple comment."""
    ...     comment = TextLine(title='Comment')

    >>> from zope.schema import Object
    >>> from lazr.restful.fields import CollectionField
    >>> @exported_as_webservice_entry()
    ... class IBookWithComments(IBook):
    ...     """A book with some comments."""
    ...
    ...     comments = exported(CollectionField(
    ...         value_type=Object(schema=ISimpleComment)))

Top-level collections are different though, they are exported by using the
exported_as_webservice_collection() in the ``Set`` class. The method that
returns all of the collection items must be tagged with
@collection_default_content decorator.

    >>> from lazr.restful.declarations import (
    ...     exported_as_webservice_collection, collection_default_content,
    ...     REQUEST_USER)
    >>> @exported_as_webservice_collection(IBook)
    ... class IBookSet(Interface):
    ...     """Set of all the books in the system."""
    ...
    ...     @collection_default_content()
    ...     def getAllBooks():
    ...         """Return an iterator over all the books."""

In case the method to call requires parameters, the value to use can be
specified using parameters to the decorator constructor. There is a
special REQUEST_USER marker that can be used to specify that this
parameter should contain the logged in user.

    >>> @exported_as_webservice_collection(IBook)
    ... class ICheckedOutBookSet(Interface):
    ...     """Give access to the checked out books."""
    ...
    ...     @collection_default_content(user=REQUEST_USER, title='')
    ...     def getByTitle(title, user):
    ...         """Return checked out books.
    ...         :param title: String to match against the book title.
    ...             The empty string matches everything.
    ...         :param user: The user who should have checked the book out.
    ...         """

Like for entries, this adds keys in the 'lazr.restful.exported'
tagged value.

    >>> print_export_tag(IBookSet)
    collection_default_content: {None: ('getAllBooks', {})}
    collection_entry_schema: <InterfaceClass __builtin__.IBook>
    type: 'collection'

    >>> print_export_tag(ICheckedOutBookSet)
    collection_default_content: {None: ('getByTitle',
            {'title': '',
             'user': <class '...REQUEST_USER'>})}
    collection_entry_schema: <InterfaceClass __builtin__.IBook>
    type: 'collection'

The entry schema for a collection must be provided and must be an
interface:

    >>> @exported_as_webservice_collection()
    ... class MissingEntrySchema(Interface):
    ...     pass
    Traceback (most recent call last):
      ...
    TypeError: ...

    >>> @exported_as_webservice_collection("not an interface")
    ... class InvalidEntrySchema(Interface):
    ...     pass
    Traceback (most recent call last):
      ...
    TypeError: entry_schema must be an interface.

It's an error to try to export a collection without marking a method as
exporting the default content.

    >>> class ISampleInterface(Interface):
    ...     pass

    >>> @exported_as_webservice_collection(ISampleInterface)
    ... class MissingDefaultContent(Interface):
    ...     pass
    Traceback (most recent call last):
      ...
    TypeError: exported_as_webservice_collection() is missing a method
    tagged with @collection_default_content.

As it is an error, to mark more than one method:

    >>> @exported_as_webservice_collection(ISampleInterface)
    ... class TwoDefaultContent(Interface):
    ...     @collection_default_content()
    ...     def getAll1():
    ...         """A first getAll()."""
    ...     @collection_default_content()
    ...     def getAll2():
    ...         """Another getAll()."""
    Traceback (most recent call last):
      ...
    TypeError: Only one method can be marked with
    @collection_default_content for version '(earliest version)'.

exported_as_webservice_collection() can only be used on Interface.

    >>> @exported_as_webservice_collection(ISampleInterface)
    ... class NotAnInterface:
    ...     pass
    Traceback (most recent call last):
      ...
    TypeError: exported_as_webservice_collection() can only be used on an
    interface.

collection_default_content() can only be used from within an Interface
declaration:

    >>> @collection_default_content()
    ... def a_function(): pass
    Traceback (most recent call last):
      ...
    TypeError: @collection_default_content can only be used from within
    an interface definition.

Exporting methods
=================

Entries and collections can publish named operations on the
webservice. Every named operation corresponds to some method defined
on the content interface. To publish a method as a named operation,
you tag it with special decorators.

Four different decorators are used based on the kind of method
exported.

1. @export_read_operation

    This will mark the method as available as a GET operation on the
    exported resource.

2. @export_write_operation

    This will mark the method as available as a POST operation on the
    exported resource.

3. @export_factory_operation(schema, fields)

    Like the @export_write_operation decorator, this will mark the
    method as available as a POST operation on the exported resource,
    with the addition that the result of the method is a new object and
    the HTTP status code will be set appropriately.

    This decorator takes as parameters the schema of the object it is
    creating and the name of the fields in the schema that are passed as
    parameters.

4. @export_destructor_operation

    This will mark the method as available as a DELETE operation on the
    exported resource.

The specification of the web service's acceptable method parameters
should be described using the @operation_parameters decorator, which
takes normal IField instances.

When an operation returns an object that's exposed as a resource, you
should describe its return value with the
@operation_returns_collection_of and @operation_returns_entry
decorators. Both decorators take an interface that has been exposed as
an entry. @operation_returns_entry is used when the operation returns
a single entry; @operation_returns_collection_of is used when the
operation returns a collection of entries.

    >>> from lazr.restful.declarations import (
    ...     export_operation_as, export_factory_operation,
    ...     export_read_operation, operation_parameters,
    ...     operation_returns_entry, operation_returns_collection_of,
    ...     rename_parameters_as)
    >>> from lazr.restful.interface import copy_field
    >>> @exported_as_webservice_collection(IBook)
    ... class IBookSetOnSteroids(IBookSet):
    ...     """IBookSet supporting some methods."""
    ...
    ...     @collection_default_content()
    ...     @operation_parameters(
    ...         text=copy_field(IBook['title'], title='Text to search for.'))
    ...     @operation_returns_collection_of(IBook)
    ...     @export_read_operation()
    ...     def searchBookTitles(text):
    ...         """Return list of books whose titles contain 'text'."""
    ...
    ...     @operation_parameters(
    ...         text=copy_field(IBook['title'], title='Text to search for.'))
    ...     @operation_returns_entry(IBook)
    ...     @export_read_operation()
    ...     def bestMatch(text):
    ...         """Return the best match for books containing 'text'."""
    ...
    ...     @export_operation_as('create_book')
    ...     @rename_parameters_as(base_price='price')
    ...     @export_factory_operation(
    ...         IBook, ['author', 'base_price', 'title'])
    ...     def new(author, base_price, title):
    ...         """Create a new book."""

In the above example, the exported new() method demonstrates two
features to support having different names on the web service than in
the internal API.  It is possible to export a method under a different
name by using the @export_operation_as decorator which takes the name
under which the method should be exported.

The @rename_parameters_as decorator can be used to rename the method
parameters on the web service.  In the example, the 'base_price' parameter
will be called 'price' when exported on the web service.

When some required parameters of the method should not be provided by
the webservice client, it is possible to use the @call_with decorator to
specify the value to use. The special REQUEST_USER marker can be used to
specify that this parameter should contain the logged in user.

    >>> from lazr.restful.declarations import (
    ...     call_with, export_destructor_operation, export_write_operation,
    ...     REQUEST_USER)
    >>> @exported_as_webservice_entry()
    ... class IBookOnSteroids(IBook):
    ...     """IBook with some methods."""
    ...
    ...     @call_with(who=REQUEST_USER, kind='normal')
    ...     @export_write_operation()
    ...     def checkout(who, kind):
    ...         """Check this book out."""
    ...
    ...     @export_destructor_operation()
    ...     def destroy():
    ...         """Destroy the book."""

Like other declarations, these will add tagged values to the interface
method. We didn't have to specify the return type for the factory
operation, because a factory operation always returns the
newly-created object.

    >>> print_export_tag(IBookSetOnSteroids['new'])
    as: 'create_book'
    call_with: {}
    creates: <...IBook...>
    params: {'author': <...TextLine...>,
        'base_price': <...Float...>,
        'title': <...TextLine...>}
    return_type: <lazr.restful._operation.ObjectLink object...>
    type: 'factory'

We did specify the return type for the 'searchBookTitles' method: it
returns a collection.

    >>> print_export_tag(IBookSetOnSteroids['searchBookTitles'])
    as: 'searchBookTitles'
    call_with: {}
    params: {'text': <...TextLine...>}
    return_type: <lazr.restful.fields.CollectionField object...>
    type: 'read_operation'

The 'bestMatch' method returns an entry.

    >>> print_export_tag(IBookSetOnSteroids['bestMatch'])
    as: 'bestMatch'
    call_with: {}
    params: {'text': <...TextLine...>}
    return_type: <lazr.restful.fields.Reference object...>
    type: 'read_operation'

The 'checkout' method doesn't return anything.

    >>> print_export_tag(IBookOnSteroids['checkout'])
    as: 'checkout'
    call_with: {'kind': 'normal', 'who': <class '...REQUEST_USER'>}
    params: {}
    return_type: None
    type: 'write_operation'

Parameters that are not renamed are exported under the same name:

    >>> for name, param in sorted(IBookSetOnSteroids['new'].getTaggedValue(
    ...     'lazr.restful.exported')['params'].items()):
    ...     print("%s: %s" % (name, param.__name__))
    author: author
    base_price: price
    title: title

It is possible to use @operation_parameters with
@export_factory_operation to specify parameters that are not part of the
schema.

    >>> @exported_as_webservice_entry()
    ... class ComplexBookFactory(Interface):
    ...     @operation_parameters(collection=TextLine())
    ...     @export_factory_operation(IBook, ['author', 'title'])
    ...     def create_book(author, title, collection):
    ...         """Create a book in a collection."""

    >>> print_export_tag(ComplexBookFactory['create_book'])
    as: 'create_book'
    call_with: {}
    creates: <...IBook...>
    params: {'author': <...TextLine...>,
        'collection': <...TextLine...>,
        'title': <...TextLine...>}
    return_type: <lazr.restful._operation.ObjectLink object...>
    type: 'factory'

Default values and required parameters
--------------------------------------

Parameters default and required attributes are set automatically based
on the method signature.

    >>> @exported_as_webservice_entry()
    ... class ComplexParameterDefinition(Interface):
    ...     @operation_parameters(
    ...         required1=TextLine(),
    ...         required2=TextLine(default='Not required'),
    ...         optional1=TextLine(required=True),
    ...         optional2=TextLine(),
    ...         )
    ...     @export_read_operation()
    ...     def a_method(required1, required2, optional1='Default',
    ...                  optional2='Default2'):
    ...         """Method demonstrating how required/default are set."""

In this example, the required1 definition will be automatically
considered required.

    >>> param_defs = ComplexParameterDefinition['a_method'].getTaggedValue(
    ...     'lazr.restful.exported')['params']
    >>> param_defs['required1'].required
    True

But required2 will not be considered required because a default value
was provided.

    >>> param_defs['required2'].required
    False

NOTE: It's not possible to make an optional parameter required on the
webservice. In the above case, required=True was specified on
"optional1", but that will be overridden. The reason for that is that by
default required is always True, so it's not possible to distinguish
between the case where required was set to True, and required is True
because it's the default value.

    >>> param_defs['optional1'].required
    False
    >>> print(param_defs['optional1'].default)
    Default

And optional2 was exported with the same default than the method:

    >>> param_defs['optional2'].required
    False
    >>> print(param_defs['optional2'].default)
    Default2

Error handling
--------------

All these decorators can only be used from within an interface
definition:

    >>> @export_operation_as('test')
    ... def a_method1(self): pass
    Traceback (most recent call last):
      ...
    TypeError: export_operation_as() can only be used from within an interface
    definition.

    >>> @export_read_operation()
    ... def another_method(self): pass
    Traceback (most recent call last):
      ...
    TypeError: export_read_operation() can only be used from within an
    interface definition.

An error is also reported if not enough parameters are defined as
exported:

    >>> @exported_as_webservice_entry()
    ... class MissingParameter(Interface):
    ...     @call_with(param1=1)
    ...     @operation_parameters(
    ...         param2=TextLine())
    ...     @export_read_operation()
    ...     def a_method(param1, param2, param3, param4): pass
    Traceback (most recent call last):
      ...
    TypeError: method "a_method" is missing definitions for parameter(s)
    exported in version "(earliest version)": param3, param4

Defining a parameter not available on the method also results in an
error:

    >>> @exported_as_webservice_entry()
    ... class BadParameter(Interface):
    ...     @operation_parameters(
    ...         no_such_param=TextLine())
    ...     @export_read_operation()
    ...     def a_method(): pass
    Traceback (most recent call last):
      ...
    TypeError: method "a_method" doesn't have the following exported parameters
    in version "(earliest version)": no_such_param.

But that's not a problem if the exported method actually takes arbitrary
keyword parameters:

    >>> @exported_as_webservice_entry()
    ... class AnyParameter(Interface):
    ...     @operation_parameters(
    ...         param1=TextLine())
    ...     @export_read_operation()
    ...     def a_method(**kwargs): pass

When using @export_factory_operation, TypeError will also be raised if
one of the field doesn't exists in the schema:

    >>> @exported_as_webservice_entry()
    ... class MissingParameter(Interface):
    ...     @export_factory_operation(IBook, ['no_such_field'])
    ...     def a_method(): pass
    Traceback (most recent call last):
      ...
    TypeError: IBook doesn't define 'no_such_field'.

Or if the field name doesn't represent a field:

    >>> @exported_as_webservice_entry()
    ... class NotAField(Interface):
    ...     @export_factory_operation(IBookOnSteroids, ['checkout'])
    ...     def a_method(): pass
    Traceback (most recent call last):
      ...
    TypeError: IBookOnSteroids.checkout doesn't provide IField.

Or if @operation_parameters redefine a field specified in the factory:

    >>> @exported_as_webservice_entry()
    ... class Redefinition(Interface):
    ...     @operation_parameters(title=TextLine())
    ...     @export_factory_operation(IBookOnSteroids, ['title'])
    ...     def create_book(title): pass
    Traceback (most recent call last):
      ...
    TypeError: 'title' parameter is already defined.

All parameters definitions must be schema fields:

    >>> @exported_as_webservice_entry()
    ... class BadParameterDefinition(Interface):
    ...     @operation_parameters(a_param=object())
    ...     @export_read_operation()
    ...     def a_method(): pass
    Traceback (most recent call last):
      ...
    TypeError: export definition of "a_param" in method "a_method" must
    provide IField: <object...>

Renaming a parameter that wasn't defined results in an error:

    >>> class NonExistentParameter(Interface):
    ...     @rename_parameters_as(param1='name', param2='name2')
    ...     @operation_parameters(param1=TextLine())
    ...     @export_read_operation()
    ...     def a_method(param1): pass
    Traceback (most recent call last):
      ...
    TypeError: rename_parameters_as(): no "param2" parameter is exported.

Trying to use @rename_parameters_as without exporting the method also
results in an error.

    >>> class MissingMethodExport(Interface):
    ...     @rename_parameters_as(a_param='name')
    ...     def a_method(): pass
    Traceback (most recent call last):
      ...
    TypeError: "a_method" isn't exported on the webservice.

The decorators @operation_returns_entry and
@operation_returns_collection_of will only accept an IInterface as
argument.

    >>> @exported_as_webservice_entry()
    ... class ReturnOtherThanInterface(Interface):
    ...     @operation_returns_entry("not-an-interface")
    ...     @export_read_operation()
    ...     def a_method(**kwargs): pass
    Traceback (most recent call last):
    ...
    TypeError: Entry type not-an-interface does not provide IInterface.

    >>> @exported_as_webservice_entry()
    ... class ReturnOtherThanInterface(Interface):
    ...     @operation_returns_collection_of("not-an-interface")
    ...     @export_read_operation()
    ...     def a_method(**kwargs): pass
    Traceback (most recent call last):
    ...
    TypeError: Collection value type not-an-interface does not
    provide IInterface.

Exporting exceptions
====================

When a method raises an exception, the default is to report the error as
'500 Internal Server Error'. In many cases, that's not the case and one
of the 4XX error would be better. You can use error_status to annotate an
exception with a suitable HTTP status.

    >>> from lazr.restful.declarations import error_status
    >>> @error_status(400)
    ... class InvalidDemo(Exception):
    ...     """An example exception"""

The function sets the __lazr_webservice_error__ attribute on the
exception, which will be used by the view handling the exception.

    >>> InvalidDemo.__lazr_webservice_error__
    400

The function raises an exception if it is used for something that already has
a conflicting __lazr_webservice_error__ attribute.

    >>> ignore = error_status(400)(InvalidDemo) # OK
    >>> InvalidDemo.__lazr_webservice_error__
    400
    >>> error_status(401)(InvalidDemo) # Not OK
    Traceback (most recent call last):
    ...
    ValueError: ('Exception already has an error status', 400)

It also raises an exception if it is used on something that is not an
Exception.

    >>> error_status(400)(object)
    Traceback (most recent call last):
    ...
    TypeError: Annotated value must be an exception class.

Exceptions can be also be tagged internally to the class definition with the
webservice_error() declaration to state the proper HTTP status code to use for
that kind of error.

    >>> from lazr.restful.declarations import webservice_error
    >>> class InvalidEmail(Exception):
    ...     """Error happening when the email is not valid."""
    ...     webservice_error(400)

As with error_status, the directive sets the __lazr_webservice_error__
attribute on the exception, which will be used by the view handling the
exception.

    >>> InvalidEmail.__lazr_webservice_error__
    400

Using that directive outside of a class declaration is an error:

    >>> webservice_error(402)
    Traceback (most recent call last):
      ...
    TypeError: webservice_error() can only be used from within an
    exception definition.

Export and inheritance
======================

A child interface inherits the markup of its ancestors, even when the
base interface isn't exported itself.

    >>> class IHasName(Interface):
    ...     name = exported(TextLine())
    ...
    ...     @operation_parameters(new_name=TextLine())
    ...     @export_write_operation()
    ...     def rename(new_name):
    ...         """Rename the object."""

    >>> @exported_as_webservice_entry()
    ... class IUser(IHasName):
    ...     nickname = exported(TextLine())
    ...
    ...     @operation_parameters(to=Object(IHasName), msg=TextLine())
    ...     @export_write_operation()
    ...     def talk_to(to, msg):
    ...         """Sends a message to another named object."""

    >>> for name in sorted(IUser.names(True)):
    ...     print('== %s ==' % name)
    ...     print_export_tag(IUser[name])
    == name ==
    as: 'name'
    original_name: 'name'
    type: 'field'
    == nickname ==
    as: 'nickname'
    original_name: 'nickname'
    type: 'field'
    == rename ==
    as: 'rename'
    call_with: {}
    params: {'new_name': <...TextLine...>}
    return_type: None
    type: 'write_operation'
    == talk_to ==
    as: 'talk_to'
    call_with: {}
    params: {'msg': <...TextLine...>,
        'to': <...Object...>}
    return_type: None
    type: 'write_operation'


Contributing interfaces
=======================

It is possible to mix multiple interfaces into a single exported entry. This
is specially useful when you want to export fields/methods that belong to
adapters for your entry's class instead of to the class itself. For example,
we can have an IDeveloper interface contributing to IUser.

    >>> @exported_as_webservice_entry(contributes_to=[IUser])
    ... class IDeveloper(Interface):
    ...     programming_languages = exported(List(
    ...         title='Programming Languages spoken by this developer'))

This will cause all the fields/methods of IDeveloper to be exported as part of
the IBook entry instead of exporting a new entry for IDeveloper. For this to
work you just need to ensure an object of the exported entry type can be
adapted into the contributing interface (e.g. an IUser object can be adapted
into IDeveloper).

    >>> print_export_tag(IDeveloper)
    _as_of_was_used: False
    contributes_to: [<InterfaceClass __builtin__.IUser>]
    exported: True
    plural_name: 'developers'
    publish_web_link: True
    singular_name: 'developer'
    type: 'entry'

To learn how this works, see ContributingInterfacesTestCase in
tests/test_declarations.py.


Generating the webservice
=========================

Setup
-----

Before we can continue, we must define a web service configuration
object. Each web service needs to have one of these registered
utilities providing basic information about the web service. This one
is just a sample.

    >>> from zope.component import provideUtility
    >>> from zope.security.interfaces import Unauthorized
    >>> from lazr.restful.interfaces import IWebServiceConfiguration
    >>> from lazr.restful.testing.helpers import TestWebServiceConfiguration
    >>> class MyWebServiceConfiguration(TestWebServiceConfiguration):
    ...     active_versions = ["beta", "1.0", "2.0", "3.0"]
    ...     last_version_with_mutator_named_operations = "1.0"
    ...     first_version_with_total_size_link = "2.0"
    ...     code_revision = "1.0b"
    ...     default_batch_size = 50
    ...     _scopes = None
    ...
    ...     def checkRequest(self, obj, required_scopes):
    ...         if self._scopes is not None:
    ...             if not required_scopes:
    ...                 raise Unauthorized(
    ...                     'Current authentication only allows calling '
    ...                     'scoped methods.')
    ...             elif not any(
    ...                     scope in required_scopes
    ...                     for scope in self._scopes):
    ...                 raise Unauthorized(
    ...                     'Current authentication does not allow calling '
    ...                     'this method (one of these scopes is required: '
    ...                     '%s).' % ', '.join(
    ...                         "'%s'" % scope for scope in required_scopes))
    >>> provideUtility(MyWebServiceConfiguration(), IWebServiceConfiguration)

We must also set up the ability to create versioned requests. This web
service has four versions: 'beta', '1.0', '2.0', and '3.0'.  We'll
need a marker interface for every version, registered as a utility
under the name of the version.

Each version interface subclasses the previous version's
interface. This lets a request use a resource definition for the
previous version if it hasn't changed since then.

    >>> from zope.component import getSiteManager
    >>> from lazr.restful.interfaces import IWebServiceVersion
    >>> class ITestServiceRequestBeta(IWebServiceVersion):
    ...     pass
    >>> class ITestServiceRequest10(ITestServiceRequestBeta):
    ...     pass
    >>> class ITestServiceRequest20(ITestServiceRequest10):
    ...     pass
    >>> class ITestServiceRequest30(ITestServiceRequest20):
    ...     pass
    >>> sm = getSiteManager()
    >>> for marker, name in [(ITestServiceRequestBeta, 'beta'),
    ...                      (ITestServiceRequest10, '1.0'),
    ...                      (ITestServiceRequest20, '2.0'),
    ...                      (ITestServiceRequest30, '3.0')]:
    ...     sm.registerUtility(marker, IWebServiceVersion, name=name)

    >>> from lazr.restful.testing.webservice import FakeRequest
    >>> request = FakeRequest(version='beta')


Entry
-----

The webservice can be generated from tagged interfaces.  For every
version in the web service, generate_entry_interfaces() will create a
subinterface of IEntry containing a copy of those IField definitions
from the original interface that were tagged for export.

    >>> from lazr.restful.declarations import generate_entry_interfaces
    >>> [[version, entry_interface]] = generate_entry_interfaces(
    ...     IBook, [], 'beta')

The created interface is named with 'Entry' appended to the original
name, and is in the same module

    >>> import sys
    >>> entry_interface.__module__
    'builtins'
    >>> entry_interface.__name__
    'IBookEntry_beta'

The original interface docstring is copied over to the new interface:

    >>> entry_interface.__doc__
    'A simple book data model.'

It extends IEntry.

    >>> from lazr.restful.interfaces import IEntry
    >>> entry_interface.extends(IEntry)
    True

All fields tagged were copied to the new interface:

    >>> def dump_entry_interface(entry_interface):
    ...     for name, field in sorted(
    ...         entry_interface.namesAndDescriptions()):
    ...         print("%s: %s" % (name, field.__class__.__name__))
    >>> dump_entry_interface(entry_interface)
    author: TextLine
    price: Float
    title: TextLine

The field __name__ attribute contains the exported name:

    >>> print(entry_interface['price'].__name__)
    price

Associated with the interface through tags are automatically-generated
'singular' and 'plural' names for the interface.

    >>> from lazr.restful.interfaces import LAZR_WEBSERVICE_NAME
    >>> tags = entry_interface.queryTaggedValue(LAZR_WEBSERVICE_NAME)
    >>> print(tags['singular'])
    book
    >>> print(tags['plural'])
    books

It's an error to use generate_entry_interfaces() on an interface that
wasn't marked for export:

    >>> class SimpleNotExported(Interface):
    ...     """Interface not exported."""
    >>> generate_entry_interfaces(SimpleNotExported, [], 'beta')
    Traceback (most recent call last):
      ...
    TypeError: 'SimpleNotExported' isn't tagged for webservice export.

The interface must also be exported as an entry:

    >>> generate_entry_interfaces(IBookSet, [], 'beta')
    Traceback (most recent call last):
      ...
    TypeError: 'IBookSet' isn't exported as an entry.

The adapter can be generated using the generate_entry_adapters()
function, which takes the tagged content interface and the IEntry
subinterface as parameters.

    >>> from lazr.restful.declarations import generate_entry_adapters
    >>> entry_adapter_factories = generate_entry_adapters(
    ...     IBook, [], [('beta', entry_interface)])

generate_entry_adapters() generates an adapter for every version of
the web service (see a test for it below, in "Versioned
Services"). This web service only has one version, so there's only one
adapter.

    >>> [factory] = entry_adapter_factories
    >>> print(factory.version)
    beta
    >>> entry_adapter_factory = factory.object

The generated adapter provides the webservice interface:

    >>> entry_interface.implementedBy(entry_adapter_factory)
    True

The resulting class is named based on the interface:

    >>> print(entry_adapter_factory.__name__)
    BookEntry_betaAdapter

Its docstring is also copied over from the original interface:

    >>> entry_adapter_factory.__doc__
    'A simple book data model.'

The resulting adapter has its schema attribute set to the exported
interface, and proxies all attributes to the underlying object.

    >>> from zope.interface.verify import verifyObject
    >>> from zope.interface import implementer
    >>> @implementer(IBook)
    ... class Book:
    ...     """Simple IBook implementation."""
    ...     def __init__(self, author, title, base_price,
    ...                  inventory_number):
    ...         self.author = author
    ...         self.title = title
    ...         self.base_price = base_price
    ...         self.inventory_number = inventory_number

Now we can turn a Book object into something that implements
IBookEntry.

    >>> entry_adapter = entry_adapter_factory(
    ...     Book('Aldous Huxley', 'Island', 10.0, '12345'),
    ...     request)

    >>> entry_adapter.schema is entry_interface
    True
    >>> verifyObject(entry_interface, entry_adapter)
    True
    >>> print(entry_adapter.author)
    Aldous Huxley
    >>> entry_adapter.price
    10.0
    >>> print(entry_adapter.title)
    Island

It's an error to call this function on an interface not exported on the
web service:

    >>> generate_entry_adapters(
    ...     SimpleNotExported, [], ('beta', entry_interface))
    Traceback (most recent call last):
      ...
    TypeError: 'SimpleNotExported' isn't tagged for webservice export.

Or exported as a collection:

    >>> generate_entry_adapters(IBookSet, [], ('beta', entry_interface))
    Traceback (most recent call last):
      ...
    TypeError: 'IBookSet' isn't exported as an entry.


Collection
----------

An ICollection adapter for content interface tagged as being exported as
collections on the webservice can be generated by using the
generate_collection_adapter() function.

    >>> from lazr.restful.interfaces import ICollection
    >>> from lazr.restful.declarations import (
    ...     generate_collection_adapter)

    >>> collection_adapter_factory = generate_collection_adapter(IBookSet)
    >>> ICollection.implementedBy(collection_adapter_factory)
    True

The find() method will return the result of calling the method tagged
with the @collection_default_content decorator.

    >>> @implementer(IBookSet)
    ... class BookSet:
    ...     """Simple IBookSet implementation."""
    ...
    ...     def __init__(self, books=()):
    ...         self.books = books
    ...
    ...     def getAllBooks(self):
    ...         return self.books

    >>> collection_adapter = collection_adapter_factory(
    ...     BookSet(['A book', 'Another book']), request)

    >>> verifyObject(ICollection, collection_adapter)
    True

    >>> collection_adapter.find()
    ['A book', 'Another book']

The adapter's docstring is taken from the original interface.

    >>> collection_adapter.__doc__
    'Set of all the books in the system.'

If parameters were specified, they'll be passed in to the method by
find(). The REQUEST_USER marker value will be replaced by the logged in
user.

    >>> @implementer(ICheckedOutBookSet)
    ... class CheckedOutBookSet:
    ...     """Simple ICheckedOutBookSet implementation."""
    ...
    ...     def getByTitle(self, title, user):
    ...         print('%s searched for checked out book matching "%s".' % (
    ...             user, title))

    >>> checked_out_adapter = generate_collection_adapter(
    ...     ICheckedOutBookSet)(CheckedOutBookSet(), request)

    >>> checked_out_adapter.find()
    A user searched for checked out book matching "".

It's an error to call this function on an interface not exported on the
web service:

    >>> generate_collection_adapter(SimpleNotExported)
    Traceback (most recent call last):
      ...
    TypeError: 'SimpleNotExported' isn't tagged for webservice export.

Or exported as an entry.

    >>> generate_collection_adapter(IBook)
    Traceback (most recent call last):
      ...
    TypeError: 'IBook' isn't exported as a collection.

Methods
-------

IResourceOperation adapters can be generated for exported methods by
using the generate_operation_adapter() function. Using it on a method
exported as a read operation will generate an IResourceGETOperation.

    >>> from lazr.restful.interfaces import IResourceGETOperation
    >>> from lazr.restful.declarations import (
    ...     generate_operation_adapter)

    >>> read_method_adapter_factory = generate_operation_adapter(
    ...     IBookSetOnSteroids['searchBookTitles'])
    >>> IResourceGETOperation.implementedBy(read_method_adapter_factory)
    True

The defined adapter is named GET_<interface>_<exported_name>_beta
and uses the ResourceOperation base class. The "_beta" indicates
that the adapter will be used in the earliest version of the web
service, and any subsequent versions, until a newer implementation
supercedes it.

    >>> from lazr.restful import ResourceOperation
    >>> read_method_adapter_factory.__name__
    'GET_IBookSetOnSteroids_searchBookTitles_beta'
    >>> issubclass(read_method_adapter_factory, ResourceOperation)
    True

The adapter's docstring is taken from the decorated method docstring.

    >>> read_method_adapter_factory.__doc__
    "Return list of books whose titles contain 'text'."

The adapter's params attribute contains the specification of the
parameters accepted by the operation.

    >>> from operator import attrgetter
    >>> def print_params(params):
    ...     """Print the name and type of the defined parameters."""
    ...     for param in sorted(params, key=attrgetter('__name__')):
    ...         print("%s: %s" % (param.__name__, param.__class__.__name__))
    >>> print_params(read_method_adapter_factory.params)
    text: TextLine

The call() method calls the underlying method and returns its result.

    >>> @implementer(IBookSetOnSteroids)
    ... class BookSetOnSteroids(BookSet):
    ...
    ...     result = None
    ...
    ...     def searchBookTitles(self, text):
    ...         return self.result
    ...
    ...     def new(self, author, base_price, title):
    ...         return Book(author, title, base_price, "unknown")

Now we can create a fake request that invokes the named operation.

    >>> request = FakeRequest(version='beta')
    >>> read_method_adapter = read_method_adapter_factory(
    ...     BookSetOnSteroids(), request)
    >>> verifyObject(IResourceGETOperation, read_method_adapter)
    True
    >>> read_method_adapter.send_modification_event
    False

    >>> read_method_adapter.context.result = []

Since the method is declared as returning a list of objects, the
return value is a dictionary containing a batched list.

    >>> import simplejson
    >>> for key, value in sorted(
    ...         simplejson.loads(read_method_adapter.call(text='')).items()):
    ...     print('%s: %s' % (key, value))
    entries: []
    start: 0
    total_size: 0

Methods exported as a write operations generates an adapter providing
IResourcePOSTOperation.

    >>> from lazr.restful.interfaces import IResourcePOSTOperation

    >>> write_method_adapter_factory = generate_operation_adapter(
    ...     IBookOnSteroids['checkout'])
    >>> IResourcePOSTOperation.implementedBy(write_method_adapter_factory)
    True

The generated adapter class name is POST_<interface>_<operation>_beta.

    >>> print(write_method_adapter_factory.__name__)
    POST_IBookOnSteroids_checkout_beta

The adapter's params property also contains the available parameters
(for which there are none in this case.)

    >>> print_params(write_method_adapter_factory.params)

    >>> @implementer(IBookOnSteroids)
    ... class BookOnSteroids(Book):
    ...     def checkout(self, who, kind):
    ...         print("%s did a %s check out of '%s'." % (
    ...             who, kind, self.title))

    >>> write_method_adapter = write_method_adapter_factory(
    ...     BookOnSteroids(
    ...         'Aldous Huxley', 'The Doors of Perception', 8, 'unknown'),
    ...     FakeRequest())

    >>> verifyObject(IResourcePOSTOperation, write_method_adapter)
    True
    >>> write_method_adapter.send_modification_event
    True

The call() method invokes the exported method on the context object. In
this case, the underlying parameters were set using call_with. The
REQUEST_USER specification is replaced by the current user.

    >>> write_method_adapter.call()
    A user did a normal check out of 'The Doors of Perception'.
    'null'

Methods exported as a factory also generate an adapter providing
IResourcePOSTOperation.

    >>> factory_method_adapter_factory = generate_operation_adapter(
    ...     IBookSetOnSteroids['new'])
    >>> IResourcePOSTOperation.implementedBy(factory_method_adapter_factory)
    True

    >>> factory_method_adapter = factory_method_adapter_factory(
    ...     BookSetOnSteroids(), FakeRequest())
    >>> verifyObject(IResourcePOSTOperation, factory_method_adapter)
    True
    >>> factory_method_adapter.send_modification_event
    False

The generated adapter class name is also
POST_<interface>_<operation>_beta.

    >>> print(write_method_adapter_factory.__name__)
    POST_IBookOnSteroids_checkout_beta

The adapter's params property also contains the available parameters.

    >>> print_params(factory_method_adapter_factory.params)
    author: TextLine
    price: Float
    title: TextLine

Factory operations set the 201 Created status code and return the
URL to the newly created object. The body of the response will be empty.

(For the URL generation to work, we need to register an IAbsoluteURL
adapter and set the request as the current interaction.)

    >>> from urllib.parse import quote
    >>> from zope.component import provideAdapter
    >>> from zope.traversing.browser.interfaces import IAbsoluteURL
    >>> from zope.publisher.interfaces.http import IHTTPApplicationRequest
    >>> @implementer(IAbsoluteURL)
    ... class BookAbsoluteURL:
    ...     """Returns a believable absolute URL for a book."""
    ...
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request
    ...
    ...     def __str__(self):
    ...         return ("http://api.example.org/books/" +
    ...                 quote(self.context.title))
    ...
    ...     __call__ = __str__
    >>> provideAdapter(BookAbsoluteURL,
    ...     [IBook, IHTTPApplicationRequest], IAbsoluteURL)

    >>> from zope.security.management import endInteraction, newInteraction
    >>> endInteraction()
    >>> newInteraction(factory_method_adapter.request)

    >>> print(factory_method_adapter.call(
    ...     author='Aldous Huxley', title="Eyeless in Gaza", price=10.5))
    <BLANKLINE>
    >>> response = factory_method_adapter.request.response
    >>> response.status
    201
    >>> print(response.headers['Location'])
    http://api.example.org/books/Eyeless%20in%20Gaza

The generate_operation_adapter() function can only be called on an
IMethod marked for export:

    >>> generate_operation_adapter(IBook)
    Traceback (most recent call last):
      ...
    TypeError: <...IBook...> doesn't provide IMethod.

    >>> generate_operation_adapter(IBookSet['getAllBooks'])
    Traceback (most recent call last):
      ...
    TypeError: 'getAllBooks' isn't tagged for webservice export.

Methods exported as a destructor operations generates an adapter providing
IResourceDELETEOperation.

    >>> from lazr.restful.interfaces import IResourceDELETEOperation
    >>> destructor_method_adapter_factory = generate_operation_adapter(
    ...     IBookOnSteroids['destroy'])
    >>> IResourceDELETEOperation.implementedBy(
    ...     destructor_method_adapter_factory)
    True

The generated adapter class name is
DELETE_<interface>_<operation>_beta.

    >>> print(destructor_method_adapter_factory.__name__)
    DELETE_IBookOnSteroids_destroy_beta

Destructor
----------

A method can be designated as a destructor for the entry. Here, the
destroy() method is designated as the destructor for IHasText.

    >>> @exported_as_webservice_entry()
    ... class IHasText(Interface):
    ...     text = exported(TextLine(readonly=True))
    ...
    ...     @export_destructor_operation()
    ...     def destroy():
    ...         pass
    >>> ignored = generate_entry_interfaces(IHasText, [], 'beta')

A destructor method cannot take any free arguments.

    >>> @exported_as_webservice_entry()
    ... class IHasText(Interface):
    ...     text = exported(TextLine(readonly=True))
    ...
    ...     @export_destructor_operation()
    ...     @operation_parameters(argument=TextLine())
    ...     def destroy(argument):
    ...         pass
    Traceback (most recent call last):
    ...
    TypeError: A destructor method must take no non-fixed arguments.
    In version (earliest version), the "destroy" method takes 1:
    "argument".

    >>> @exported_as_webservice_entry()
    ... class IHasText(Interface):
    ...     text = exported(TextLine(readonly=True))
    ...
    ...     @export_destructor_operation()
    ...     @call_with(argument="fixed value")
    ...     def destroy(argument):
    ...         pass
    >>> ignored = generate_entry_interfaces(IHasText, [], 'beta')

An entry cannot have more than one destructor.

    >>> from lazr.restful.declarations import export_destructor_operation
    >>> @exported_as_webservice_entry()
    ... class IHasText(Interface):
    ...     text = exported(TextLine(readonly=True))
    ...
    ...     @export_destructor_operation()
    ...     def destroy():
    ...         pass
    ...
    ...     @export_destructor_operation()
    ...     def destroy2():
    ...         pass
    >>> generate_entry_interfaces(IHasText, [], 'beta')
    Traceback (most recent call last):
    ...
    TypeError: An entry can only have one destructor method for
    version (earliest version); destroy... and destroy... make two.

Mutators
--------

A method can be designated as a mutator for some field. Here, the
set_text() method is designated as the mutator for the 'text' field.

    >>> from lazr.restful.declarations import mutator_for
    >>> @exported_as_webservice_entry()
    ... class IHasText(Interface):
    ...     text = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(text)
    ...     @operation_parameters(text=TextLine())
    ...     @export_write_operation()
    ...     def set_text(text):
    ...         pass

The implementation of set_text() applies a standardized transform to the
incoming text.

    >>> @implementer(IHasText)
    ... class HasText:
    ...
    ...     def __init__(self):
    ...         self.text = ''
    ...
    ...     def set_text(self, text):
    ...         self.text = "!" + text + "!"

Generate the entry interface and adapter...

    >>> [hastext_entry_interface] = generate_entry_interfaces(
    ...     IHasText, [], 'beta')
    >>> [hastext_entry_adapter_factory] = generate_entry_adapters(
    ...     IHasText, [], [hastext_entry_interface])

    >>> obj = HasText()
    >>> print(hastext_entry_adapter_factory.version)
    beta
    >>> hastext_entry_adapter = hastext_entry_adapter_factory.object(
    ...     obj, request)

...and you'll have an object that invokes set_text() when you set the
'text' attribute.

    >>> hastext_entry_adapter.text
    ''
    >>> hastext_entry_adapter.text = 'foo'
    >>> hastext_entry_adapter.text
    '!foo!'

The original interface defines 'text' as read-only, but the
generated interface does not.

    >>> hastext_entry_interface.object.get('text').readonly
    False

It's not necessary to expose the mutator method as a write operation.

    >>> @exported_as_webservice_entry()
    ... class IHasText(Interface):
    ...     text = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(text)
    ...     def set_text(text):
    ...         pass


A mutator method must take only one argument: the new value for the
field. Taking no arguments is obviously an error.

    >>> @exported_as_webservice_entry()
    ... class ZeroArgumentMutator(Interface):
    ...     value = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(value)
    ...     def set_value():
    ...         pass
    Traceback (most recent call last):
    ...
    TypeError: A mutator method must take one and only one non-fixed
    argument. set_value takes 0.

Taking more than one argument is also an error...

    >>> @exported_as_webservice_entry()
    ... class TwoArgumentMutator(Interface):
    ...     value = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(value)
    ...     def set_value(arg1, arg2):
    ...         pass
    Traceback (most recent call last):
    ...
    TypeError: A mutator method must take one and only one non-fixed
    argument. set_value takes 2.

...unless all but one of the arguments are spoken for by a call_with()
annotation. This definition does not result in a TypeError.

    >>> @exported_as_webservice_entry()
    ... class OneFixedArgumentMutator(Interface):
    ...     value = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(value)
    ...     @call_with(arg1=REQUEST_USER, arg3='fixed')
    ...     @operation_parameters(arg2=TextLine())
    ...     @export_write_operation()
    ...     def set_value(arg1, arg2, arg3):
    ...         pass

A field can only have a mutator if it's read-only (not settable
directly).

    >>> @exported_as_webservice_entry()
    ... class WritableMutator(Interface):
    ...     value = exported(TextLine(readonly=False))
    ...
    ...     @mutator_for(value)
    ...     @export_write_operation()
    ...     def set_value(new_value):
    ...         pass
    Traceback (most recent call last):
    ...
    TypeError: Only a read-only field can have a mutator method.

A field can only have one mutator.

    >>> @exported_as_webservice_entry()
    ... class FieldWithTwoMutators(Interface):
    ...     value = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(value)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value(new_value):
    ...         pass
    ...
    ...     @mutator_for(value)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value_2(new_value):
    ...         pass
    Traceback (most recent call last):
    ...
    TypeError: A field can only have one mutator method for version
    (earliest version); set_value_2 makes two.

Scopes
------

A method can be tagged with a list of scope names.  If the user has
authenticated in such a way as to limit their access to particular scopes
(indicated by `IWebServiceConfiguration.checkRequest()`), then they can only
call methods that declare at least one of the corresponding scopes.

    >>> from lazr.restful.declarations import scoped
    >>> from zope.component import getUtility

    >>> @exported_as_webservice_entry()
    ... class IScopedEntry(Interface):
    ...
    ...     value = exported(TextLine(readonly=False))
    ...
    ...     @scoped('read')
    ...     @export_read_operation()
    ...     def get_info():
    ...         pass
    ...
    ...     @scoped('update')
    ...     @export_write_operation()
    ...     def do_update():
    ...         pass
    ...
    ...     @scoped('read', 'update')
    ...     @export_write_operation()
    ...     def multiple_scopes():
    ...         pass
    ...
    ...     @export_write_operation()
    ...     def unscoped():
    ...         pass

    >>> @implementer(IScopedEntry)
    ... class ScopedEntry:
    ...
    ...     value = 'initial'
    ...
    ...     def get_info(self):
    ...         print('get_info called')
    ...
    ...     def do_update(self):
    ...         print('do_update called')
    ...
    ...     def multiple_scopes(self):
    ...         print('multiple_scopes called')
    ...
    ...     def unscoped(self):
    ...         print('unscoped called')

    >>> [(version, scoped_entry_interface)] = generate_entry_interfaces(
    ...     IScopedEntry, [], 'beta')
    >>> scoped_entry_adapter_factory = generate_entry_adapters(
    ...     IScopedEntry, [], [(version, scoped_entry_interface)])[0].object

    >>> get_info_method_adapter_factory = generate_operation_adapter(
    ...     IScopedEntry['get_info'])
    >>> IResourceGETOperation.implementedBy(get_info_method_adapter_factory)
    True
    >>> do_update_method_adapter_factory = generate_operation_adapter(
    ...     IScopedEntry['do_update'])
    >>> IResourcePOSTOperation.implementedBy(do_update_method_adapter_factory)
    True
    >>> multiple_scopes_method_adapter_factory = generate_operation_adapter(
    ...     IScopedEntry['multiple_scopes'])
    >>> IResourcePOSTOperation.implementedBy(
    ...     multiple_scopes_method_adapter_factory)
    True
    >>> unscoped_method_adapter_factory = generate_operation_adapter(
    ...     IScopedEntry['unscoped'])
    >>> IResourcePOSTOperation.implementedBy(unscoped_method_adapter_factory)
    True

    >>> obj = ScopedEntry()
    >>> request = FakeRequest(version='beta')
    >>> scoped_entry_adapter = scoped_entry_adapter_factory(obj, request)
    >>> get_info_method_adapter = (
    ...     get_info_method_adapter_factory(obj, request))
    >>> do_update_method_adapter = (
    ...     do_update_method_adapter_factory(obj, request))
    >>> multiple_scopes_method_adapter = (
    ...     multiple_scopes_method_adapter_factory(obj, request))
    >>> unscoped_method_adapter = (
    ...     unscoped_method_adapter_factory(obj, request))

A user with unscoped authentication can call any method, and get or set
attributes.

    >>> _ = get_info_method_adapter.call()
    get_info called
    >>> _ = do_update_method_adapter.call()
    do_update called
    >>> _ = multiple_scopes_method_adapter.call()
    multiple_scopes called
    >>> _ = unscoped_method_adapter.call()
    unscoped called
    >>> print(scoped_entry_adapter.value)
    initial
    >>> scoped_entry_adapter.value = 'set by unscoped user'

A user with both scopes can call any method tagged with either scope, but
can neither get nor set attributes.

    >>> config = getUtility(IWebServiceConfiguration)
    >>> config._scopes = ['read', 'update']
    >>> _ = get_info_method_adapter.call()
    get_info called
    >>> _ = do_update_method_adapter.call()
    do_update called
    >>> _ = multiple_scopes_method_adapter.call()
    multiple_scopes called
    >>> _ = unscoped_method_adapter.call()
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.
    >>> print(scoped_entry_adapter.value)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.
    >>> scoped_entry_adapter.value = 'set by scoped user'
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.

A user with one scope can only call the methods tagged with that scope, and
can neither get nor set attributes.

    >>> config._scopes = ['read']
    >>> _ = get_info_method_adapter.call()
    get_info called
    >>> _ = do_update_method_adapter.call()
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication does not allow calling this method (one of these scopes is required: 'update').
    >>> _ = multiple_scopes_method_adapter.call()
    multiple_scopes called
    >>> _ = unscoped_method_adapter.call()
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.
    >>> print(scoped_entry_adapter.value)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.
    >>> scoped_entry_adapter.value = 'set by scoped user'
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.

    >>> config._scopes = ['update']
    >>> _ = get_info_method_adapter.call()
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication does not allow calling this method (one of these scopes is required: 'read').
    >>> _ = do_update_method_adapter.call()
    do_update called
    >>> _ = multiple_scopes_method_adapter.call()
    multiple_scopes called
    >>> _ = unscoped_method_adapter.call()
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.
    >>> print(scoped_entry_adapter.value)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.
    >>> scoped_entry_adapter.value = 'set by scoped user'
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.security.interfaces.Unauthorized: Current authentication only allows calling scoped methods.

    >>> config._scopes = None

Read-only fields
----------------

A read-write field can be published as read-only in the web service.

    >>> @exported_as_webservice_entry()
    ... class ExternallyReadOnlyField(Interface):
    ...     value = exported(TextLine(readonly=False), readonly=True)

    >>> interfaces = generate_entry_interfaces(
    ...     ExternallyReadOnlyField, [], 'beta')
    >>> [(beta, beta_interface)] = interfaces

    >>> ExternallyReadOnlyField['value'].readonly
    False
    >>> beta_interface['value'].readonly
    True

A read-only field cannot be published as read-write in the web service
just by declaring it read-write. You have to provide a
mutator.

    >>> @exported_as_webservice_entry()
    ... class InternallyReadOnlyField(Interface):
    ...     value = exported(TextLine(readonly=True), readonly=False)

    >>> generate_entry_interfaces(InternallyReadOnlyField, [], 'beta')
    Traceback (most recent call last):
    ...
    TypeError: InternallyReadOnlyField.value is defined as a read-only
    field, so you can't just declare it to be read-write in the web
    service: you must define a mutator.

Caching
-------

It is possible to cache a server response in the browser cache using
the @cache_for decorator:

    >>> from lazr.restful.declarations import cache_for
    >>> @exported_as_webservice_collection(IBook)
    ... class ICachedBookSet(IBookSet):
    ...     """IBookSet supporting caching."""
    ...
    ...     @collection_default_content()
    ...     @export_read_operation()
    ...     @cache_for(60)
    ...     def getAllBooks():
    ...         """Return all books."""
    ...
    ...
    >>> @implementer(ICachedBookSet)
    ... class CachedBookSet(BookSet):
    ...     """Simple ICachedBookSet implementation."""
    ...
    ...     def getAllBooks(self):
    ...         return self.books

    >>> read_method_adapter_factory = generate_operation_adapter(
    ...     ICachedBookSet['getAllBooks'])
    >>> read_method_adapter = read_method_adapter_factory(
    ...     CachedBookSet(['Cool book']), request)
    >>> print(read_method_adapter.call())
    ['Cool book']
    >>> for name, value in sorted(request.response.headers.items()):
    ...     print('%s: %s' % (name, value))
    Cache-control: max-age=60
    Content-Type: application/json

Only positive int or long objects should be passed to @cache_for:

    >>> class ICachedBookSet(IBookSet):
    ...     @cache_for('60')
    ...     def getAllBooks():
    ...         """Return all books."""
    ...
    Traceback (most recent call last):
    ...
    TypeError: Caching duration should be an integer type, not str
    >>>
    >>> class ICachedBookSet(IBookSet):
    ...     @cache_for(-15)
    ...     def getAllBooks():
    ...         """Return all books."""
    ...
    Traceback (most recent call last):
    ...
    ValueError: Caching duration should be a positive number: -15

Versioned services
==================

Different versions of the webservice can publish the same data model
object in totally different ways.

Collections
-----------

A collection's contents are determined by calling one of its
methods. Which method is called, and with which arguments, can vary
across versions.

    >>> from lazr.restful.declarations import generate_operation_adapter

    >>> @exported_as_webservice_collection(Interface)
    ... class IMultiVersionCollection(Interface):
    ...     @collection_default_content('2.0')
    ...     def content_20():
    ...         """The content method for version 2.0."""
    ...
    ...     @collection_default_content('1.0', argument='1.0 value')
    ...     @collection_default_content(argument='pre-1.0 value')
    ...     def content_pre_20(argument):
    ...         """The content method for versions before 2.0"""

Here's a simple implementation of IMultiVersionCollection. It'll
illustrate how the different versions of the web service invoke
different methods to find the collection contents.

    >>> @implementer(IMultiVersionCollection)
    ... class MultiVersionCollection():
    ...     """Simple IMultiVersionCollection implementation."""
    ...
    ...     def content_20(self):
    ...         return ["contents", "for", "version", "2.0"]
    ...
    ...     def content_pre_20(self, argument):
    ...         return ["you", "passed", "in", argument]

By passing a version string into generate_collection_adapter(), we can
get different adapter classes for different versions of the web
service. We'll be invoking each version against the same data model
object. Here it is:

    >>> data_object = MultiVersionCollection()

Passing in None to generate_collection_adapter gets us the collection
as it appears in the earliest version of the web service. The
content_pre_20() method is invoked with the 'argument' parameter equal
to "pre-1.0 value".

    >>> interface = IMultiVersionCollection
    >>> adapter_earliest_factory = generate_collection_adapter(
    ...     interface, None)
    >>> print(adapter_earliest_factory.__name__)
    MultiVersionCollectionCollectionAdapter___Earliest

    >>> collection_earliest = adapter_earliest_factory(data_object, request)
    >>> print(collection_earliest.find())
    ['you', 'passed', 'in', 'pre-1.0 value']

Passing in '1.0' gets us the collection as it appears in the 1.0
version of the web service. Note that the argument passed in to
content_pre_20() is different, and so the returned contents are
slightly different.

    >>> adapter_10_factory = generate_collection_adapter(interface, '1.0')
    >>> print(adapter_10_factory.__name__)
    MultiVersionCollectionCollectionAdapter_1_0

    >>> collection_10 = adapter_10_factory(data_object, request)
    >>> print(collection_10.find())
    ['you', 'passed', 'in', '1.0 value']

Passing in '2.0' gets us a collection with totally different contents,
because a totally different method is being called.

    >>> adapter_20_factory = generate_collection_adapter(interface, '2.0')
    >>> print(adapter_20_factory.__name__)
    MultiVersionCollectionCollectionAdapter_2_0

    >>> collection_20 = adapter_20_factory(data_object, request)
    >>> print(collection_20.find())
    ['contents', 'for', 'version', '2.0']

An error occurs when we try to generate an adapter for a version
that's not mentioned in the annotations.

    >>> generate_collection_adapter(interface, 'NoSuchVersion')
    Traceback (most recent call last):
    ...
    AssertionError: 'IMultiVersionCollection' isn't tagged for export
    to web service version 'NoSuchVersion'.

Entries
-------

The singular and plural name of an entry never changes between
versions, because the names are a property of the original
interface. But the published fields can change or be renamed from
version to version.

Here's a data model interface defining four fields which are published
in some versions and not others, and which may have different names in
different versions.

1. A TextLine called 'field', published in all versions.
2. A Text called 'unchanging_name', published in all versions.
3. A TextLine called 'field3' in the earliest version, removed in '1.0',
   published as '20_name' in '2.0', and renamed to '30_name' in '3.0'.
4. A Float not published in the earliest version, introduced as
   'new_in_10' in '1.0', and renamed to 'renamed_in_30' in '3.0'.

    >>> from zope.schema import Text, Float
    >>> @exported_as_webservice_entry()
    ... class IMultiVersionEntry(Interface):
    ...     field = exported(TextLine())
    ...
    ...     field2 = exported(Text(), exported_as='unchanging_name')
    ...
    ...     field3 = exported(TextLine(),
    ...         ('3.0', dict(exported_as='30_name')),
    ...         ('2.0', dict(exported=True, exported_as='20_name')),
    ...         ('1.0', dict(exported=False)))
    ...
    ...     field4 = exported(Float(),
    ...         ('3.0', dict(exported_as='renamed_in_30')),
    ...         ('1.0', dict(exported=True, exported_as='new_in_10')),
    ...         exported=False)

Let's take a look at the entry interfaces generated for each version.

    >>> versions = ['beta', '1.0', '2.0', '3.0']
    >>> versions_and_interfaces = generate_entry_interfaces(
    ...     IMultiVersionEntry, [], *versions)

    >>> for version, interface in versions_and_interfaces:
    ...     print(version)
    beta
    1.0
    2.0
    3.0

    >>> interface_beta, interface_10, interface_20, interface_30 = (
    ...     [interface for version, interface in versions_and_interfaces])

    >>> dump_entry_interface(interface_beta)
    field: TextLine
    field3: TextLine
    unchanging_name: Text

    >>> dump_entry_interface(interface_10)
    field: TextLine
    new_in_10: Float
    unchanging_name: Text

    >>> dump_entry_interface(interface_20)
    20_name: TextLine
    field: TextLine
    new_in_10: Float
    unchanging_name: Text

    >>> dump_entry_interface(interface_30)
    30_name: TextLine
    field: TextLine
    renamed_in_30: Float
    unchanging_name: Text


Here's a simple implementation of the entry.

    >>> @implementer(IMultiVersionEntry)
    ... class MultiVersionEntry():
    ...     """Simple IMultiVersionEntry implementation."""
    ...     field = "field value"
    ...     field2 = "unchanging value"
    ...     field3 = "field 3 value"
    ...     field4 = 1.0


When we call generate_entry_adapters(), we'll get an adapter
classes for each version of the web service. We'll be invoking
each version against the same data model object. Here it is:

    >>> data_object = MultiVersionEntry()


generate_entry_adapters() generates adaptor factories that mediate
between this data model object and the many-faceted interface
classes.

    >>> entry_adapters = generate_entry_adapters(
    ...     IMultiVersionEntry, [], versions_and_interfaces)

    >>> for version, adapter in entry_adapters:
    ...     print(version)
    beta
    1.0
    2.0
    3.0

    >>> adapter_beta, adapter_10, adapter_20, adapter_30 = (
    ...     [interface for version, interface in entry_adapters])

Here's the 'beta' version of the object:

    >>> object_beta = adapter_beta(data_object, request)
    >>> print(object_beta.field)
    field value
    >>> print(object_beta.field3)
    field 3 value
    >>> print(object_beta.unchanging_name)
    unchanging value

The 'field4' field is not available in the 'beta' version under any name.

    >>> print(object_beta.field4)
    Traceback (most recent call last):
    ...
    AttributeError: 'MultiVersionEntryEntry_betaAdapter' object has no
    attribute 'field4'

    >>> print(object_beta.new_in_10)
    Traceback (most recent call last):
    ...
    AttributeError: 'MultiVersionEntryEntry_betaAdapter' object has no
    attribute 'new_in_10'

Here's the '1.0' version. 'field3' is gone and the 'field4' field is
now available as 'new_in_10'.

    >>> object_10 = adapter_10(data_object, request)
    >>> print(object_10.field)
    field value
    >>> print(object_10.unchanging_name)
    unchanging value
    >>> print(object_10.new_in_10)
    1.0

    >>> object_10.field3
    Traceback (most recent call last):
    ...
    AttributeError: 'MultiVersionEntryEntry_1_0Adapter' object has no
    attribute 'field3'

Here's the '2.0' version. 'field3' is back, but now it's called '20_name'.

    >>> object_20 = adapter_20(data_object, request)
    >>> print(object_20.field)
    field value
    >>> print(object_20.unchanging_name)
    unchanging value
    >>> print(getattr(object_20, '20_name'))
    field 3 value
    >>> print(object_20.new_in_10)
    1.0

Here's the '3.0' version. 'field3' has been renamed to '30_name' and
'field4' has been renamed to 'renamed_in_30'

    >>> object_30 = adapter_30(data_object, request)
    >>> print(object_30.field)
    field value
    >>> print(object_30.unchanging_name)
    unchanging value
    >>> print(getattr(object_30, '30_name'))
    field 3 value
    >>> print(object_30.renamed_in_30)
    1.0

    >>> getattr(object_30, '20_name')
    Traceback (most recent call last):
    ...
    AttributeError: 'MultiVersionEntryEntry_3_0Adapter' object has no
    attribute '20_name'

    >>> object_30.new_in_10
    Traceback (most recent call last):
    ...
    AttributeError: 'MultiVersionEntryEntry_3_0Adapter' object has no
    attribute 'new_in_10'

Why the list of version strings?
================================

Why does generate_entry_interfaces need a list of version strings?
This example should make it clear.

    >>> @exported_as_webservice_entry()
    ... class IAmbiguousMultiVersion(Interface):
    ...     field1 = exported(TextLine(),
    ...         ('foo', dict(exported_as='foo_name')))
    ...     field2 = exported(TextLine(),
    ...         ('bar', dict(exported_as='bar_name')))

This web service clearly has two versions, 'foo', and 'bar', but which
is the earlier version and which the later? If 'foo' is the earlier
version, then 'bar' inherits behavior from 'foo'.

    >>> foo, bar = generate_entry_interfaces(
    ...     IAmbiguousMultiVersion, [], 'foo', 'bar')

    >>> print(foo.version)
    foo
    >>> dump_entry_interface(foo.object)
    field2: TextLine
    foo_name: TextLine

    >>> print(bar.version)
    bar
    >>> dump_entry_interface(bar.object)
    bar_name: TextLine
    foo_name: TextLine

But if 'bar' is the earlier version, then 'foo' inherits behavior from
'bar'. (We need to redefine the class because our previous call to
generate_entry_interfaces() modified the class to reflect the original
list of versions.)

    >>> @exported_as_webservice_entry()
    ... class IAmbiguousMultiVersion(Interface):
    ...     field1 = exported(TextLine(),
    ...         ('foo', dict(exported_as='foo_name')))
    ...     field2 = exported(TextLine(),
    ...         ('bar', dict(exported_as='bar_name')))

    >>> bar, foo = generate_entry_interfaces(
    ...     IAmbiguousMultiVersion, [], 'bar', 'foo')

    >>> print(bar.version)
    bar
    >>> dump_entry_interface(bar.object)
    bar_name: TextLine
    field1: TextLine

    >>> print(foo.version)
    foo
    >>> dump_entry_interface(foo.object)
    bar_name: TextLine
    foo_name: TextLine

If a web service definition is complex enough, it's possible to derive
an ordered list of all the versions just from looking at the field
annotations. But it's not possible in general, and that's why
generate_entry_interfaces takes a list of versions.

Error handling
==============

You'll get an error if you annotate a field with a version that turns
out not to be included in the version list.

    >>> @exported_as_webservice_entry()
    ... class INonexistentVersionEntry(Interface):
    ...     field = exported(TextLine(),
    ...         ('2.0', dict(exported_as='foo')),
    ...         ('1.0', dict(exported_as='bar')))

    >>> generate_entry_interfaces(
    ...     INonexistentVersionEntry, [], 'beta', '1.0')
    Traceback (most recent call last):
    ...
    ValueError: Field "field" in interface "INonexistentVersionEntry":
    Unrecognized version "2.0".

You'll get an error if you put an earlier version's annotations on top
of a later version.

    >>> @exported_as_webservice_entry()
    ... class IWrongOrderEntry(Interface):
    ...     field = exported(TextLine(),
    ...         ('1.0', dict(exported_as='bar')),
    ...         ('2.0', dict(exported_as='foo')))

    >>> generate_entry_interfaces(IWrongOrderEntry, [], '1.0', '2.0')
    Traceback (most recent call last):
    ...
    ValueError: Field "..." in interface "IWrongOrderEntry":
    Version "1.0" defined after the later version "2.0".

You'll get an error if you define annotations twice for the same
version. This can happen because you repeated the version annotations:

    >>> @exported_as_webservice_entry()
    ... class IDuplicateEntry(Interface):
    ...     field = exported(TextLine(),
    ...         ('beta', dict(exported_as='another_beta_name')),
    ...         ('beta', dict(exported_as='beta_name')))

    >>> generate_entry_interfaces(IDuplicateEntry, [], 'beta', '1.0')
    Traceback (most recent call last):
    ...
    ValueError: Field "field" in interface "IDuplicateEntry":
    Duplicate definitions for version "beta".

Or it can happen because you defined the earliest version implicitly
using keyword arguments, and then explicitly defined conflicting
values.

    >>> @exported_as_webservice_entry()
    ... class IDuplicateEntry(Interface):
    ...     field = exported(TextLine(),
    ...         ('beta', dict(exported_as='beta_name')),
    ...         exported_as='earliest_name')

    >>> generate_entry_interfaces(IDuplicateEntry, [], 'beta', '1.0')
    Traceback (most recent call last):
    ...
    ValueError: Field "field" in interface "IDuplicateEntry":
    Annotation "as" has conflicting values for the earliest version:
    "earliest_name" (from keyword arguments) and "beta_name" (defined
    explicitly).

You'll get an error if you include an unrecognized key in a field's
version definition.

    >>> @exported_as_webservice_entry()
    ... class InvalidMultiVersionEntry(Interface):
    ...     field = exported(TextLine(),
    ...         ('3.0', dict(not_recognized='this will error')))
    Traceback (most recent call last):
    ...
    ValueError: Unrecognized annotation for version "3.0": "not_recognized"

    >>> @exported_as_webservice_entry()
    ... class InvalidMultiVersionEntry(Interface):
    ...     field = exported(TextLine(), not_recognized='this will error')
    Traceback (most recent call last):
    ...
    TypeError: exported got an unexpected keyword argument 'not_recognized'

generate_entry_interfaces() generates an interface class for
every version, even when an interface does not change at all between
versions. (This could be optimized away.)

    >>> @exported_as_webservice_entry()
    ... class IUnchangingEntry(Interface):
    ...     field = exported(TextLine(),
    ...         ('3.0', dict(exported_as='30_name')),
    ...         ('beta', dict(exported_as='unchanging_name')))

    >>> [interface.version for interface in
    ...      generate_entry_interfaces(IUnchangingEntry, [], *versions)]
    ['beta', '1.0', '2.0', '3.0']

Named operations
----------------

It's easy to reflect the most common changes between versions:
operations and arguments being renamed, changes in fixed values, etc.
This method appears differently in three versions of the web service:
2.0, 1.0, and in an unnamed pre-1.0 version.

    >>> from lazr.restful.declarations import operation_for_version
    >>> @exported_as_webservice_entry()
    ... class IMultiVersionMethod(Interface):
    ...     @cache_for(300)
    ...     @operation_for_version('3.0')
    ...
    ...     @call_with(fixed='2.0 value', user=REQUEST_USER)
    ...     @operation_for_version('2.0')
    ...
    ...     @call_with(fixed='1.0 value', user=REQUEST_USER)
    ...     @export_operation_as('new_name')
    ...     @rename_parameters_as(required="required_argument")
    ...     @operation_for_version('1.0')
    ...
    ...     @call_with(fixed='pre-1.0 value', user=REQUEST_USER)
    ...     @cache_for(100)
    ...     @operation_parameters(
    ...         required=TextLine(),
    ...         fixed=TextLine()
    ...         )
    ...     @export_read_operation()
    ...     def a_method(required, fixed, user):
    ...         """Method demonstrating multiversion publication."""

Here's a simple implementation of IMultiVersionMethod. It'll
illustrate how the different versions of the web service invoke
`a_method` with different hard-coded values for the `fixed` argument.

    >>> @implementer(IMultiVersionMethod)
    ... class MultiVersionMethod():
    ...     """Simple IMultiVersionMethod implementation."""
    ...
    ...     def a_method(self, required, fixed, user):
    ...         return "Required value: %s. Fixed value: %s. User: %s." % (
    ...             required, fixed, user)

By passing a version string into generate_operation_adapter(), we can
get different adapter classes for different versions of the web
service. We'll be invoking each version against the same data model
object. Here it is:

    >>> data_object = MultiVersionMethod()

Passing in None to generate_operation_adapter gets us the method as it
appears in the earliest version of the web service.

    >>> method = IMultiVersionMethod['a_method']
    >>> adapter_earliest_factory = generate_operation_adapter(method, None)
    >>> print(adapter_earliest_factory.__name__)
    GET_IMultiVersionMethod_a_method_beta

    >>> method_earliest = adapter_earliest_factory(data_object, request)
    >>> print(method_earliest.call(required="foo"))
    Required value: foo. Fixed value: pre-1.0 value. User: A user.

Passing in '1.0' or '2.0' gets us the method as it appears in the
appropriate version of the web service. Note that the name of the
adapter factory changes to reflect the fact that the method's name in
1.0 is 'new_name', not 'a_method'.

    >>> adapter_10_factory = generate_operation_adapter(method, '1.0')
    >>> print(adapter_10_factory.__name__)
    GET_IMultiVersionMethod_new_name_1_0

    >>> method_10 = adapter_10_factory(data_object, request)
    >>> print(method_10.call(required="bar"))
    Required value: bar. Fixed value: 1.0 value. User: A user.

    >>> adapter_20_factory = generate_operation_adapter(method, '2.0')
    >>> print(adapter_20_factory.__name__)
    GET_IMultiVersionMethod_new_name_2_0

    >>> method_20 = adapter_20_factory(data_object, request)
    >>> print(method_20.call(required="baz"))
    Required value: baz. Fixed value: 2.0 value. User: A user.

    >>> adapter_30_factory = generate_operation_adapter(method, '3.0')
    >>> print(adapter_30_factory.__name__)
    GET_IMultiVersionMethod_new_name_3_0
    >>> method_30 = adapter_30_factory(data_object, request)
    >>> print(method_30.call(required="baz"))
    Required value: baz. Fixed value: 2.0 value. User: A user.

An error occurs when we try to generate an adapter for a version
that's not mentioned in the annotations.

    >>> generate_operation_adapter(method, 'NoSuchVersion')
    Traceback (most recent call last):
    ...
    AssertionError: 'a_method' isn't tagged for export to web service
    version 'NoSuchVersion'

Now that we've seen how lazr.restful uses the annotations to create
classes, let's take a closer look at how the 'a_method' method object
is annotated.

    >>> dictionary = method.getTaggedValue('lazr.restful.exported')

The tagged value containing the annotations looks like a dictionary,
but it's actually a stack of dictionaries named after the versions.

    >>> dictionary.dict_names
    [None, '1.0', '2.0', '3.0']

The dictionary on top of the stack is for the 3.0 version of the web
service. This version inherits its name ('new_name') and its fixed
arguments ('2.0 value' and REQUEST_USER) from the 2.0 version, but it
also sets a new value for 'cache_for'.

    >>> print(dictionary['as'])
    new_name
    >>> print(pformat(dictionary['call_with']))
    {'fixed': '2.0 value',
     'user': <class '...REQUEST_USER'>}
    >>> dictionary['cache_for']
    300

Let's pop the 3.0 version off the stack. Now we can see how the method
looks in 2.0. In 2.0, the method is published as 'new_name' and its
'fixed' argument is fixed to the string '2.0 value'. It inherits its
value for 'cache_for' from version 1.0.

    >>> ignored = dictionary.pop()
    >>> print(dictionary['as'])
    new_name
    >>> print(pformat(dictionary['call_with']))
    {'fixed': '2.0 value',
     'user': <class '...REQUEST_USER'>}
    >>> dictionary['cache_for']
    100

The published name of the 'required' argument is 'required_argument',
not 'required'.

    >>> print(dictionary['params']['required'].__name__)
    required_argument

Let's pop the 2.0 version off the stack. Now we can see how the method
looks in 1.0. It's still called 'new_name', and its 'required'
argument is still called 'required_argument', but its 'fixed' argument
is fixed to the string '1.0 value'.

    >>> ignored = dictionary.pop()
    >>> print(dictionary['as'])
    new_name
    >>> print(pformat(dictionary['call_with']))
    {'fixed': '1.0 value',
     'user': <class '...REQUEST_USER'>}
    >>> print(dictionary['params']['required'].__name__)
    required_argument
    >>> dictionary['cache_for']
    100

Let's pop one more time to see how the method looks in the pre-1.0
version. It hasn't yet been renamed to 'new_name', its 'required'
argument hasn't yet been renamed to 'required_argument', and its
'fixed' argument is fixed to the string 'pre-1.0 value'.

    >>> ignored = dictionary.pop()
    >>> print(dictionary['as'])
    a_method
    >>> print(dictionary['params']['required'].__name__)
    required
    >>> print(pformat(dictionary['call_with']))
    {'fixed': 'pre-1.0 value',
     'user': <class '...REQUEST_USER'>}
    >>> dictionary['cache_for']
    100

@operation_removed_in_version
=============================

Sometimes you want version n+1 to remove a named operation that was
present in version n. The @operation_removed_in_version declaration
does just this.

Let's define an operation that's introduced in 1.0 and removed in 2.0.

    >>> from lazr.restful.declarations import operation_removed_in_version
    >>> @exported_as_webservice_entry()
    ... class DisappearingMultiversionMethod(Interface):
    ...     @operation_removed_in_version(2.0)
    ...     @operation_parameters(arg=Float())
    ...     @export_read_operation()
    ...     @operation_for_version(1.0)
    ...     def method(arg):
    ...         """A doomed method."""

    >>> dictionary = DisappearingMultiversionMethod[
    ...     'method'].getTaggedValue('lazr.restful.exported')

The method is not present in 2.0:

    >>> version, attrs = dictionary.pop()
    >>> print(version)
    2.0
    >>> sorted(attrs.items())
    [('type', 'removed_operation')]

It is present in 1.0:

    >>> version, attrs = dictionary.pop()
    >>> print(version)
    1.0
    >>> print(attrs['type'])
    read_operation
    >>> print(repr(attrs['params']['arg']))
    <zope.schema._field.Float object...>

But it's not present in the unnamed pre-1.0 version, since it hadn't
been defined yet:

    >>> pre_10 = dictionary.pop()
    >>> print(pre_10.version)
    None
    >>> print(pre_10.object)
    {'type': 'removed_operation'}

The @operation_removed_in_version declaration can also be used to
reset a named operation's definition if you need to completely re-do
it.

For instance, ordinarily you can't change the type of an operation, or
totally redefine its parameters--and you shouldn't really need
to. It's usually easier to publish two different operations that have
the same name in different versions. But you can do it with a single
operation, by removing the operation with
@operation_removed_in_version and defining it again--either in the
same version or in some later version.

In this example, the type of the operation, the type and number of the
arguments, and the return value change in version 1.0.

    >>> @exported_as_webservice_entry()
    ... class ReadOrWriteMethod(Interface):
    ...     @operation_parameters(arg=TextLine(), arg2=TextLine())
    ...     @export_write_operation()
    ...     @operation_removed_in_version(1.0)
    ...
    ...     @operation_parameters(arg=Float())
    ...     @operation_returns_collection_of(Interface)
    ...     @export_read_operation()
    ...     def method(arg, arg2='default'):
    ...         """A read *or* a write operation, depending on version."""

    >>> dictionary = ReadOrWriteMethod[
    ...     'method'].getTaggedValue('lazr.restful.exported')

In version 1.0, the 'method' named operation is a write operation that
takes two TextLine arguments and has no special return value.

    >>> version, attrs = dictionary.pop()
    >>> print(version)
    1.0
    >>> print(attrs['type'])
    write_operation
    >>> attrs['params']['arg']
    <zope.schema._bootstrapfields.TextLine object...>
    >>> attrs['params']['arg2']
    <zope.schema._bootstrapfields.TextLine object...>
    >>> print(attrs.get('return_type'))
    None

In the unnamed pre-1.0 version, the 'method' operation is a read
operation that takes a single Float argument and returns a collection.

    >>> version, attrs = dictionary.pop()
    >>> print(attrs['type'])
    read_operation

    >>> attrs['params']['arg']
    <zope.schema._field.Float object...>
    >>> list(attrs['params'])
    ['arg']

    >>> attrs['return_type']
    <lazr.restful.fields.CollectionField object...>

Mutators
========

Different versions can define different mutator methods for the same field.

    >>> @exported_as_webservice_entry()
    ... class IDifferentMutators(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_for_version('beta')
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value(new_value):
    ...         pass
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_for_version('1.0')
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value_2(new_value):
    ...         pass

    >>> ignored = generate_entry_interfaces(
    ...     IDifferentMutators, [], 'beta', '1.0')

But you can't define two mutators for the same field in the same version.

    >>> @exported_as_webservice_entry()
    ... class IDuplicateMutator(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_for_version('1.0')
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value(new_value):
    ...         pass
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_for_version('1.0')
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value_2(new_value):
    ...         pass
    Traceback (most recent call last):
    ...
    TypeError: A field can only have one mutator method for version
    1.0; set_value_2 makes two.

Here's a case that's a little trickier. You'll also get an error if
you implicitly define a mutator for the earliest version (without
giving its name), and then define another one explicitly (giving the
name of the earliest version.)

    >>> @exported_as_webservice_entry()
    ... class IImplicitAndExplicitMutator(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_for_version('beta')
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value_2(new_value):
    ...         pass
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value_2(new_value):
    ...         pass

    >>> generate_entry_interfaces(
    ...     IImplicitAndExplicitMutator, [], 'beta', '1.0')
    Traceback (most recent call last):
    ...
    ValueError: Field "field" in interface
    "IImplicitAndExplicitMutator": Both implicit and explicit mutator
    definitions found for earliest version beta.

This error isn't detected until you try to generate the entry
interfaces, because until that point lazr.restful doesn't know that
'beta' is the earliest version. If the earliest version was 'alpha',
the IImplicitAndExplicitMutator class would be valid.

(Again, to test this hypothesis, we need to re-define the class,
because the generate_entry_interfaces call modified the original
class's annotations in place.)

    >>> @exported_as_webservice_entry()
    ... class IImplicitAndExplicitMutator(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_for_version('beta')
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value_2(new_value):
    ...         pass
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value_2(new_value):
    ...         pass

    >>> ignored = generate_entry_interfaces(
    ...     IImplicitAndExplicitMutator, [], 'alpha', 'beta', '1.0')

Destructor operations
=====================

A destructor can be published in different ways in different versions,
but the restrictions on destructor arguments are enforced separately
for each version.

Here, the destructor fixes a value for the 'fixed2' argument in the
earliest version, but not in '1.0'. This is fine: the 1.0 value for
'fixed2' will be inherited from the previous version.

    >>> @exported_as_webservice_entry()
    ... class IGoodDestructorEntry(Interface):
    ...     @call_with(fixed1="value3")
    ...     @operation_for_version('1.0')
    ...     @export_destructor_operation()
    ...     @call_with(fixed1="value1", fixed2="value")
    ...     @operation_parameters(fixed1=TextLine(), fixed2=TextLine())
    ...     def destructor(fixed1, fixed2):
    ...         """Another destructor method."""

    >>> ignore = generate_entry_interfaces(
    ...     IGoodDestructorEntry, [], 'beta', '1.0')

In this next example, the destructor is removed in 1.0 and
added back in 2.0. The 2.0 version does not inherit any values from
its prior incarnation, so the fact that it does not fix any value for
'fixed2' is a problem. The fact that 'fixed2' is fixed in 3.0 doesn't
help; the method is incompletely specified in 2.0.

    >>> @exported_as_webservice_entry()
    ... class IBadDestructorEntry(Interface):
    ...     @call_with(fixed2="value4")
    ...     @operation_for_version('2.0')
    ...     @export_destructor_operation()
    ...     @operation_parameters(fixed1=TextLine(), fixed2=TextLine())
    ...     @call_with(fixed1="value3")
    ...     @operation_for_version('2.0')
    ...     @operation_removed_in_version('1.0')
    ...     @export_destructor_operation()
    ...     @call_with(fixed1="value1", fixed2="value")
    ...     @operation_parameters(fixed1=TextLine(), fixed2=TextLine())
    ...     def destructor(fixed1, fixed2):
    ...         """Another destructor method."""
    Traceback (most recent call last):
    ...
    TypeError: A destructor method must take no non-fixed
    arguments. In version 2.0, the "destructor" method takes 1:
    "fixed2".


Security
========

The adapters have checkers defined for them that grant access to all
attributes in the interface. (There is no reason to protect them since
the underlying content security checker will still apply.)

::

    >>> from lazr.restful.debug import debug_proxy
    >>> from zope.security.checker import ProxyFactory

    # ProxyFactory wraps the content using the defined checker.
    >>> print(debug_proxy(ProxyFactory(entry_adapter)))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        public: author, price, schema, title
        public (set): author, price, schema, title

    >>> print(debug_proxy(ProxyFactory(collection_adapter)))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        public: entry_schema, find

    >>> print(debug_proxy(ProxyFactory(read_method_adapter)))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        public: __call__, return_type, send_modification_event

    >>> print(debug_proxy(ProxyFactory(write_method_adapter)))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        public: __call__, send_modification_event

    >>> print(debug_proxy(ProxyFactory(factory_method_adapter)))
    zope.security._proxy._Proxy (using zope.security.checker.Checker)
        public: __call__, send_modification_event

ZCML Registration
=================

There is a ZCML directive available that will inspect a given module and
generate and register all the interfaces and adapters for all interfaces
marked for export.

(Put the interface in a module where it will be possible for the ZCML
handler to inspect.)

    >>> from lazr.restful.testing.helpers import register_test_module
    >>> bookexample = register_test_module(
    ...     'bookexample', IBook, IBookSet, IBookOnSteroids,
    ...     IBookSetOnSteroids, ISimpleComment, InvalidEmail)

After the registration, adapters from IBook to IEntry, and IBookSet to
ICollection are available:

    >>> from zope.component import getMultiAdapter
    >>> book = Book('George Orwell', '1984', 10.0, '12345-1984')
    >>> bookset = BookSet([book])

    >>> entry_adapter = getMultiAdapter((book, request), IEntry)
    >>> verifyObject(IEntry, entry_adapter)
    True

    >>> print(entry_adapter.schema.__name__)
    IBookEntry_beta
    >>> verifyObject(entry_adapter.schema, entry_adapter)
    True

    >>> collection_adapter = getMultiAdapter((bookset, request), ICollection)
    >>> verifyObject(ICollection, collection_adapter)
    True

IResourceOperation adapters named under the exported method names
are also available for IBookSetOnSteroids and IBookOnSteroids.

    >>> from zope.component import getGlobalSiteManager
    >>> adapter_registry = getGlobalSiteManager().adapters

    >>> from lazr.restful.interfaces import IWebServiceClientRequest
    >>> request_interface = IWebServiceClientRequest
    >>> adapter_registry.lookup(
    ...     (IBookSetOnSteroids, request_interface),
    ...     IResourceGETOperation, 'searchBookTitles')
    <class '...GET_IBookSetOnSteroids_searchBookTitles_beta'>
    >>> adapter_registry.lookup(
    ...     (IBookSetOnSteroids, request_interface),
    ...     IResourcePOSTOperation, 'create_book')
    <class '...POST_IBookSetOnSteroids_create_book_beta'>
    >>> adapter_registry.lookup(
    ...     (IBookOnSteroids, request_interface),
    ...     IResourcePOSTOperation, 'checkout')
    <class '...POST_IBookOnSteroids_checkout_beta'>

There is also a 'index.html' view on the IWebServiceClientRequest
registered for the InvalidEmail exception.

    >>> from zope.interface import implementedBy
    >>> adapter_registry.lookup(
    ...     (implementedBy(InvalidEmail), IWebServiceClientRequest),
    ...     Interface, 'index.html')
    <class '...WebServiceExceptionView'>

(Clean-up.)

    >>> del bookexample
    >>> del sys.modules['lazr.restful.bookexample']

Error handling
--------------

Some error handling happens in the ZCML registration phase. At this
point, all the annotations have been processed, and the
IWebServiceConfiguration utility (with its canonical list of versions)
has become available. This lets us run checks on the versioning
annotations that couldn't be run before.

Here's a class annotated by someone who believes that version 1.0 of
the web service is a later version than version 2.0. (Or who believes
that named operation annotations proceed from the top down rather than
the bottom up.)

    >>> @exported_as_webservice_entry()
    ... class WrongOrderVersions(Interface):
    ...     @export_operation_as('10_name')
    ...     @operation_for_version("1.0")
    ...     @operation_parameters(arg=Float())
    ...     @export_read_operation()
    ...     @operation_for_version("2.0")
    ...     def method(arg):
    ...         """A method."""

An attempt to register this module with ZCML results in an error
explaining the problem.

    >>> register_test_module('wrongorder', WrongOrderVersions)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.configuration.config.ConfigurationExecutionError: ...AssertionError... Annotations on "WrongOrderVersions.method" put an earlier version on top of a later version: "beta", "2.0", "1.0". The correct order is: "beta", "1.0", "2.0"...

Here's a class in which a named operation is removed in version 1.0
and then annotated without being reinstated.

    >>> @exported_as_webservice_entry()
    ... class AnnotatingARemovedMethod(Interface):
    ...     @operation_parameters(arg=TextLine())
    ...     @export_operation_as('already_been_removed')
    ...     @operation_removed_in_version("2.0")
    ...     @operation_parameters(arg=Float())
    ...     @export_read_operation()
    ...     @operation_for_version("1.0")
    ...     def method(arg):
    ...         """A method."""

    >>> register_test_module('annotatingremoved', AnnotatingARemovedMethod)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.configuration.config.ConfigurationExecutionError: ... Method "method" contains annotations for version "2.0", even though it's not published in that version. The bad annotations are: "as", "params"...

Mutators as named operations
----------------------------

In earlier versions of lazr.restful, mutator methods were published as
named operations. This behavior is now deprecated and will eventually
be removed. But to maintain backwards compatibility, mutator methods
are still published as named operations up to a certain point. The
MyWebServiceConfiguration class (above) defines
last_version_with_mutator_named_operations as '1.0', meaning that in
'beta' and '1.0', mutator methods will be published as named
operations, and in '2.0' and '3.0' they will not.

Let's consider an entry that defines a mutator in the very first
version of the web service and never removes it.

    >>> @exported_as_webservice_entry()
    ... class IBetaMutatorEntry(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value(new_value):
    ...         pass

    >>> @implementer(IBetaMutatorEntry)
    ... class BetaMutator:
    ...     pass

    >>> module = register_test_module(
    ...     'betamutator', IBetaMutatorEntry, BetaMutator)

Here's a helper method that will create a request for a given version.

    >>> from zope.interface import alsoProvides
    >>> def request_for(version):
    ...     request = FakeRequest(version=version)
    ...     marker = getUtility(IWebServiceVersion, name=version)
    ...     alsoProvides(request, marker)
    ...     return request

Here's a helper method that will look up named operation for a given
version.

    >>> from lazr.restful.interfaces import IResourcePOSTOperation
    >>> def operation_for(context, version, name):
    ...     request = request_for(version)
    ...     return getMultiAdapter(
    ...         (context, request), IResourcePOSTOperation, name)

In the 'beta' and '1.0' versions, the lookup succeeds and returns the
generated adapter class defined for 'beta'. These two versions publish
"set_value" as a named POST operation.

    >>> context = BetaMutator()
    >>> operation_for(context, 'beta', 'set_value')
    <lazr.restful.declarations.POST_IBetaMutatorEntry_set_value_beta ...>
    >>> operation_for(context, '1.0', 'set_value')
    <lazr.restful.declarations.POST_IBetaMutatorEntry_set_value_beta ...>

In '2.0', the lookup fails, not because of anything in the definition
of IBetaMutatorEntry, but because the web service configuration
defines 1.0 as the last version in which mutators are published as
named operations.

    >>> operation_for(context, '2.0', 'set_value')
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.interface.interfaces.ComponentLookupError: ...

Here's an entry that defines a mutator method in version 2.0, after
the cutoff point.

    >>> @exported_as_webservice_entry()
    ... class I20MutatorEntry(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     @operation_for_version('2.0')
    ...     def set_value(new_value):
    ...         pass

    >>> @implementer(I20MutatorEntry)
    ... class Mutator20:
    ...     pass

    >>> module = register_test_module(
    ...     'mutator20', I20MutatorEntry, Mutator20)

The named operation lookup never succeeds. In '1.0' it fails because
the mutator hasn't been published yet. In '2.0' it fails because that
version comes after the last one to publish mutators as named
operations ('1.0').

    >>> context = Mutator20()
    >>> operation_for(context, '1.0', 'set_value')
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.interface.interfaces.ComponentLookupError: ...

    >>> operation_for(context, '2.0', 'set_value')
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.interface.interfaces.ComponentLookupError: ...

Edge cases
==========

You can promote a named operation to a mutator operation
--------------------------------------------------------

Here's a named operation that was defined in '1.0' and promoted to a
mutator in '3.0'.

    >>> @exported_as_webservice_entry()
    ... class IOperationPromotedToMutator(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @operation_for_version('3.0')
    ...     @operation_parameters(text=TextLine())
    ...     @export_write_operation()
    ...     @operation_for_version('1.0')
    ...     def set_value(text):
    ...         pass

    >>> @implementer(IOperationPromotedToMutator)
    ... class OperationPromotedToMutator:
    ...
    ...     def __init__(self):
    ...         self.field = None
    ...
    ...     def set_value(self, value):
    ...         self.field = "!" + value + "!"

    >>> module = register_test_module(
    ...     'mutatorpromotion', IOperationPromotedToMutator,
    ...     OperationPromotedToMutator)

    >>> context = OperationPromotedToMutator()

The operation is not available in 'beta', because it hasn't been
defined yet.

    >>> print(operation_for(context, 'beta', 'set_value').__class__.__name__)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.interface.interfaces.ComponentLookupError: ...

The operation is available in both '1.0', and '2.0', even though
mutator operations aren't published as named operations after
1.0. This is because the operation doesn't become a mutator operation
until 3.0.

    >>> print(operation_for(context, '1.0', 'set_value').__class__.__name__)
    POST_IOperationPromotedToMutator_set_value_1_0

    >>> print(operation_for(context, '2.0', 'set_value').__class__.__name__)
    POST_IOperationPromotedToMutator_set_value_1_0

The operation is not available in 3.0, the version in which it becomes
a mutator.

    >>> operation_for(context, '3.0', 'set_value')
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.interface.interfaces.ComponentLookupError: ...

But the mutator is active, as you can see by modifying the entry's field:

    >>> context = OperationPromotedToMutator()
    >>> request_30 = request_for('3.0')
    >>> entry = getMultiAdapter((context, request_30), IEntry)
    >>> entry.field = 'foo'
    >>> print(entry.field)
    !foo!

You can immediately reinstate a mutator operation as a named operation
----------------------------------------------------------------------

This method defines a mutator 'set_value' for version 1.0, which will be
removed in version 2.0. It *also* defines a named operation to be published
as 'set_value' in version 2.0, and a third operation to be published as
'set_value' in version 3.0.

    >>> @exported_as_webservice_entry()
    ... class IMutatorPlusNamedOperationEntry(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     @operation_for_version('1.0')
    ...     def set_value(new_value):
    ...         pass
    ...
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     @export_operation_as('set_value')
    ...     @operation_for_version('2.0')
    ...     def not_a_mutator(new_value):
    ...         pass
    ...
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     @export_operation_as('set_value')
    ...     @operation_for_version('3.0')
    ...     def also_not_a_mutator(new_value):
    ...         pass

    >>> @implementer(IMutatorPlusNamedOperationEntry)
    ... class MutatorPlusNamedOperation:
    ...     pass

    >>> module = register_test_module(
    ...     'multimutator', IMutatorPlusNamedOperationEntry,
    ...     MutatorPlusNamedOperation)

The mutator is accessible for version 1.0, as you'd expect.

    >>> context = MutatorPlusNamedOperation()
    >>> print(operation_for(context, '1.0', 'set_value').__class__.__name__)
    POST_IMutatorPlusNamedOperationEntry_set_value_1_0

The named operations that replace the mutator in versions 2.0 and 3.0 are
also accessible.

    >>> print(operation_for(context, '2.0', 'set_value').__class__.__name__)
    POST_IMutatorPlusNamedOperationEntry_set_value_2_0
    >>> print(operation_for(context, '3.0', 'set_value').__class__.__name__)
    POST_IMutatorPlusNamedOperationEntry_set_value_3_0

So, in the version that gets rid of named operations for mutator methods,
you can immediately define a named operation with the same name as one of
the outgoing mutator methods.

Removing mutator named operations altogether
--------------------------------------------

You can remove this behavior altogether (such that mutators are never
named operations) by setting the value of the configuration variable
'last_version_with_mutator_named_operations' to None.

    >>> config = getUtility(IWebServiceConfiguration)
    >>> config.last_version_with_mutator_named_operations = None

Here's a class identical to IBetaMutatorEntry: it defines a mutator in
the 'beta' version of the web service. (We have to redefine the class
to avoid conflicting registrations.)

    >>> @exported_as_webservice_entry()
    ... class IBetaMutatorEntry2(IBetaMutatorEntry):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value(new_value):
    ...         pass

    >>> @implementer(IBetaMutatorEntry2)
    ... class BetaMutator2:
    ...     pass

    >>> module = register_test_module(
    ...     'betamutator2', IBetaMutatorEntry2, BetaMutator2)

    >>> module = register_test_module(
    ...     'betamutator', IBetaMutatorEntry, BetaMutator)

Back when last_version_with_mutator_named_operations was '1.0', the
'set_value' named operation on IBetaMutatorEntry was accessible in
'beta' but not in '1.0' or later versions. Now, IBetaMutatorEntry2's
'set_value' mutator is not even accessible in 'beta'.

    >>> context = BetaMutator2()
    >>> operation_for(context, 'beta', 'set_value')
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.interface.interfaces.ComponentLookupError: ...

Getting the old behavior back
-----------------------------

You can bring back the old behavior (in which mutators are always
named operations) by setting 'last_version_with_mutator_named_operations'
to the last active version.

    >>> config.last_version_with_mutator_named_operations = (
    ...     config.active_versions[-1])

Again, we have to publish a new entry class, to avoid conflicting
registrations.

    >>> @exported_as_webservice_entry()
    ... class IBetaMutatorEntry3(Interface):
    ...     field = exported(TextLine(readonly=True))
    ...
    ...     @mutator_for(field)
    ...     @export_write_operation()
    ...     @operation_parameters(new_value=TextLine())
    ...     def set_value(new_value):
    ...         pass

    >>> @implementer(IBetaMutatorEntry3)
    ... class BetaMutator3:
    ...     pass

    >>> module = register_test_module(
    ...     'betamutator3', IBetaMutatorEntry3, BetaMutator3)

Back when last_version_with_mutator_named_operations was '1.0', the
'set_value' mutator on IBetaMutatorEntry was not accessible in any
version past '1.0'. Now, the corresponding IBetaMutatorEntry3 mutator
is accessible in every version.

    >>> context = BetaMutator3()
    >>> operation_for(context, 'beta', 'set_value')
    <...POST_IBetaMutatorEntry3_set_value_beta...>
    >>> operation_for(context, '1.0', 'set_value')
    <...POST_IBetaMutatorEntry3_set_value_beta...>
    >>> operation_for(context, '2.0', 'set_value')
    <...POST_IBetaMutatorEntry3_set_value_beta...>
    >>> operation_for(context, '3.0', 'set_value')
    <...POST_IBetaMutatorEntry3_set_value_beta...>

