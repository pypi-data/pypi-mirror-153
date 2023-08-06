=====================
NEWS for lazr.restful
=====================

2.0.0 (2022-06-01)
==================

- Drop Python 2 support.
- Add support for Python 3.9 and 3.10.
- Add basic pre-commit configuration.
- Publish docs on Read the Docs.
- Apply inclusive naming via the woke pre-commit hook. The following API
  changes were performed:
  ``lazr.restful.metazcml.webservice_sanity_checks``
  => ``lazr.restful.metazcml.webservice_coherence_checks``,
  ``lazr.restful.testing.webservice.DummyURL``
  => ``lazr.restful.testing.webservice.StubAbsoluteURL``,
  ``lazr.restful.testing.webservice.DummyAbsoluteURL``
  => ``lazr.restful.testing.webservice.StubAbsoluteURL``,
  ``lazr.restful.testing.webservice.DummyRootResourceURL``
  => ``lazr.restful.testing.webservice.StubRootResourceURL``
- Apply black code formatter via pre-commit.
- Remove ``export_as_webservice_entry`` and
  ``export_as_webservice_collection``; these were deprecated in 0.22.0 and
  cannot work on Python 3.  Use the class decorators
  ``@exported_as_webservice_entry`` and
  ``@exported_as_webservice_collection`` instead.
- Deprecate ``lazr.restful.utils.safe_hasattr``, since Python's builtin
  ``hasattr`` is fixed as of Python 3.2.
- The collection marshallers (list, set, tuple) will now correctly
  unmarshall ``None`` as ``None``.

1.1.0 (2021-10-07)
==================

- Add a new ``@scoped`` decorator to ``lazr.restful.declarations``, allowing
  applications to tag methods with scope names and issue authentication
  tokens constrained to only be able to call methods with particular scopes.
  Scoped requests cannot currently use attributes, accessors, or mutators;
  this may change in future.

1.0.4 (2021-09-13)
==================

- Adjust versioning strategy to avoid importing pkg_resources, which is slow
  in large environments.

1.0.3 (2021-05-20)
==================

Give ``DateTimeFieldMarshaller`` an ``unmarshall`` method, rather than
special-casing it elsewhere.

Generate stable ETags for dict fields.

Use a stable ordering for fields in entry representations.

Stabilize ETags of entries containing collections of strings between Python
2 and 3 (bug 1928474).

Add an ``IJSONPublishable`` adapter for ``date`` and ``datetime``.

1.0.2 (2021-05-14)
==================

Avoid traceback reference cycle in ``ReadWriteResource.__call__``.

1.0.1 (2021-02-18)
==================

Preserve specified parameter ordering in ``export_factory_operation`` and
``BaseResourceOperationAdapter``.  This can make a difference when creating
objects, by ensuring that validators are called in the correct order.

1.0.0 (2021-01-21)
==================

Rework ``lazr.restful.testing.webservice.WebServiceCaller`` to send named
POSTs as ``multipart/form-data`` requests.  Arguments that are instances of
``io.BufferedIOBase`` are sent as-is rather than being encoded as JSON,
allowing robust use of binary arguments on both Python 2 and 3
(bug 1116954).

Normalize line breaks in text fields marshalled from a request to Unix-style
LF, since ``multipart/form-data`` encoding requires CRLF.

Make ``lazr.restful.testing.webservice.pprint_entry`` and
``lazr.restful.testing.webservice.pprint_collection`` recurse into lists in
order to print text string representations in the Python 3 style.

Require zope.publisher >= 6.0.0 on Python 3.

Make ``lazr.restful.testing.helpers.encode_unicode`` return ``str`` on
Python 3.

Sort fields in HTML views of entries by name.

Don't attempt to JSON-decode ``Bytes`` fields read from a request, since
binary data can't be marshalled via JSON without additional encoding that we
don't do, and ``lazr.restfulclient`` doesn't JSON-encode binary fields.

Declare support for Python 3.

0.23.0 (2020-09-28)
===================

Change ``lazr.restful.testing.webservice.pprint_entry`` and
``lazr.restful.testing.webservice.pprint_collection`` to print text string
representations in the Python 3 style (``'text'`` rather than ``u'text'``)
on both Python 2 and 3.  This makes it easier to write bilingual doctests,
although existing callers need to change.

Stop ``lazr.restful.utils.make_identifier_safe`` having locale-dependent
behaviour.

