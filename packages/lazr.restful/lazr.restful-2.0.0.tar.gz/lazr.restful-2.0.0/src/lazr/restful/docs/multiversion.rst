Publishing multiple versions of a web service
*********************************************

A single data model can yield many different lazr.restful web
services. Typically these different services represent successive
versions of a single web service, improved over time.

This test defines three different versions of a web service ('beta',
'1.0', and 'dev'), all based on the same underlying data model.

Setup
=====

First, let's set up the web service infrastructure. Doing this first
will let us create HTTP requests for different versions of the web
service. The first step is to install the common ZCML used by all
lazr.restful web services.

    >>> from zope.configuration import xmlconfig
    >>> zcmlcontext = xmlconfig.string("""
    ... <configure xmlns="http://namespaces.zope.org/zope">
    ...   <include package="lazr.restful" file="basic-site.zcml"/>
    ...   <utility
    ...       factory="lazr.restful.example.base.filemanager.FileManager" />
    ... </configure>
    ... """)

Web service configuration object
--------------------------------

Here's the web service configuration, which defines the three
versions: 'beta', '1.0', and 'dev'.

    >>> from lazr.restful import directives
    >>> from lazr.restful.interfaces import IWebServiceConfiguration
    >>> from lazr.restful.simple import BaseWebServiceConfiguration
    >>> from lazr.restful.testing.webservice import WebServiceTestPublication

    >>> class WebServiceConfiguration(BaseWebServiceConfiguration):
    ...     hostname = 'api.multiversion.dev'
    ...     use_https = False
    ...     active_versions = ['beta', '1.0', 'dev']
    ...     first_version_with_total_size_link = '1.0'
    ...     code_revision = 'test'
    ...     max_batch_size = 100
    ...     view_permission = None
    ...     directives.publication_class(WebServiceTestPublication)

    >>> from grokcore.component.testing import grok_component
    >>> ignore = grok_component(
    ...     'WebServiceConfiguration', WebServiceConfiguration)

    >>> from zope.component import getUtility
    >>> config = getUtility(IWebServiceConfiguration)

Collections previously exposed their total size via a `total_size`
attribute.  However, newer versions of lazr.restful expose a
`total_size_link` intead.  To facilitate transitioning from one
approach to the other the configuration option
`first_version_with_total_size_link` has been added to
IWebServiceConfiguration.

In this case, `first_version_with_total_size_link` is '1.0'. This
means that named operations in versions prior to '1.0' will always
return a `total_size`, but named operations in '1.0' and later
versions will return a `total_size_link` when appropriate.

URL generation
--------------

The URL to an entry or collection is different in different versions
of web service. Not only does every URL includes the version number as
a path element ("http://api.multiversion.dev/1.0/..."), the name or
location of an object might change from one version to another.

We implement this in this example web service by defining ILocation
implementations that retrieve the current browser request and branch
based on the value of request.version. You'll see this in the
ContactSet class.

Here, we tell Zope to use Zope's default AbsoluteURL class for
generating the URLs of objects that implement ILocation. There's no
multiversion-specific code here.

    >>> from zope.component import getSiteManager
    >>> from zope.traversing.browser import AbsoluteURL
    >>> from zope.traversing.browser.interfaces import IAbsoluteURL
    >>> from zope.location.interfaces import ILocation
    >>> from lazr.restful.interfaces import IWebServiceLayer

    >>> sm = getSiteManager()
    >>> sm.registerAdapter(
    ...     AbsoluteURL, (ILocation, IWebServiceLayer),
    ...     provided=IAbsoluteURL)

Defining the request marker interfaces
--------------------------------------

Every version must have a corresponding subclass of
IWebServiceClientRequest. Each interface class is registered as a
named utility implementing IWebServiceVersion. For instance, in the
example below, the I10Version class will be registered as
the IWebServiceVersion utility with the name "1.0".

When a request comes in, lazr.restful figures out which version the
client is asking for, and tags the request with the appropriate marker
interface. The utility registrations make it easy to get the marker
interface for a version, given the version string.

In a real application, these interfaces will be generated and
registered automatically.

    >>> from lazr.restful.interfaces import IWebServiceClientRequest
    >>> class IBetaVersion(IWebServiceClientRequest):
    ...     pass

    >>> class I10Version(IWebServiceClientRequest):
    ...     pass

    >>> class IDevVersion(IWebServiceClientRequest):
    ...     pass

    >>> versions = ((IBetaVersion, 'beta'),
    ...             (I10Version, '1.0'),
    ...             (IDevVersion, 'dev'))

    >>> from lazr.restful import register_versioned_request_utility
    >>> for cls, version in versions:
    ...     register_versioned_request_utility(cls, version)

