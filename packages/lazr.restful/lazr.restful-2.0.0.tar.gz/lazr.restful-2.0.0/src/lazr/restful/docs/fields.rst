LAZR Fields
***********

===============
CollectionField
===============

CollectionField is a field representing an iterable collection. The
field provides ICollectionField which is an extension of ISequence.

    >>> from zope.schema import Int
    >>> from zope.schema.interfaces import ISequence
    >>> from lazr.restful.interfaces import ICollectionField
    >>> from lazr.restful.fields import CollectionField

    >>> int_collection = CollectionField(
    ...     title='A collection', value_type=Int())

    >>> from zope.interface.verify import verifyObject
    >>> verifyObject(ICollectionField, int_collection)
    True

    >>> ICollectionField.extends(ISequence)
    True

By default, such fields are readonly.

    >>> int_collection.readonly
    True

But it can be made read-write.

    >>> rw_collection = CollectionField(
    ...     title='A writable collection.', readonly=False)
    >>> rw_collection.readonly
    False

The validate method accepts any iterable that satisfy the contained
elements.

    >>> int_collection.validate(range(10))

But if the object isn't iterable, NotAContainer is raised.

    >>> int_collection.validate(object())
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.schema._bootstrapinterfaces.NotAContainer: <object...>

If the iterable contains an invalid item, WrongContainedType is raised.

    >>> int_collection.validate(['a', 1, 2, 'b'])
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.schema._bootstrapinterfaces.WrongContainedType: ...

=========
Reference
=========

A Reference field is just like an Object except that it doesn't validate
by value, but only check that the value provides the proper schema.

    >>> from zope.interface import Interface, directlyProvides
    >>> from zope.schema import Text
    >>> class MySchema(Interface):
    ...     a_value = Text()

    >>> from lazr.restful.fields import Reference
    >>> from lazr.restful.interfaces import IReference

    >>> reference = Reference(schema=MySchema)
    >>> verifyObject(IReference, reference)
    True

    >>> class Fake:
    ...     pass
    >>> fake = Fake()
    >>> reference.validate(fake)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.schema._bootstrapinterfaces.SchemaNotProvided: ...

    >>> directlyProvides(fake, MySchema)
    >>> reference.validate(fake)

The Reference field supports the standard IField constraint.

    >>> reference = Reference(
    ...     schema=MySchema,
    ...     constraint=lambda value: 'good' in value.a_value)

    >>> fake.a_value = 'bad'
    >>> reference.validate(fake)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.schema._bootstrapinterfaces.ConstraintNotSatisfied: ...

    >>> fake.a_value = 'good'
    >>> reference.validate(fake)