Remove ``lazr.restful.utils.safe_js_escape``.  Launchpad hasn't used it
since 2012, and it was a confusing interface in that it combined JavaScript
and HTML escaping.  If any code is still using this, it should use
``cgi.escape``/``html.escape`` (if necessary) and ``json.dumps`` directly
instead.

Some more Python 3 porting work, still not yet complete.

0.22.2 (2020-09-02)
===================

Fix dereferencing of URLs that redirect within HTTPS requests.

Some more Python 3 porting work, still not yet complete.

0.22.1 (2020-07-08)
===================

Fix test failure with zope.interface >= 5.0.0.

Make ``ObjectLookupFieldMarshaller`` accept URLs that redirect, provided
that the redirected-to resource has a ``context`` attribute that evaluates
to the appropriate model object.

0.22.0 (2020-06-12)
===================

Set a different ETag when serving WADL for different revisions of the web
service (bug 1875917).

Deprecate the "class advice" APIs from ``lazr.restful.declarations``:
``export_as_webservice_entry`` and ``export_as_webservice_collection``.  In
their place, prefer the equivalent class decorators:
``@exported_as_webservice_entry`` and
``@exported_as_webservice_collection``.  The functions based on class advice
will not work on Python 3.

0.21.1 (2020-02-19)
===================

Only require the separate wsgiref package on Python 2.

Remove epydoc dependency, incorporating the relevant code directly.

Allow newer versions of grokcore.component and martian rather than pinning
exact (and old) versions.

Some miscellaneous Python 3 porting work, not yet complete.

0.21.0 (2019-12-17)
===================

Fix IDjangoLocation for compatibility with zope.traversing >= 3.13, which
only adapts objects to ILocation if they do not have a __parent__ attribute.
Objects implementing IDjangoLocation must now have a __parent_object__
attribute instead of __parent__.

Fix double closing brace when encoding the result of a custom operation
where the result has an adapter to ICollection.

Generate IEntry subinterfaces with field ordering matching that in the
original interface.

Fixed bug 1803564: Values from requests that contain only whitespace are now
interpreted correctly.

Remove limitation on immediately reinstating a named operation with the same
name as a mutator in the webservice version that gets rid of named
operations for mutator methods.  (This was previously only unreliably
enforced in any case, as it depended on the order of methods returned by
zope.interface.Interface.namesAndDescriptions.)

Fix test failures with zope.configuration >= 4.3.0.

Fix test failures with Python >= 2.7.17 (or backported fixes for
CVE-2019-9740).

Import ComponentLookupError from zope.interface.interfaces rather than
zope.component.interfaces, fixing a deprecation warning.

Switch from buildout to tox.

Remove dependency on zope.app.pagetemplate.  Explicitly depend on
zope.datetime, which was previously only pulled in indirectly.

0.20.1 (2018-02-21)
===================

Adjust docstring rendering to avoid closing sys.stdout when running under
"zope.testrunner --subunit" with docutils >= 0.8.

0.20.0 (2017-06-29)
===================

Fixed bug 1294543: contributes_to can now reference interfaces in other
modules and webservice:register directives.

Switch zope.interface, zope.component, and lazr.delegates users from class
advice to class decorators.

Restrict find_exported_interfaces to names that would ordinarily be
considered to be exported from a module.

0.19.10 (2012-12-06)
====================

Fixed bug 809863: WebServicePublicationMixin.getResource() converts
ComponentLookupErrors to NotFound.

0.19.9 (2012-10-23)
===================

Fixed bug 924291: The FixedVocabularyFieldMarshaller will now correctly return
the entire vocabulary if the value passed in is None.

0.19.8 (2012-10-02)
===================

Fixed bug 1020439: The dict marshaller will now correctly unmarshall None.

0.19.7 (2012-09-26)
===================

Fixed bug 1056666: make named operations which result in a resource URL change
issue a 301 response containing the new location.

0.19.6 (2012-03-15)
===================

Fixed bug 955668: make marshallers work correctly for  collection fields
(Set, List, Dict) where the key and/or value types have not been specified.
In such cases, the default marshaller is used for the collection elements.

0.19.5 (2012-03-13)
===================

Fixed bug 953587: add a dict marshaller so that exported method parameters
can be of type dict.

0.19.4 (2011-10-11)
===================

Fixed bug 871944: a successful write with an If-Match would sometimes
return stale values.

0.19.3 (2011-09-20)
===================

Fixed bug 854695: exceptions with no __traceback__ attribute would cause an
AttributeError

0.19.2 (2011-09-08)
===================

