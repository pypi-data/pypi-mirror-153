# Copyright 2008-2009 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.restful
#
# lazr.restful is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.restful is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.restful.  If not, see <http://www.gnu.org/licenses/>.

"""Classes for a resource that implements a binary file repository."""

__all__ = [
    "ByteStorageResource",
]

from zope.interface import implementer
from zope.publisher.interfaces import NotFound
from zope.schema import ValidationError

from lazr.restful.interfaces import IByteStorageResource
from lazr.restful._resource import HTTPResource


@implementer(IByteStorageResource)
class ByteStorageResource(HTTPResource):
    """A resource providing read-write access to a stored byte stream."""

    def __call__(self):
        """Handle a GET, PUT, or DELETE request."""
        if self.request.method == "GET":
            return self.do_GET()
        else:
            if self.context.field.readonly:
                # Read-only resources only support GET.
                allow_string = "GET"
            elif self.request.method == "PUT":
                type = self.request.headers["Content-Type"]
                disposition, params = self._parseContentDispositionHeader(
                    self.request.headers["Content-Disposition"]
                )
                cache_stream = self.request.bodyStream.getCacheStream()
                representation = cache_stream.read()
                return self.do_PUT(
                    type, representation, params.get("filename")
                )
            elif self.request.method == "DELETE":
                return self.do_DELETE()
            else:
                allow_string = "GET PUT DELETE"
        # The client tried to invoke an unsupported HTTP method.
        self.request.response.setStatus(405)
        self.request.response.setHeader("Allow", allow_string)

    def do_GET(self):
        """See `IByteStorageResource`."""
        media_type = self.getPreferredSupportedContentType()
        if media_type in [self.WADL_TYPE, self.DEPRECATED_WADL_TYPE]:
            result = self.toWADL().encode()
            self.request.response.setHeader("Content-Type", media_type)
            return result
        if not self.context.is_stored:
            # No stored document exists here yet.
            raise NotFound(self.context, self.context.filename, self.request)
        self.request.response.setStatus(303)  # See Other
        self.request.response.setHeader("Location", self.context.alias_url)

    def do_PUT(self, type, representation, filename):
        """See `IByteStorageResource`."""
        try:
            self.context.field.validate(representation)
        except ValidationError as e:
            self.request.response.setStatus(400)  # Bad Request
            return str(e)
        self.context.createStored(type, representation, filename)

    def do_DELETE(self):
        """See `IByteStorageResource`."""
        self.context.deleteStored()
