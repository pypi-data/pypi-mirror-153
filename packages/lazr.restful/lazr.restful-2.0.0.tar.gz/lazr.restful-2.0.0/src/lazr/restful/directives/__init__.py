# Copyright 2009 Canonical Ltd.  All rights reserved.

"""Martian directives used in lazr.restful."""

__all__ = [
    "request_class",
    "publication_class",
    "settings",
]

import martian
from zope.component import getSiteManager
from zope.location.interfaces import ILocation
from zope.interface.interface import InterfaceClass
from zope.traversing.browser import AbsoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL

from lazr.restful.interfaces import (
    IServiceRootResource,
    IWebServiceClientRequest,
    IWebServiceConfiguration,
    IWebServiceLayer,
)
from lazr.restful._resource import (
    register_versioned_request_utility,
    ServiceRootResource,
)
from lazr.restful.simple import (
    BaseWebServiceConfiguration,
    Publication,
    Request,
    RootResourceAbsoluteURL,
)
from lazr.restful.utils import make_identifier_safe


class request_class(martian.Directive):
    """Directive used to specify a service's request class.

    The default is lazr.restful.simple.Request.
    """

    scope = martian.CLASS
    store = martian.ONCE
    default = Request


class publication_class(martian.Directive):
    """Directive used to specify a service's publication class.

    The default is lazr.restful.simple.Publication.
    """

    scope = martian.CLASS
    store = martian.ONCE
    default = Publication


class ConfigurationGrokker(martian.ClassGrokker):
    """Subclass BaseWebServiceConfiguration for an easy configuration class.

    Subclass BaseWebServiceConfiguration and override any of the
    configuration settings specific to your web service.

    This grokker creates default implementations of createRequest()
    and get_request_user, if those methods are not implemented.

    The default implementations use the request and publication
    classes you specify with the directives
    lazr.restful.directives.request_class() and
    lazr.restful.directives.publication_class().

    This grokker then registers an instance of your subclass as the
    singleton configuration object.

    This grokker also creates marker interfaces for every web service
    version defined in the configuration, and registers each as an
    IWebServiceVersion utility.
    """

    martian.component(BaseWebServiceConfiguration)
    martian.directive(request_class)
    martian.directive(publication_class)

    def execute(self, cls, config, request_class, publication_class, *kw):
        # If implementations of the IWebServiceConfiguration methods are
        # missing, create them from the declarations.
        if not getattr(cls, "createRequest", None):

            def createRequest(self, body_instream, environ):
                """See `IWebServiceConfiguration`."""
                request = request_class(body_instream, environ)
                # Once we traverse the URL a bit and find the
                # requested web service version, we'll be able to set
                # the application to the appropriate service root
                # resource. This happens in
                # WebServiceRequestTraversal._removeVirtualHostTraversals().
                request.setPublication(publication_class(None))
                return request

            cls.createRequest = createRequest

        if not getattr(cls, "get_request_user", None):

            def get_request_user(self):
                return None

            cls.get_request_user = get_request_user

        # Register as utility.
        utility = cls()
        sm = getSiteManager()
        sm.registerUtility(utility, IWebServiceConfiguration)

        # Create and register marker interfaces for request objects.
        superclass = IWebServiceClientRequest
        for version in utility.active_versions:
            name_part = make_identifier_safe(version)
            if not name_part.startswith("_"):
                name_part = "_" + name_part
            classname = "IWebServiceClientRequestVersion" + name_part
            marker_interface = InterfaceClass(classname, (superclass,), {})
            register_versioned_request_utility(marker_interface, version)
            superclass = marker_interface
        return True


class ServiceRootGrokker(martian.ClassGrokker):
    """Registers your service root as a singleton object."""

    martian.component(ServiceRootResource)

    def execute(self, cls, config, *kw):
        getSiteManager().registerUtility(cls(), IServiceRootResource)
        return True


class RootResourceAbsoluteURLGrokker(martian.ClassGrokker):
    """Registers a strategy for generating your service's base URL.

    In most cases you can simply create an empty subclass of
    RootResourceAbsoluteURL.
    """

    martian.component(RootResourceAbsoluteURL)

    def execute(self, cls, config, *kw):
        getSiteManager().registerAdapter(cls)
        return True


class location_interface(martian.Directive):
    """Directive to specify the location interface.

    The default is zope.location.interfaces.ILocation
    """

    scope = martian.CLASS
    store = martian.ONCE
    default = ILocation


class AbsoluteURLGrokker(martian.ClassGrokker):
    """Registers a strategy for generating an object's URL.

    In most cases you can simply create an empty subclass of
    AbsoluteURL.
    """

    martian.component(AbsoluteURL)
    martian.directive(location_interface)

    def execute(self, cls, config, location_interface, *kw):
        getSiteManager().registerAdapter(
            cls, (location_interface, IWebServiceLayer), IAbsoluteURL
        )
        return True
