# Copyright 2009 Canonical Ltd.  All rights reserved.

"""A simple security policy for the LAZR example web service."""

__all__ = [
    "CookbookWebServiceSecurityPolicy",
]

from zope.security.simplepolicies import PermissiveSecurityPolicy
from zope.security.proxy import removeSecurityProxy
from lazr.restful.example.base.interfaces import IRecipe


class CookbookWebServiceSecurityPolicy(PermissiveSecurityPolicy):
    """A very basic security policy."""

    def checkPermission(self, permission, object):
        """Check against a simple policy.

        * Private recipes are always hidden.
        * Any fields protected by lazr.restful.example.base.ViewPrivate are
          hidden.
        """
        if IRecipe.providedBy(object):
            return not removeSecurityProxy(object).private
        elif permission == "lazr.restful.example.base.ViewPrivate":
            return False
        else:
            return True
