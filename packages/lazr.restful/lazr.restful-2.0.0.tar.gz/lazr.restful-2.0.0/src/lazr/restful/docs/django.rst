Django integration
******************

lazr.restful includes some code to make it easier to publish Django
model objects as web service resources.

Setup
=====

lazr.restful doesn't depend on Django, but these tests need access to
Django-like modules and classes. We're going to create some fake
modules and classes for purposes of the tests. If Django is actually
installed on this system, these modules will mask the real modules, but
it'll only last until the end of the test.

    >>> import sys
    >>> import types
    >>> def create_fake_module(name):
    ...     previous = None
    ...     previous_names = []
    ...     for module_name in name.split('.'):
    ...         previous_names.append(module_name)
    ...         full_name = '.'.join(previous_names)
    ...         module = sys.modules.get(full_name)
    ...         if module is None:
    ...             module = types.ModuleType(full_name)
    ...         if previous is not None:
    ...             setattr(previous, module_name, module)
    ...         previous = module
    ...         sys.modules[full_name] = module

Before loading django.zcml, we need to create fake versions of all the
modules and classes we'll be using, because if the real Django happens
to be installed, loading the real Django classes will trigger all
sorts of Django code that we can't handle.

    >>> create_fake_module('settings')
    >>> import settings

    >>> class ObjectDoesNotExist(Exception):
    ...     pass
    >>> create_fake_module('django.core.exceptions')
    >>> import django.core.exceptions
    >>> django.core.exceptions.ObjectDoesNotExist = ObjectDoesNotExist

    >>> class Manager:
    ...     """A fake version of Django's Manager class."""
    ...     def __init__(self, l):
    ...         self.list = l
    ...     def iterator(self):
    ...         return self.list.__iter__()
    ...     def all(self):
    ...         return self.list
    ...     def count(self):
    ...         return len(self.list)

    >>> create_fake_module('django.db.models.manager')
    >>> import django.db.models.manager
    >>> django.db.models.manager.Manager = Manager

Now we can load a ZCML configuration typical of a lazr.restful
application that publishes Django model objects through a web service.

    >>> from zope.configuration import xmlconfig
    >>> ignore = xmlconfig.string("""
    ...   <configure xmlns="http://namespaces.zope.org/zope">
    ...     <include package="lazr.restful" file="basic-site.zcml" />
    ...     <include package="lazr.restful.frameworks" file="django.zcml" />
    ...   </configure>
    ... """)


Configuration
=============

Like any lazr.restful app, a Django app can subclass
BaseWebServiceConfiguration and customize the subclass to set
configuration options. However, you might find it easier to subclass
DjangoWebServiceConfiguration instead and put the configuration in
your settings.py file.

An attribute 'foo_bar' defined in IWebServiceConfiguration can be set
in your settings.py file as LAZR_RESTFUL_FOO_BAR. Here, we'll override
the default value of 'show_tracebacks'.

    >>> settings.LAZR_RESTFUL_SHOW_TRACEBACKS = False

    >>> from lazr.restful.frameworks.django import (
    ...     DjangoWebServiceConfiguration)
    >>> class MyConfiguration(DjangoWebServiceConfiguration):
    ...     pass
    >>> MyConfiguration().show_tracebacks
    True

Once grok is called on the configuration class...

    >>> from grokcore.component.testing import grok_component
    >>> ignored = grok_component('MyConfiguration', MyConfiguration)

...MyConfiguration is the registered utility for
IWebServiceConfiguration, and its value for use_https and
show_tracebacks have been taken from the 'settings' module.

    >>> from zope.component import getUtility
    >>> from lazr.restful.interfaces import IWebServiceConfiguration
    >>> utility = getUtility(IWebServiceConfiguration)
    >>> utility.show_tracebacks
    False

Attributes that don't have values in settings.py are given their
default value.

    >>> utility.active_versions
    []
    >>> utility.use_https
    True


IDjangoLocation
===============

The simplest way to generate URLs for your resources is to have your
service root resource implement IAbsoluteURL (to generate the root of
all web service URLs), and have all your model classes implement
ILocation (which defines the URL in terms of a parent object's
URL).

ILocation requires that you define a property called __name__. This is
part of the URL unique to an object, as opposed to the first part of
the URL, which comes from its parent. Unfortunately, the Django object
metaclass won't allow you to assign a property to __name__.

IDjangoLocation is a class provided by lazr.restful. It acts just like
ILocation, but the last part of the URL comes from __url_path__
instead of __name__.

Here's some setup; a root resource that has its own AbsoluteURL
implementation.

    >>> from lazr.restful.testing.webservice import (
    ...     StubRootResource, StubRootResourceURL)
    >>> from zope.component import getSiteManager
    >>> sm = getSiteManager()
    >>> sm.registerAdapter(StubRootResourceURL)

Now here's a subordinate resource that just implements IDjangoLocatino.

    >>> from zope.interface import implementer
    >>> from lazr.restful.frameworks.django import IDjangoLocation
    >>> @implementer(IDjangoLocation)
    ... class SubordinateResource:
    ...
    ...     @property
    ...     def __parent_object__(self):
    ...         return StubRootResource()
    ...
    ...     @property
    ...     def __url_path__(self):
    ...         return "myname"

The django.zcml file in lazr/restful/frameworks contains an adapter
between IDjangoLocation and ILocation. Thanks to that adapter, it's
possible to adapt a Django model object to ILocation and check on its
__name__.

    >>> from zope.location.interfaces import ILocation
    >>> resource = SubordinateResource()
    >>> as_location = ILocation(resource)
    >>> print(as_location.__name__)
    myname

It's also possible to adapt a Django model object to IAbsoluteURL and
get its full URL.

    >>> from zope.component import getMultiAdapter
    >>> from zope.traversing.browser.interfaces import IAbsoluteURL
    >>> from lazr.restful.simple import Request
    >>> request = Request("", {})
    >>> print(str(getMultiAdapter((resource, request), IAbsoluteURL)))
    http://exampleurl/myname


ObjectDoesNotExist
==================

The django.zcml helper file contains an adapter registration so that
Django's ObjectDoesNotExist exceptions are treated as 404
errors.

To test this, we simply instantiate an ObjectDoesNotExist and then get
a view for it.

    >>> exception = ObjectDoesNotExist()
    >>> view = getMultiAdapter((exception, request), name="index.html")
    >>> view()
    ''

The view for the ObjectDoesNotExist exception sets the HTTP response
code to 404.

    >>> request.response.getStatus()
    404


Managers
========

The django.zcml file includes an adapter between Django's Manager
class (which controls access to the database) and Zope's
IFiniteCollection interface (used by lazr.batchnavigator to batch data
sets).

    >>> from zope.interface.common.sequence import IFiniteSequence
    >>> data = ["foo", "bar", "baz"]
    >>> from django.db.models.manager import Manager
    >>> manager = Manager(data)
    >>> sequence = IFiniteSequence(manager)

The adapter class is ManagerSequencer.

    >>> sequence
    <lazr.restful.frameworks.django.ManagerSequencer...>

A ManagerSequencer object makes a Manager object act like a Python
list, which is what IFiniteSequence needs.

    >>> len(sequence)
    3

    >>> print(sequence[1])
    bar

    >>> sequence[1:3]
    ['bar', 'baz']

    >>> [x for x in sequence]
    ['foo', 'bar', 'baz']