Example model objects
=====================

Now let's define the data model. The model in webservice.txt is
pretty complicated; this model will be just complicated enough to
illustrate how to publish multiple versions of a web service.

    >>> from zope.interface import Interface, Attribute
    >>> from zope.schema import Bool, Bytes, Int, Text, TextLine, Object

    >>> class IContact(Interface):
    ...     name = TextLine(title="Name", required=True)
    ...     phone = TextLine(title="Phone number", required=True)
    ...     fax = TextLine(title="Fax number", required=False)

Here's an interface for the 'set' object that manages the
contacts.

    >>> from lazr.restful.interfaces import ITraverseWithGet
    >>> class IContactSet(ITraverseWithGet):
    ...     def getAllContacts():
    ...         "Get all contacts."
    ...
    ...     def getContactsWithPhone():
    ...         "Get all contacts that have a phone number."
    ...
    ...     def findContacts(self, string, search_fax):
    ...         """Find contacts by name, phone number, or fax number."""

Here's a simple implementation of IContact.

    >>> from urllib.parse import quote
    >>> from zope.interface import implementer
    >>> from lazr.restful.security import protect_schema
    >>> @implementer(IContact, ILocation)
    ... class Contact:
    ...     def __init__(self, name, phone, fax):
    ...         self.name = name
    ...         self.phone = phone
    ...         self.fax = fax
    ...
    ...     @property
    ...     def __parent__(self):
    ...         return ContactSet()
    ...
    ...     @property
    ...     def __name__(self):
    ...         return self.name
    >>> protect_schema(Contact, IContact)

Here's a simple ContactSet with a predefined list of contacts.

    >>> from operator import attrgetter
    >>> from zope.publisher.interfaces.browser import IBrowserRequest
    >>> from lazr.restful.interfaces import IServiceRootResource
    >>> from lazr.restful.simple import TraverseWithGet
    >>> from lazr.restful.utils import get_current_web_service_request
    >>> @implementer(IContactSet, ILocation)
    ... class ContactSet(TraverseWithGet):
    ...
    ...     def __init__(self):
    ...         self.contacts = CONTACTS
    ...
    ...     def get(self, request, name):
    ...         contacts = [contact for contact in self.contacts
    ...                     if contact.name == name]
    ...         if len(contacts) == 1:
    ...             return contacts[0]
    ...         return None
    ...
    ...     def getAllContacts(self):
    ...         return self.contacts
    ...
    ...     def getContactsWithPhone(self):
    ...         return [contact for contact in self.contacts
    ...                 if contact.phone is not None]
    ...
    ...     def findContacts(self, string, search_fax=True):
    ...          return [contact for contact in self.contacts
    ...                  if (string in contact.name
    ...                      or (contact.phone is not None
    ...                          and string in contact.phone)
    ...                      or (search_fax and string in contact.fax))]
    ...
    ...     @property
    ...     def __parent__(self):
    ...         request = get_current_web_service_request()
    ...         return getUtility(
    ...             IServiceRootResource, name=request.version)
    ...
    ...     @property
    ...     def __name__(self):
    ...         request = get_current_web_service_request()
    ...         if request.version == 'beta':
    ...             return 'contact_list'
    ...         return 'contacts'

    >>> from lazr.restful.security import protect_schema
    >>> protect_schema(ContactSet, IContactSet)

Here are the "model objects" themselves:

    >>> C1 = Contact("Cleo Python", "555-1212", "111-2121")
    >>> C2 = Contact("Oliver Bluth", "10-1000000", "22-2222222")
    >>> C3 = Contact("Fax-your-order Pizza", None, "100-200-300")
    >>> CONTACTS = [C1, C2, C3]

Defining the web service data model
===================================

We've defined an underlying data model (IContact), and now we're going
to define the evolution of a web service through three versions, by
defining three derivative data models. In a real application, these
IEntry subclasses would be generated from lazr.restful decorators
present in IContact but for testing purposes we're going to just
define the three IEntry subclasses manually.