Fixed bug 842917: multiple values for ws.op in a request would generate a
TypeError

0.19.1 (2011-09-08)
===================

Fixed bug 832136: original tracebacks were being obscured when exceptions are
reraised.

0.19.0 (2011-07-27)
===================

A new decorator, @accessor_for, has been added to
lazr.restful.declarations. This makes it possible to export a method
with bound variables as an accessor for an attribute.

0.18.1 (2011-04-01)
===================

Fixed minor test failures.

The object modification event will not be fired if a client sends an
empty changeset via PATCH.

The webservice may define an adapter which is used, after an operation on a
resource, to provide notifications consisting of namedtuples (level, message).
Any notifications are json encoded and inserted into the response header using
the 'X-Lazr-Notification' key. They may then be used by the caller to provide
extra information to the user about the completed request.

The webservice:json TALES function now returns JSON that will survive
HTML escaping.

0.18.0 (2011-03-23)
===================

If the configuration variable `require_explicit_versions` is set,
lazr.restful will not load up a web service unless every field, entry,
and named operation explicitly states which version of the web service
it first appears in.

0.17.5 (2011-03-15)
===================

When a view is registered for an exception, but the view contains no
information that's useful to lazr.restful, re-raise the exception
instead of trying to render the view.

0.17.4 (2011-03-08)
===================

Reverted the client cache representations to JSON-only. Call sites need to
escape the JSON_PLUS_XHTML_TYPE representation which may require
JSONEncoderForHTML or declaring the the script as CDATA.

0.17.3 (2011-03-08)
===================

Fixed a bug in exception handling when the associated response code is
in the 4xx series.

0.17.2 (2011-03-03)
===================

Several of the techniques for associating an exception with an HTTP
response code were not working at all. Fixed them.

0.17.1 (2011-02-23)
===================

Add a new test to the testsuite.

0.17.0 (2011-02-17)
===================

Added the ability to get a combined JSON/HTML representation of an
entry that has custom HTML representations for some of its fields.

0.16.1 (2011-02-16)
===================

Fixed a bug that prevented a write operation from being promoted to a
mutator operation.

0.16.0 (No official release)
============================

If each entry in the web service corresponds to some object on a
website, and there's a way of converting a web service request into a
website request, the web service will now provide website links for
each entry.

You can suppress the website link for a particular entry class by
passing publish_web_link=False into export_as_webservice_entry().

Validation errors for named operations will be properly sent to the
client even if they contain Unicode characters. (Launchpad bug 619180.)

0.15.4 (2011-01-26)
===================

Fixed inconsistent handling of custom HTML field renderings. An
IFieldHTMLRenderer can now return either Unicode or UTF-8.

0.15.3 (2011-01-21)
===================

lazr.restful will now complain if you try to export an IObject, as
this causes infinite recursion during field validation. We had code
that worked around the infinite recursion, but it wasn't reliable and
we've now removed it to simplify. Use IReference whenever you would
use IObject.


0.15.2 (2011-01-20)
===================

lazr.restful gives a more helpful error message when a published
interface includes a reference to an unpublished interface. (Launchpad
bug 539070)

lazr.restful's tests now pass in Python 2.7. (Launchpad bug 691841)

0.15.1 (2011-01-19)
===================

Fixed a redirect bug when a web browser requests a representation
other than JSON.

Removed overzealous error checking that was causing problems for
browsers such as Chromium. (Launchpad bug 423149.)

0.15.0 (2010-11-30)
===================

Added an optimization to the WADL docstring handling that results in a 30%
decrease in WADL generation time for large files.

0.14.1 (2010-10-24)
===================

Fixed a unicode encoding bug that precluded reporting exceptions with
non-ASCII characters.

0.14.0 (2010-10-05)
===================

Rework ETag generation to be less conservative (an optimization).

0.13.3 (2010-09-29)
===================

Named operations that take URLs as arguments will now accept URLs
relative to the versioned service root. Previously they would only
accept absolute URLs. PUT and PATCH requests will also accept relative
URLs. This fixes bug 497602.

0.13.2 (2010-09-27)
===================

Avoided an error when looking at a Location header that contains
characters not valid in URIs. (An error will probably still happen,
but having it happen in lazr.restful was confusing people.)

0.13.1 (2010-09-23)
===================

Removed a Python 2.6-ism to restore compatibility with Python 2.5.

0.13.0 (2010-09-06)
===================

Add the ability to annotate an exception so the client will be given the
exception message as the HTTP body of the response.

