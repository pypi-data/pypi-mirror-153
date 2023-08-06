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
"""Interfaces for lazr.restful."""

# pylint: disable-msg=W0401

__version__ = 1.0

# Re-export in such a way that __version__ can still be imported if
# dependencies are not yet available.
try:
    # While we generally frown on "*" imports, this approach, combined with
    # the fact we only test code from this module, means that we can verify
    # what has been exported in the local files (DRY).
    from lazr.restful.interfaces._fields import *  # noqa: F401, F403
    from lazr.restful.interfaces._fields import __all__ as _fields_all
    from lazr.restful.interfaces._rest import *  # noqa: F401, F403
    from lazr.restful.interfaces._rest import __all__ as _rest_all

    __all__ = []
    __all__.extend(_fields_all)
    __all__.extend(_rest_all)
except ImportError:
    pass