The "beta" version of the web service publishes the IContact interface
exactly as it is defined.

    >>> from lazr.restful.interfaces import IEntry
    >>> class IContactEntry(IEntry):
    ...     """Marker for a contact published through the web service."""

    >>> from zope.interface import taggedValue
    >>> from lazr.restful.interfaces import LAZR_WEBSERVICE_NAME
    >>> class IContactEntryBeta(IContactEntry, IContact):
    ...     """The part of an author we expose through the web service."""
    ...     taggedValue(LAZR_WEBSERVICE_NAME,
    ...                 dict(singular="contact", plural="contacts"))

The "1.0" version publishes the IContact interface as is, but renames
two of the fields.

    >>> class IContactEntry10(IContactEntry):
    ...     name = TextLine(title="Name", required=True)
    ...     phone_number = TextLine(title="Phone number", required=True)
    ...     fax_number = TextLine(title="Fax number", required=False)
    ...     taggedValue(LAZR_WEBSERVICE_NAME,
    ...                 dict(singular="contact", plural="contacts"))

IContactEntry10's "phone_number" and "fax_number" fields correspond to
IContact's 'phone' and 'fax' fields. Since we changed the name, we
must set the tags on the fields object giving the corresponding field
name in IContact. Ordinarily, the lazr.restful declarations take care
of this for us, but here we need to do it ourselves because we're
defining the IEntry classes by hand.

    >>> from lazr.restful.declarations import LAZR_WEBSERVICE_EXPORTED
    >>> IContactEntry10['phone_number'].setTaggedValue(
    ...     LAZR_WEBSERVICE_EXPORTED, dict(original_name="phone"))
    >>> IContactEntry10['fax_number'].setTaggedValue(
    ...     LAZR_WEBSERVICE_EXPORTED, dict(original_name="fax"))

The "dev" version drops the "fax_number" field because fax machines
are obsolete.

    >>> class IContactEntryDev(IContactEntry):
    ...     name = TextLine(title="Name", required=True)
    ...     phone_number = TextLine(title="Phone number", required=True)
    ...     taggedValue(LAZR_WEBSERVICE_NAME,
    ...                 dict(singular="contact", plural="contacts"))
    >>> IContactEntryDev['phone_number'].setTaggedValue(
    ...     LAZR_WEBSERVICE_EXPORTED, dict(original_name="phone"))

Implementing the entry resources
================================

The Contact class defined above implements the IContact interface, but
IContact just describes the data model, not any particular web
service. The IContactEntry subclasses above -- IContactEntryBeta,
IContactEntry10, IContactEntryDev -- describe the three versions of
the web service. Each of these interfaces must be implemented by a
subclass of Entry.

In a real application, the Entry subclasses would be generated from
lazr.restful decorators present in IContact (just like the IEntry
subclasses), but for testing purposes we're going to define the three
Entry subclasses manually.

    >>> from zope.component import adapter
    >>> from zope.interface import implementer
    >>> from lazr.delegates import delegate_to
    >>> from lazr.restful import Entry

    >>> @adapter(IContact)
    ... @implementer(IContactEntryBeta)
    ... @delegate_to(IContactEntryBeta)
    ... class ContactEntryBeta(Entry):
    ...     """A contact, as exposed through the 'beta' web service."""
    ...     schema = IContactEntryBeta
    ...     # This dict is normally generated by lazr.restful, but since we
    ...     # create the adapters manually here, we need to do the same for
    ...     # this dict.
    ...     _orig_interfaces = {
    ...         'name': IContact, 'phone': IContact, 'fax': IContact}
    ...     def __init__(self, context, request):
    ...         self.context = context

    >>> sm.registerAdapter(
    ...     ContactEntryBeta, [IContact, IBetaVersion],
    ...     provided=IContactEntry)

By wrapping one of our predefined Contacts in a ContactEntryBeta
object, we can verify that it implements IContactEntryBeta and
IContactEntry.

    >>> entry = ContactEntryBeta(C1, None)
    >>> IContactEntry.validateInvariants(entry)
    >>> IContactEntryBeta.validateInvariants(entry)