0.12.1 (2010-09-02)
===================

Make WADL generation more deterministic.

0.12.0 (2010-08-26)
===================

Added the ability to take a read-write field and publish it as
read-only through the web service.

0.11.2 (2010-08-23)
===================

Optimized lazr.restful to send 'total_size' instead of
'total_size_link' when 'total_size' is easy to calculate, possibly
saving the client from sending another HTTP request.

0.11.1 (2010-08-13)
===================

Fixed a bug that prevented first_version_with_total_size_link from
working properly in a multi-version environment.

0.11.0 (2010-08-10)
===================

Added an optimization to total_size so that it is fetched via a link when
possible.  The new configuration option first_version_with_total_size_link
specifies what version should be the first to expose the behavior.  The default
is for it to be enabled for all versions so set this option to preserve the
earlier behavior for previously released web services.

0.10.0 (2010-08-05)
===================

Added the ability to mark interface A as a contributor to interface B so that
instead of publishing A separately we will add all of A's fields and
operations to the published version of B. Objects implementing B must be
adaptable into A for this to work, but lazr.restful will take care of doing
the actual adaptation before accessing fields/operations that are not directly
provided by an object.

0.9.29 (2010-06-14)
===================

Added invalidation code for the representation cache on events
generated by lazr.restful itself. Made the cache more robust and fixed
a bug where it would totally redact a forbidden representation rather
than simply refuse to serve it. Made it possible for a cache to refuse
to cache an object for any reason.

0.9.28 (2010-06-03)
===================

Special note: This version adds a new configuration element,
'enable_server_side_representation_cache'. This lets you turn the
representation cache on and off at runtime without unregistering the
cache utility.

Fixed some test failures.

0.9.27 (2010-06-01)
====================

Added the ability to define a representation cache used to store the
JSON representations of entry resources, rather than building them
from scratch every time. Although the cache has hooks for
invalidation, lazr.restful will never invalidate any part of the cache
on its own. You need to hook lazr.restful's invalidation code into
your ORM or other data store.

0.9.26 (2010-05-18)
===================

Special note: This version adds a new configuration element,
'compensate_for_mod_compress_etag_modification'. If you are running
lazr.restful behind an Apache server, setting this configuration
element will make mod_compress work properly with lazr.restful. This
is not a permanent solution: a better solution will be available when
Apache bug 39727 is fixed.

Special note: This version removes the configuration element
'set_hop_to_hop_headers'. You can still define this element in your
configuration, but it will have no effect.

Removed code that handles compression through hop-to-hop
headers. We've never encountered a real situation in which these
headers were useful. Compression can and should be handled by
intermediaries such as mod_compress. (Unfortunately, mod_compress has
its own problems, which this release tries to work around.)

0.9.25 (2010-04-14)
===================

Special note: This version introduces a new configuration element,
'caching_policy'. This element starts out simple but may become more
complex in future versions. See the IWebServiceConfiguration interface
for more details.

Service root resources are now client-side cacheable for an amount of
time that depends on the server configuration and the version of the
web service requested. To get the full benefit, clients will need to
upgrade to lazr.restfulclient 0.9.14.

When a PATCH or PUT request changes multiple fields at once, the
changes are applied in a deterministic order designed to minimize
possible conflicts.

0.9.24 (2010-03-17)
====================

Entry resources will now accept conditional PATCH requests even if one
of the resource's read-only fields has changed behind the scenes
recently.

0.9.23 (2010-03-11)
===================

There are two new attributes of the web service configuration,
"service_description" and "version_descriptions". Both are optional,
but they're useful for giving your users an overview of your web
service and of the differences between versions.

0.9.22 (2010-03-05)
===================

Special note: this version will break backwards compatibility in your
web service unless you take a special step. See
"last_version_with_named_mutator_operations" below.

Refactored the code that tags request objects with version
information, so that tagging would happen consistently.

By default, mutator methods are no longer separately published as
named operations. To maintain backwards compatibility (or if you just
want this feature back), put the name of the most recent version of
your web service in the "last_version_with_mutator_named_operations"
field of your IWebServiceConfiguration implementation.

0.9.21 (2010-02-23)
===================

Fixed a family of bugs that were treating a request originated by a
web browser as though it had been originated by a web service client.

0.9.20 (2010-02-16)
===================

Fixed a bug that broke multi-versioned named operations that take
the request user as a fixed argument.

0.9.19 (2010-02-15)
===================

A few minor bugfixes to help with Launchpad integration.

