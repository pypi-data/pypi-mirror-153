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
"""Patterns for building a RESTful web service."""

# pylint: disable-msg=W0401

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata

__version__ = importlib_metadata.version("lazr.restful")

# Re-export in such a way that __version__ can still be imported if
# dependencies are not yet available.
try:
    # While we generally frown on "*" imports, this approach, combined with
    # the fact we only test code from this module, means that we can verify
    # what has been exported in the local files (DRY).
    from lazr.restful._bytestorage import *  # noqa: F401, F403
    from lazr.restful._bytestorage import __all__ as _bytestorage_all
    from lazr.restful._operation import *  # noqa: F401, F403
    from lazr.restful._operation import __all__ as _operation_all
    from lazr.restful._resource import *  # noqa: F401, F403
    from lazr.restful._resource import __all__ as _resource_all

    __all__ = []
    __all__.extend(_bytestorage_all)
    __all__.extend(_operation_all)
    __all__.extend(_resource_all)
except ImportError:
    pass