Here's the implemenation of IContactEntry10, which defines Python
properties to implement the different field names.

    >>> @adapter(IContact)
    ... @implementer(IContactEntry10)
    ... @delegate_to(IContactEntry10)
    ... class ContactEntry10(Entry):
    ...     schema = IContactEntry10
    ...     # This dict is normally generated by lazr.restful, but since we
    ...     # create the adapters manually here, we need to do the same for
    ...     # this dict.
    ...     _orig_interfaces = {
    ...         'name': IContact, 'phone_number': IContact,
    ...         'fax_number': IContact}
    ...
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...
    ...     @property
    ...     def phone_number(self):
    ...         return self.context.phone
    ...
    ...     @property
    ...     def fax_number(self):
    ...         return self.context.fax
    >>> sm.registerAdapter(
    ...     ContactEntry10, [IContact, I10Version],
    ...     provided=IContactEntry)

    >>> entry = ContactEntry10(C1, None)
    >>> IContactEntry.validateInvariants(entry)
    >>> IContactEntry10.validateInvariants(entry)

Finally, here's the implementation of IContactEntry for the "dev" version of
the web service.

    >>> @adapter(IContact)
    ... @implementer(IContactEntryDev)
    ... @delegate_to(IContactEntryDev)
    ... class ContactEntryDev(Entry):
    ...     schema = IContactEntryDev
    ...     # This dict is normally generated by lazr.restful, but since we
    ...     # create the adapters manually here, we need to do the same for
    ...     # this dict.
    ...     _orig_interfaces = {'name': IContact, 'phone_number': IContact}
    ...
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...
    ...     @property
    ...     def phone_number(self):
    ...         return self.context.phone
    >>> sm.registerAdapter(
    ...     ContactEntryDev, [IContact, IDevVersion],
    ...     provided=IContactEntry)

    >>> entry = ContactEntryDev(C1, None)
    >>> IContactEntry.validateInvariants(entry)
    >>> IContactEntryDev.validateInvariants(entry)

Looking up the appropriate implementation
=========================================

Because there is no single IEntry implementation for Contact objects,
you can't just adapt Contact to IEntry.

    >>> from zope.component import getAdapter

    >>> getAdapter(C1, IEntry)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.interface.interfaces.ComponentLookupError: ...

When adapting Contact to IEntry you must provide a versioned request
object. The IEntry object you get back will implement the appropriate
version of the web service.

To test this we'll need to manually create some versioned request
objects. The traversal process would take care of this for us (see
"Request lifecycle" below), but it won't work yet because we have yet
to define a service root resource.

    >>> from lazr.restful.testing.webservice import (
    ...     create_web_service_request)
    >>> from zope.interface import alsoProvides

    >>> from zope.component import getMultiAdapter
    >>> request_beta = create_web_service_request('/beta/')
    >>> alsoProvides(request_beta, IBetaVersion)
    >>> beta_entry = getMultiAdapter((C1, request_beta), IEntry)
    >>> print(beta_entry.fax)
    111-2121

    >>> request_10 = create_web_service_request('/1.0/')
    >>> alsoProvides(request_10, I10Version)
    >>> one_oh_entry = getMultiAdapter((C1, request_10), IEntry)
    >>> print(one_oh_entry.fax_number)
    111-2121

    >>> request_dev = create_web_service_request('/dev/')
    >>> alsoProvides(request_dev, IDevVersion)
    >>> dev_entry = getMultiAdapter((C1, request_dev), IEntry)
    >>> print(dev_entry.fax)
    Traceback (most recent call last):
    ...
    AttributeError: 'ContactEntryDev' object has no attribute 'fax'

Implementing the collection resource
====================================

The set of contacts publishes a slightly different named operation in
every version of the web service, so in a little bit we'll be
implementing three different versions of the same named operation. The
contact set itself also changes between versions. In the 'beta' and
'1.0' versions, the contact set serves all contcts. In the 'dev'
version, the contact set omits contacts that only have a fax
number. We'll implement this behavior by implementing ICollection
twice and registering each implementation for the appropriate versions
of the web service.

    >>> from lazr.restful import Collection
    >>> from lazr.restful.interfaces import ICollection

First we'll implement the version used in 'beta' and '1.0'.

    >>> @adapter(IContactSet)
    ... class ContactCollectionBeta(Collection):
    ...     """A collection of contacts, exposed through the web service."""
    ...
    ...     entry_schema = IContactEntry
    ...
    ...     def find(self):
    ...        """Find all the contacts."""
    ...        return self.context.getAllContacts()

Let's make sure it implements ICollection.

    >>> from zope.interface.verify import verifyObject
    >>> contact_set = ContactSet()
    >>> verifyObject(ICollection, ContactCollectionBeta(contact_set, None))
    True