0.9.18 (2010-02-11)
===================

Special note: this version contains backwards-incompatible
changes. You *must* change your configuration object to get your code
to work in this version! See "active_versions" below.

Added a versioning system for web services. Clients can now request
any number of distinct versions as well as a floating "trunk" which is
always the most recent version. By using version-aware annotations,
developers can publish the same data model differently over time. See
the example web service in example/multiversion/ to see how the
annotations work.

This release _replaces_ one of the fields in
IWebServiceConfiguration. The string 'service_version_uri'_prefix has
become the list 'active_versions'. The simplest way to deal with this is
to just put your 'service_version_uri_prefix' into a list and call it
'active_versions'. We recommend you also add a floating "development"
version to the end of 'active_versions', calling it something like
"devel" or "trunk". This will give your users a permanent alias to
"the most recent version of the web service".

0.9.17 (2009-11-10)
===================

Fixed a bug that raised an unhandled exception when a client tried to
set a URL field to a non-string value.

0.9.16 (2009-10-28)
===================

Fixed a bug rendering the XHTML representation of exported objects when they
contain non-ascii characters.

0.9.15 (2009-10-21)
===================

Corrected a misspelling of the WADL media type.

0.9.14 (2009-10-20)
===================

lazr.restful now runs without deprecation warnings on Python 2.6.

0.9.13 (2009-10-19)
===================

Fixed WADL template: HostedFile DELETE method should have an id of
HostedFile-delete, not HostedFile-put.

0.9.12 (2009-10-14)
===================

Transparent compression using Transfer-Encoding is now optional and
disabled by default for WSGI applications. (Real WSGI servers don't
allow applications to set hop-by-hop headers like Transfer-Encoding.)

This release introduces a new field to IWebServiceConfiguration:
set_hop_by_hop_headers. If you are rolling your own
IWebServiceConfiguration implementation, rather than subclassing from
BaseWebServiceConfiguration or one of its subclasses, you'll need to
set a value for this. Basically: set it to False if your application
is running in a WSGI server, and set it to True otherwise.

0.9.11 (2009-10-12)
===================

Fixed a minor import problem.

0.9.10 (2009-10-07)
===================

lazr.restful runs under Python 2.4 once again.

0.9.9 (2009-10-07)
==================

The authentication-related WSGI middleware classes have been split
into a separate project, lazr.authentication.

Fixed a bug that prevented some incoming strings from being loaded by
simplejson.

0.9.8 (2009-10-06)
==================

Added WSGI middleware classes for protecting resources with HTTP Basic
Auth or OAuth.

0.9.7 (2009-09-24)
==================

Fixed a bug that made it impossible to navigate to a field resource if
the field was a link to another object.

0.9.6 (2009-09-16)
==================

Simplified most web service configuration with grok directives.

0.9.5 (2009-08-26)
==================

Added a function that generates a basic WSGI application, given a
service root class, a publication class, and a response class.

Added an AbsoluteURL implementation for the simple
ServiceRootResource.

Added an adapter from Django's Manager class to IFiniteSequence, so
that services that use Django can serve database objects as
collections without special code.

Added an AbsoluteURL implementation for objects that provide more than
one URL path for the generated URL.

For services that use Django, added an adapter from Django's
ObjectDoesNotExist to lazr.restful's NotFoundView.

Fixed some testing infrastructure in lazr.restful.testing.webservice.

Fix some critical packaging problems.

0.9.4 (2009-08-17)
==================

Fixed an import error in simple.py.

Removed a Python 2.6ism from example/wsgi/root.py.


0.9.3 (2009-08-17)
==================

Added a lazr.restful.frameworks.django module to help with publishing
Django model objects through lazr.restful web services.

TraverseWithGet implementations now pass the request object into
get().

Create a simplified IServiceRootResource implementation for web
services that don't register their top-level collections as Zope
utilities.

Make traversal work for entries whose canonical location is beneath
another entry.

Raise a ValueError when numeric dates are passed to the
DatetimeFieldMarshaller.


0.9.2 (2009-08-05)
==================

Added a second example webservice that works as a standalone WSGI
application.

Bug 400170; Stop hacking sys.path in setup.py.

Bug 387487; Allow a subordinate entry resource under a resource where there
would normally be a field.  Navigation to support subordinate IObjects is
added to the publisher.


0.9.1 (2009-07-13)
==================

Declare multipart/form-data as the incoming media type for named
operations that include binary fields.

0.9 (2009-04-29)
================

- Initial public release
