WSGI example web service
************************

lazr.restful has two example web services. The one in
src/lazr/restful/example is designed to test all of lazr.restful's
features and Zope integrations. The one in
src/lazr/restful/example/wsgi is designed to be a simple,
understandable web service that can act as WSGI middleware.

Getting Started
===============

Here's how to set up a web server serving up the example WSGI web
service.

1. python bootstrap.py
2. bin/buildout
3. bin/run src/lazr/restful/example/wsgi/run.py localhost 8001

The web server is now running at http://localhost:8001/1.0/.

(Why "1.0"? That's defined in the web service configuration; see
below.)

Resources
=========

The resources for the WSGI example web service are:

1. A service root resource. Defined in lazr.restful.example.wsgi.root,
   published at /1.0/

2. A collection resource, defined in
   lazr.restful.example.wsgi.resources, published at /1.0/pairs

3. Two key-value pair entries. The key-value pair is defined in
   lazr.restful.example.wsgi.resources. The resources themselves are
   published at /1.0/pairs/1 and /1.0/pairs/foo.

For simplicity's sake, there are no named operations (if you're
curious, the web service in lazr/restful/example has many named
operations) and no way to create or delete key-value pairs.

Let's take a look at the resource definitions. This is the part that
will be significantly different for any web service you create. There
is code in these classes that's not explained here: it's code for
traversal or for URL generation, and it's explained below.

The root
--------

Every lazr.restful web service needs a root resource. The simplest way
to get a root resource is to subclass lazr.restful.simple.RootResource
and implement _build_top_level_objects(), which advertises the main
features of your web service to your users.

Our service root resource is
lazr.restful.example.wsgi.root.WSGIExampleWebServiceRootResource. We
only have one top-level object, the collection of key-value pairs, so
this implementation of _build_top_level_objects() just returns
'pairs'. It maps 'pairs' to a 2-tuple (IKeyValuePair, pairset). Here,
"pairset" is the collection of key-value pairs itself, and
IKeyValuePair is a Zope interface class that explains what kind of
object is found in the collection. You'll see IKeyValuePair again in
the next section of this document.

If you subclass RootResource, lazr.restful will automatically know to
use that class as your service root. If you decide not to subclass
RootResource, you'll have to register your root class as the utility
for IServiceRootResource (see "Utilities" below).

The top-level collection
------------------------

The collection of key-value pairs is defined in
lazr.restful.example.wsgi.resources. First we define an interface
(IPairSet) that's decorated with lazr.restful decorators:

1. @exported_as_webservice_collection(IKeyValuePair) tells lazr.restful
   that an IPairSet should be published as a collection resource, as
   opposed to being published as an entry or not published at all. The
   "IKeyValuePair" lets lazr.restful know that this is a collection of
   key-value pairs and not some other kind of collection.

2. @collection_default_content() tells lazr.restful to call the
   getPairs() method when it wants to know what items are in the
   collection.

Then we define the implementation (PairSet), which implements
getPairs().

The entry resource
------------------

The key-value pair is also defined in
lazr.restful.example.wsgi.resources. First we define an interface
(IKeyValuePair) that's decorated with lazr.restful decorators:

1. @exported_as_webservice_entry() tells lazr.restful that an
   IKeyValuePair should be published as an entry, as opposed to being
   published as an entry or not published at all.

2. exported() tells lazr.restful which attributes of an IKeyValuePair
   should be published to the web service, and which ones are for
   internal use only. In this case, both 'key' and 'value' are
   published.

Then we define KeyValuePair, which simply stores a key and value.

Traversal
=========

The traversal code turns an incoming URL path like "/1.0/pairs/foo"
into an object to be published. The fragment "1.0" identifies the
IServiceRootResource, the fragment "pairs" identifies the IPairSet,
and the fragment "foo" identifies a specific IKeyValuePair within the
IPairSet.

Traversal code can get very complicated. If you're interested in the
complex stuff, look at the custom code in lazr.restful.example that
implements IPublishTraverse. But all the example resources in
lazr.restful.example.wsgi do traversal simply by subclassing
lazr.restful.publisher.TraverseWithGet. With TraverseWithGet, to
traverse from a parent resource to its children, all you have to do is
define a get() method. This method takes a path fragment like "pairs"
and returns the corresponding object.

Let's take an example. A request comes in for "/1.0/pairs". What happens?

1."1.0" identifies the web service root
  (lazr.restful.example.wsgi.root.WSGIExampleWebServiceRootResource)

2. "pairs" is passed into WSGIExampleWebServiceRootResource.get(), and
   the result is the lazr.restful.example.wsgi.resources.PairSet
   object. (The get() implementation is inherited from
   RootResource. It works because our implementation
   of _build_top_level_objects returned a dictionary that had a key
   called "pairs".)

3. There are no more path fragments, so traversal is complete. The
   PairSet object will be published as a collection resource. Why a
   collection? Because PairSet implements IPairSet, which is published
   as a collection. (Remember @exported_as_webservice_collection()?)

You don't have to write all the traversal code your web service will
ever use. There's a set of default rules that take over once your
custom traversal code returns an IEntry, the way PairSet.get() does.