Register it as the ICollection adapter for IContactSet in
IBetaVersion and I10Version.

    >>> for version in [IBetaVersion, I10Version]:
    ...     sm.registerAdapter(
    ...         ContactCollectionBeta, [IContactSet, version],
    ...         provided=ICollection)

Make sure the functionality works properly.

    >>> collection = getMultiAdapter(
    ...     (contact_set, request_beta), ICollection)
    >>> len(collection.find())
    3

    >>> collection = getMultiAdapter(
    ...     (contact_set, request_10), ICollection)
    >>> len(collection.find())
    3

Now let's implement the different version used in 'dev'.

    >>> class ContactCollectionDev(ContactCollectionBeta):
    ...     def find(self):
    ...         """Find all the contacts, sorted by name."""
    ...         return self.context.getContactsWithPhone()

This class also implements ICollection.

    >>> verifyObject(ICollection, ContactCollectionDev(contact_set, None))
    True

Register it as the ICollection adapter for IContactSet in
IDevVersion.

    >>> sm.registerAdapter(
    ...         ContactCollectionDev, [IContactSet, IDevVersion],
    ...         provided=ICollection)

Make sure the functionality works properly. Note that the contact that
only has a fax number no longer shows up.

    >>> collection = getMultiAdapter(
    ...     (contact_set, request_dev), ICollection)
    >>> [contact.name for contact in collection.find()]
    ['Cleo Python', 'Oliver Bluth']

Implementing the named operations
---------------------------------

All three versions of the web service publish a named operation for
searching for contacts, but they publish it in slightly different
ways. In 'beta' it publishes a named operation called 'findContacts',
which does a search based on name, phone number, and fax number. In
'1.0' it publishes the same operation, but the name is
'find'. In 'dev' the contact set publishes 'find',
but the functionality is changed to search only the name and phone
number.

Here's the named operation as implemented in versions 'beta' and '1.0'.

    >>> from lazr.restful import ResourceGETOperation
    >>> from lazr.restful.fields import CollectionField, Reference
    >>> from lazr.restful.interfaces import IResourceGETOperation
    >>> @implementer(IResourceGETOperation)
    ... class FindContactsOperationBase(ResourceGETOperation):
    ...    """An operation that searches for contacts."""
    ...
    ...    params = [ TextLine(__name__='string') ]
    ...    return_type = CollectionField(value_type=Reference(schema=IContact))
    ...
    ...    def call(self, string):
    ...        try:
    ...            return self.context.findContacts(string)
    ...        except ValueError as e:
    ...            self.request.response.setStatus(400)
    ...            return str(e)

This operation is registered as the "findContacts" operation in the
'beta' service, and the 'find' operation in the '1.0' service.

    >>> sm.registerAdapter(
    ...     FindContactsOperationBase, [IContactSet, IBetaVersion],
    ...     provided=IResourceGETOperation, name="findContacts")

    >>> sm.registerAdapter(
    ...     FindContactsOperationBase, [IContactSet, I10Version],
    ...     provided=IResourceGETOperation, name="find")

Here's the slightly different named operation as implemented in
version 'dev'.

    >>> class FindContactsOperationNoFax(FindContactsOperationBase):
    ...    """An operation that searches for contacts."""
    ...
    ...    def call(self, string):
    ...        try:
    ...            return self.context.findContacts(string, False)
    ...        except ValueError as e:
    ...            self.request.response.setStatus(400)
    ...            return str(e)

    >>> sm.registerAdapter(
    ...     FindContactsOperationNoFax, [IContactSet, IDevVersion],
    ...     provided=IResourceGETOperation, name="find")

The service root resource
=========================

To make things more interesting we'll define two distinct service
roots. The 'beta' web service will publish the contact set as
'contact_list', and subsequent versions will publish it as 'contacts'.

    >>> from lazr.restful.simple import RootResource
    >>> from zope.traversing.browser.interfaces import IAbsoluteURL

    >>> @implementer(IAbsoluteURL)
    ... class BetaServiceRootResource(RootResource):
    ...     top_level_collections = {
    ...         'contact_list': (IContact, ContactSet()) }

    >>> @implementer(IAbsoluteURL)
    ... class PostBetaServiceRootResource(RootResource):
    ...     top_level_collections = {
    ...         'contacts': (IContact, ContactSet()) }

    >>> for version, cls in (('beta', BetaServiceRootResource),
    ...                      ('1.0', PostBetaServiceRootResource),
    ...                      ('dev', PostBetaServiceRootResource)):
    ...     app = cls()
    ...     sm.registerUtility(app, IServiceRootResource, name=version)

    >>> beta_app = getUtility(IServiceRootResource, 'beta')
    >>> dev_app = getUtility(IServiceRootResource, 'dev')

    >>> beta_app.top_level_names
    ['contact_list']

    >>> dev_app.top_level_names
    ['contacts']

