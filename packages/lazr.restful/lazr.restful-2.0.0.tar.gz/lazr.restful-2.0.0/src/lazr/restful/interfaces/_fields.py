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

"""Interfaces for LAZR zope.schema fields."""

__all__ = [
    "ICollectionField",
    "IReference",
    "IReferenceChoice",
]


from zope.interface import Attribute
from zope.schema.interfaces import IChoice, IObject, ISequence


class ICollectionField(ISequence):
    """A field representing a sequence.

    All iterables satisfy this collection field.
    """


class IReference(IObject):
    """A reference to an object providing a particular schema.

    Validation only enforce that the object provides the interface, not
    that all its attributes matches the schema constraints.
    """


class IReferenceChoice(IReference, IChoice):
    """Interface for a choice among objects."""

    schema = Attribute(
        "The interface provided by all elements of the choice vocabulary."
    )
