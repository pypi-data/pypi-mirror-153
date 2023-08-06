__all__ = ["IKeyValuePair", "IPairSet", "KeyValuePair", "PairSet"]

from zope.interface import implementer
from zope.schema import Bool, Text
from zope.location.interfaces import ILocation

from lazr.restful.declarations import (
    collection_default_content,
    export_destructor_operation,
    export_operation_as,
    export_read_operation,
    export_write_operation,
    exported,
    exported_as_webservice_collection,
    exported_as_webservice_entry,
    mutator_for,
    operation_for_version,
    operation_parameters,
    operation_removed_in_version,
    operation_returns_collection_of,
)

# Our implementations of these classes can be based on the
# implementations from the WSGI example.
from lazr.restful.example.wsgi.resources import (
    PairSet as BasicPairSet,
    KeyValuePair as BasicKeyValuePair,
)


# Our interfaces _will_ diverge from the WSGI example interfaces, so
# define them separately.
@exported_as_webservice_entry()
class IKeyValuePair(ILocation):
    key = exported(Text(title="The key"))
    value = exported(Text(title="The value"))
    a_comment = exported(
        Text(title="A comment on this key-value pair.", readonly=True),
        ("1.0", dict(exported=True, exported_as="comment")),
    )
    deleted = exported(
        Bool(title="Whether this key-value pair has been " "deleted"),
        ("3.0", dict(exported=True)),
        exported=False,
    )

    @mutator_for(a_comment)
    @export_write_operation()
    @operation_parameters(comment=Text())
    @operation_for_version("1.0")
    def comment_mutator_1(comment):
        """A comment mutator that adds some junk on the end."""

    @mutator_for(a_comment)
    @export_write_operation()
    @operation_parameters(comment=Text())
    @operation_for_version("3.0")
    def comment_mutator_2(comment):
        """A comment mutator that adds different junk on the end."""

    @export_destructor_operation()
    @operation_for_version("1.0")
    def total_destruction():
        """A destructor that removes the key-value pair altogether."""

    @export_destructor_operation()
    @operation_for_version("3.0")
    def mark_as_deleted():
        """A destructor that simply sets .deleted to True."""


@exported_as_webservice_collection(IKeyValuePair)
class IPairSet(ILocation):
    # In versions 2.0 and 3.0, the collection of key-value pairs
    # includes all pairs.
    @collection_default_content("2.0")
    def getPairs():
        """Return the key-value pairs."""

    # Before 2.0, it only includes pairs whose values are not None.
    @collection_default_content("beta")
    def getNonEmptyPairs():
        """Return the key-value pairs that don't map to None."""

    def get(request, name):
        """Retrieve a key-value pair by its key."""

    # This operation is not published in trunk.
    @operation_removed_in_version("trunk")
    # In 3.0, it's published as 'by_value'
    @export_operation_as("by_value")
    @operation_for_version("3.0")
    # In 1.0 and 2.0, it's published as 'byValue'
    @export_operation_as("byValue")
    @operation_parameters(value=Text())
    @operation_returns_collection_of(IKeyValuePair)
    @export_read_operation()
    @operation_for_version("1.0")
    # This operation is not published in versions earlier than 1.0.
    def find_for_value(value):
        """Find key-value pairs that have the given value."""


@implementer(IPairSet)
class PairSet(BasicPairSet):
    def find_for_value(self, value):
        return [pair for pair in self.pairs if value == pair.value]

    def getNonEmptyPairs(self):
        return [pair for pair in self.pairs if pair.value is not None]


@implementer(IKeyValuePair)
class KeyValuePair(BasicKeyValuePair):
    def __init__(self, pairset, key, value):
        super().__init__(pairset, key, value)
        self.a_comment = ""
        self.deleted = False

    def comment_mutator_1(self, comment):
        """A comment mutator."""
        self.a_comment = comment + " (modified by mutator #1)"

    def comment_mutator_2(self, comment):
        """A comment mutator."""
        self.a_comment = comment + " (modified by mutator #2)"

    def total_destruction(self):
        """Remove the pair from the pairset."""
        self.set.pairs.remove(self)

    def mark_as_deleted(self):
        """Set .deleted to True."""
        self.deleted = True