Both classes will use the default lazr.restful code to generate their
URLs.

    >>> from zope.traversing.browser import absoluteURL
    >>> from lazr.restful.simple import RootResourceAbsoluteURL
    >>> for cls in (BetaServiceRootResource, PostBetaServiceRootResource):
    ...     sm.registerAdapter(
    ...         RootResourceAbsoluteURL, [cls, IBrowserRequest])

    >>> beta_request = create_web_service_request('/beta/')
    >>> print(beta_request.traverse(None))
    <BetaServiceRootResource object...>

    >>> print(absoluteURL(beta_app, beta_request))
    http://api.multiversion.dev/beta/

    >>> dev_request = create_web_service_request('/dev/')
    >>> print(dev_request.traverse(None))
    <PostBetaServiceRootResource object...>

    >>> print(absoluteURL(dev_app, dev_request))
    http://api.multiversion.dev/dev/

Request lifecycle
=================

When a request first comes in, there's no way to tell which version
it's associated with.

    >>> from lazr.restful.testing.webservice import (
    ...     create_web_service_request)

    >>> request_beta = create_web_service_request('/beta/')
    >>> IBetaVersion.providedBy(request_beta)
    False

The traversal process associates the request with a particular version.

    >>> request_beta.traverse(None)
    <BetaServiceRootResource object ...>
    >>> IBetaVersion.providedBy(request_beta)
    True
    >>> print(request_beta.version)
    beta

Using the web service
=====================

Now that we can create versioned web service requests, let's try out
the different versions of the web service.

Beta
----

Here's the service root resource.

    >>> import simplejson
    >>> request = create_web_service_request('/beta/')
    >>> resource = request.traverse(None)
    >>> body = simplejson.loads(resource())
    >>> print(sorted(body.keys()))
    ['contacts_collection_link', 'resource_type_link']

    >>> print(body['contacts_collection_link'])
    http://api.multiversion.dev/beta/contact_list

Here's the contact list.

    >>> request = create_web_service_request('/beta/contact_list')
    >>> resource = request.traverse(None)

We can't access the underlying data model object through the request,
but since we happen to know which object it is, we can pass it into
absoluteURL along with the request object, and get the correct URL.

    >>> print(absoluteURL(contact_set, request))
    http://api.multiversion.dev/beta/contact_list

    >>> body = simplejson.loads(resource())
    >>> body['total_size']
    3
    >>> for link in sorted(
    ...     [contact['self_link'] for contact in body['entries']]):
    ...     print(link)
    http://api.multiversion.dev/beta/contact_list/Cleo%20Python
    http://api.multiversion.dev/beta/contact_list/Fax-your-order%20Pizza
    http://api.multiversion.dev/beta/contact_list/Oliver%20Bluth

We can traverse through the collection to an entry.

    >>> request_beta = create_web_service_request(
    ...     '/beta/contact_list/Cleo Python')
    >>> resource = request_beta.traverse(None)

Again, we can't access the underlying data model object through the
request, but since we know which object represents Cleo Python, we can
pass it into absoluteURL along with this request object, and get the
object's URL.

    >>> print(C1.name)
    Cleo Python
    >>> print(absoluteURL(C1, request_beta))
    http://api.multiversion.dev/beta/contact_list/Cleo%20Python

    >>> from collections import OrderedDict
    >>> body = simplejson.loads(resource(), object_pairs_hook=OrderedDict)
    >>> list(body)
    ['self_link', 'resource_type_link', 'name', 'phone', 'fax', 'http_etag']
    >>> print(body['name'])
    Cleo Python

We can traverse through an entry to one of its fields.

    >>> request_beta = create_web_service_request(
    ...     '/beta/contact_list/Cleo Python/fax')
    >>> field = request_beta.traverse(None)
    >>> print(simplejson.loads(field()))
    111-2121