Here's a more complex example. A request comes in for
"/1.0/pairs/foo/value". What happens?

1. "1.0" identifies the web service root (WSGIExampleWebServiceRootResource)

2. "pairs" is passed into WSGIExampleWebServiceRootResource.get(), and
   the result is the PairSet object.

3. "foo" is passed into PairSet.get(), and the result is the KeyValuePair
   object.

4. Because IKeyValuePair is published as an entry (remember
   @exported_as_webservice_entry?), the custom traversal code now
   stops. What happens next is entirely controlled by lazr.restful.
   Because of this, it doesn't make sense to have an entry subclass
   TraverseWithGet or implement IPublishTraverse.

5. "value" identifies a published field of IKeyValuePair. lazr.restful
   traverses to that field. It's a Text field.

6. There are no more path fragments, so traversal is complete. The
   Text field is published as a field resource.

URL generation
==============

URL generation is the opposite of traversal. With traversal you have a
URL and you need to find which object it refers to. With URL
generation you have an object and you need to find its URL.

URL generation can get arbitrarily complex--for each of your resource
classes, you must define a class that implements the Zope interface
IAbsoluteURL. But this web service takes a simpler approach. We define
two empty classes, both in lazr.restful.example.wsgi.root:
RootAbsoluteURL and BelowRootAbsoluteURL. The subclasses contain no
code of their own; they act as signals to lazr.restful that we want to
use certain URL generation strategies.

RootAbsoluteURL is a subclass of
lazr.restful.simple.RootResourceAbsoluteURL. By subclassing it we tell
lazr.restful to generate the URL to the root resource using the
hostname, protocol, and path information specified in the web service
configuration (see below). Pretty much any lazr.restful web service
should be able to use this strategy, since you need to define a lot of
that configuration information anyway.

The second strategy is a little more work. Keep in mind the basic
structure of this web service. There's a root resource, a collection
resource underneath the root, a bunch of entry resources underneath
the collection resource, and a bunch of field resources underneath
each entry. Every resource except for the root has a unique
parent.

BelowRootAbsoluteURL is a subclass of
zope.traversing.browser.AbsoluteURL, which knows how to generate URLs
using a recursive algorithm. To calculate a resource's URL, this
algorithm calculates the URL of the parent resource, and tacks a
resource-specific string onto it.

So the URL of a key-value pair is the URL of the collection
("http://localhost:8000/1.0/pairs"), plus a slash, plus a
resource-specific string (the key, "foo"). We use RootAbsoluteURL to
calculate the URL of the root resource ("http://localhost:8000/1.0"),
so the recursion has a place to bottom out. All we need is a way to
know the parent of any given resource, and for any given resource,
which string to stick on the end of the parent's URL.

We do this by having all our classes (except for the root) implement a
Zope interface called ILocation. With ILocation you just have to
define two properties: __parent__ and __name__. __parent__ points to
the object's parent in the resource tree, and __name__ is the portion of
the URL space unique to this object. An object's URL is its
__parent__'s url, plus a slash, plus its __name__.

Here's an example. Consider the key-value pair at
http://localhost:8000/1.0/pairs/foo. Its __name__ is the name of the
key, "foo". Its __parent__ is the top-level collection of key-value
pairs, found with getUtility(IPairSet). The collection's __name__ is
"pairs", and its __parent__ is the service root.

The service root gets its URL from RootAbsoluteURL (which gets most of
its information from the web service configuration), which gives us
"http://localhost:8000/1.0/". Put those pieces together, and you get
"http://localhost:8000/1.0/pairs/foo".

Configuration
=============

The configuration class (defined in lazr.restful.example.wsgi.root)
contains miscellaneous service-specific configuration settings. It's
consulted it for miscellaneous things that depend on the web service
and shouldn't be hard-coded. The most interesting configuration
setting is probably service_version_uri_prefix, which controls the
version number that shows up in URLs.

The simplest way to create this class is to subclass
lazr.restful.simple.BaseWebServiceConfiguration. You can see what
configuration settings are available by looking at the interface
definition class, lazr.restful.interfaces.IWebServiceConfiguration.
Just have your subclass set any of the IWebServiceConfiguration values
you want to change, and leave the rest alone. This web service
overrides the IWebServiceConfiguration defaults for four settings:
code_revision, service_version_uri_prefix, use_https, and
view_permission.

Utilities
=========

The service root and the web service configuration object are both
registered as Zope utilities. A Zope utility is basically a
singleton. These two classes are registered as singletons because from
time to time, lazr.restful needs access to a canonical instance of one
of these classes.

lazr.restful automatically registers utilities when you
subclass certain classes. Subclass lazr.restful.simple.RootResource
and your subclass will be registered as the "service root resource"
utility. Subclass BaseWebServiceConfiguration and your subclass will
be registered as the "web service configuration" utility.

If you don't want to subclass these magic classes, you'll need to
register the utilities yourself, using ZCML. See
lazr/restful/example/base/ for a web service that uses ZCML to
register utilities.

[XXX leonardr 20090803 bug=407505 miscellaneous improvements to this
doc.]