We can invoke a named operation, and it returns a total_size (because
'beta' is an earlier version than the
first_version_with_total_size_link).

    >>> import simplejson
    >>> request_beta = create_web_service_request(
    ...     '/beta/contact_list',
    ...     environ={'QUERY_STRING' : 'ws.op=findContacts&string=Cleo'})
    >>> operation = request_beta.traverse(None)
    >>> result = simplejson.loads(operation())
    >>> [contact['name'] for contact in result['entries']]
    ['Cleo Python']

    >>> result['total_size']
    1

    >>> request_beta = create_web_service_request(
    ...     '/beta/contact_list',
    ...     environ={'QUERY_STRING' : 'ws.op=findContacts&string=111'})

    >>> operation = request_beta.traverse(None)
    >>> result = simplejson.loads(operation())
    >>> [contact['fax'] for contact in result['entries']]
    ['111-2121']

1.0
---

Here's the service root resource.

    >>> import simplejson
    >>> request = create_web_service_request('/1.0/')
    >>> resource = request.traverse(None)
    >>> body = simplejson.loads(resource())
    >>> print(sorted(body.keys()))
    ['contacts_collection_link', 'resource_type_link']

Note that 'contacts_collection_link' points to a different URL in
'1.0' than in 'dev'.

    >>> print(body['contacts_collection_link'])
    http://api.multiversion.dev/1.0/contacts

An attempt to use the 'beta' name of the contact list in the '1.0' web
service will fail.

    >>> request = create_web_service_request('/1.0/contact_list')
    >>> resource = request.traverse(None)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: Object: <PostBetaServiceRootResource...>, name: ...'contact_list'

Here's the contact list under its correct URL.

    >>> request = create_web_service_request('/1.0/contacts')
    >>> resource = request.traverse(None)
    >>> print(absoluteURL(contact_set, request))
    http://api.multiversion.dev/1.0/contacts

    >>> body = simplejson.loads(resource())
    >>> body['total_size']
    3
    >>> for link in sorted(
    ...     [contact['self_link'] for contact in body['entries']]):
    ...     print(link)
    http://api.multiversion.dev/1.0/contacts/Cleo%20Python
    http://api.multiversion.dev/1.0/contacts/Fax-your-order%20Pizza
    http://api.multiversion.dev/1.0/contacts/Oliver%20Bluth

We can traverse through the collection to an entry.

    >>> request_10 = create_web_service_request(
    ...     '/1.0/contacts/Cleo Python')
    >>> resource = request_10.traverse(None)
    >>> print(absoluteURL(C1, request_10))
    http://api.multiversion.dev/1.0/contacts/Cleo%20Python

Note that the 'fax' and 'phone' fields are now called 'fax_number' and
'phone_number'.

    >>> body = simplejson.loads(resource(), object_pairs_hook=OrderedDict)
    >>> list(body)
    ['self_link', 'resource_type_link', 'name', 'phone_number', 'fax_number',
     'http_etag']
    >>> print(body['name'])
    Cleo Python

We can traverse through an entry to one of its fields.

    >>> request_10 = create_web_service_request(
    ...     '/1.0/contacts/Cleo Python/fax_number')
    >>> field = request_10.traverse(None)
    >>> print(simplejson.loads(field()))
    111-2121

The fax field in '1.0' is called 'fax_number', and attempting
to traverse to its 'beta' name ('fax') will fail.

    >>> request_10 = create_web_service_request(
    ...     '/1.0/contacts/Cleo Python/fax')
    >>> field = request_10.traverse(None)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: Object: <Contact object...>, name: ...'fax'

We can invoke a named operation. Note that the name of the operation
is now 'find' (it was 'findContacts' in 'beta'). And note that
total_size has been replaced by total_size_link, since '1.0' is the
first_version_with_total_size_link.

    >>> request_10 = create_web_service_request(
    ...     '/1.0/contacts',
    ...     environ={'QUERY_STRING' : 'ws.op=find&string=e&ws.size=2'})
    >>> operation = request_10.traverse(None)
    >>> result = simplejson.loads(operation())
    >>> [contact['name'] for contact in result['entries']]
    ['Cleo Python', 'Oliver Bluth']

    >>> result['total_size']
    Traceback (most recent call last):
    ...
    KeyError: 'total_size'

    >>> print(result['total_size_link'])
    http://.../1.0/contacts?string=e&ws.op=find&ws.show=total_size
    >>> size_request = create_web_service_request(
    ...     '/1.0/contacts',
    ...     environ={'QUERY_STRING' :
    ...         'string=e&ws.op=find&ws.show=total_size'})
    >>> operation = size_request.traverse(None)
    >>> result = simplejson.loads(operation())
    >>> print(result)
    3

If the resultset fits on a single page, total_size will be provided
instead of total_size_link, as a convenience.

    >>> request_10 = create_web_service_request(
    ...     '/1.0/contacts',
    ...     environ={'QUERY_STRING' : 'ws.op=find&string=111'})
    >>> operation = request_10.traverse(None)
    >>> result = simplejson.loads(operation())
    >>> [contact['fax_number'] for contact in result['entries']]
    ['111-2121']
    >>> result['total_size']
    1

Attempting to invoke the operation using its 'beta' name won't work.

    >>> request_10 = create_web_service_request(
    ...     '/1.0/contacts',
    ...     environ={'QUERY_STRING' : 'ws.op=findContacts&string=Cleo'})
    >>> operation = request_10.traverse(None)
    >>> print(operation())
    No such operation: findContacts

Dev
---

Here's the service root resource.

    >>> request = create_web_service_request('/dev/')
    >>> resource = request.traverse(None)
    >>> body = simplejson.loads(resource())
    >>> print(sorted(body.keys()))
    ['contacts_collection_link', 'resource_type_link']

    >>> print(body['contacts_collection_link'])
    http://api.multiversion.dev/dev/contacts

Here's the contact list.

    >>> request_dev = create_web_service_request('/dev/contacts')
    >>> resource = request_dev.traverse(None)
    >>> print(absoluteURL(contact_set, request_dev))
    http://api.multiversion.dev/dev/contacts

    >>> body = simplejson.loads(resource())
    >>> body['total_size']
    2
    >>> for link in sorted(
    ...     [contact['self_link'] for contact in body['entries']]):
    ...     print(link)
    http://api.multiversion.dev/dev/contacts/Cleo%20Python
    http://api.multiversion.dev/dev/contacts/Oliver%20Bluth

We can traverse through the collection to an entry.

    >>> request_dev = create_web_service_request(
    ...     '/dev/contacts/Cleo Python')
    >>> resource = request_dev.traverse(None)
    >>> print(absoluteURL(C1, request_dev))
    http://api.multiversion.dev/dev/contacts/Cleo%20Python

Note that the published field names have changed between 'dev' and
'1.0'. The phone field is still 'phone_number', but the 'fax_number'
field is gone.

    >>> body = simplejson.loads(resource(), object_pairs_hook=OrderedDict)
    >>> list(body)
    ['self_link', 'resource_type_link', 'name', 'phone_number', 'http_etag']
    >>> print(body['name'])
    Cleo Python

We can traverse through an entry to one of its fields.

    >>> request_dev = create_web_service_request(
    ...     '/dev/contacts/Cleo Python/name')
    >>> field = request_dev.traverse(None)
    >>> print(simplejson.loads(field()))
    Cleo Python

We cannot use 'dev' to traverse to a field not published in the 'dev'
version.

    >>> request_beta = create_web_service_request(
    ...     '/dev/contacts/Cleo Python/fax')
    >>> field = request_beta.traverse(None)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: Object: <Contact object...>, name: ...'fax'

    >>> request_beta = create_web_service_request(
    ...     '/dev/contacts/Cleo Python/fax_number')
    >>> field = request_beta.traverse(None)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: Object: <Contact object...>, name: ...'fax_number'

We can invoke a named operation.

    >>> request_dev = create_web_service_request(
    ...     '/dev/contacts',
    ...     environ={'QUERY_STRING' : 'ws.op=find&string=Cleo'})
    >>> operation = request_dev.traverse(None)
    >>> result = simplejson.loads(operation())
    >>> [contact['name'] for contact in result['entries']]
    ['Cleo Python']

Note that a search for Cleo's fax number no longer finds anything,
because the named operation published as 'find' in the 'dev' web
service doesn't search the fax field.

    >>> request_dev = create_web_service_request(
    ...     '/dev/contacts',
    ...     environ={'QUERY_STRING' : 'ws.op=find&string=111'})
    >>> operation = request_dev.traverse(None)
    >>> result = simplejson.loads(operation())
    >>> [entry for entry in result['entries']]
    []
