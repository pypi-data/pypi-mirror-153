# Copyright 2009 Canonical Ltd.  All rights reserved.
# pylint: disable-msg=E0211,E0213

"""Interface objects for the LAZR example web service."""

__all__ = [
    "AlreadyNew",
    "Cuisine",
    "ICookbook",
    "ICookbookSet",
    "ICookbookSubclass",
    "IDish",
    "IDishSet",
    "IFileManager",
    "IHasGet",
    "IFileManagerBackedByteStorage",
    "IRecipe",
    "IRecipeSet",
    "NameAlreadyTaken",
]

from zope.interface import Attribute, Interface
from zope.schema import Bool, Bytes, Choice, Date, Float, Int, TextLine, Text
from zope.location.interfaces import ILocation

from lazr.enum import EnumeratedType, Item

from lazr.restful.fields import CollectionField, Reference
from lazr.restful.interfaces import IByteStorage, ITopLevelEntryLink
from lazr.restful.declarations import (
    collection_default_content,
    export_destructor_operation,
    export_factory_operation,
    export_read_operation,
    export_write_operation,
    exported,
    exported_as_webservice_collection,
    exported_as_webservice_entry,
    operation_parameters,
    operation_returns_collection_of,
    operation_returns_entry,
    webservice_error,
)


class AlreadyNew(Exception):
    """A cookbook's name prohibits the cheap 'The New' trick."""

    webservice_error(400)


class NameAlreadyTaken(Exception):
    """The name given for a cookbook is in use by another cookbook."""

    webservice_error(409)


class WhitespaceStrippingTextLine(TextLine):
    """A TextLine that won't abide leading or trailing whitespace."""

    def set(self, object, value):
        """Strip whitespace before setting."""
        if value is not None:
            value = value.strip()
        super().set(object, value)


class Cuisine(EnumeratedType):
    """A vocabulary for cuisines."""

    GENERAL = Item("General", "General cooking")
    VEGETARIAN = Item("Vegetarian", "Vegetarian cooking")
    AMERICAN = Item("American", "Traditional American cooking")
    DESSERT = Item("Dessert", "Desserts")
    FRANCAISE = Item("Fran\xe7aise", "Cuisine fran\xe7aise")


class IHasGet(Interface):
    """A marker interface objects that implement traversal with get()."""

    def get(name):
        """Traverse to a contained object."""


@exported_as_webservice_entry(plural_name="dishes")
class IDish(ILocation):
    """A dish, annotated for export to the web service."""

    name = exported(TextLine(title="Name", required=True))
    recipes = exported(
        CollectionField(
            title="Recipes in this cookbook",
            value_type=Reference(schema=Interface),
        )
    )

    def removeRecipe(recipe):
        """Remove one of this dish's recipes."""


@exported_as_webservice_entry()
class IRecipe(ILocation):
    """A recipe, annotated for export to the web service."""

    id = exported(Int(title="Unique ID", required=True))
    dish = exported(Reference(title="Dish", schema=IDish))
    cookbook = exported(Reference(title="Cookbook", schema=Interface))
    instructions = exported(
        Text(title="How to prepare the recipe", required=True)
    )
    private = exported(
        Bool(title="Whether the public can see this recipe.", default=False)
    )
    prepared_image = exported(
        Bytes(0, 5000, title="An image of the prepared dish.", readonly=True)
    )

    @export_destructor_operation()
    def delete():
        """Delete the recipe."""


@exported_as_webservice_entry()
class ICookbook(IHasGet, ILocation):
    """A cookbook, annotated for export to the web service."""

    name = exported(TextLine(title="Name", required=True))
    copyright_date = exported(
        Date(
            title="Copyright Date",
            description="The copyright date for this work.",
        ),
        readonly=True,
    )
    description = exported(
        WhitespaceStrippingTextLine(title="Description", required=False)
    )
    revision_number = exported(
        Int(
            title="A record of the number of times "
            "this cookbook has been modified."
        )
    )
    confirmed = exported(
        Bool(
            title="Whether this information has been confirmed", default=False
        )
    )
    cuisine = exported(
        Choice(
            vocabulary=Cuisine, title="Cuisine", required=False, default=None
        )
    )
    last_printing = exported(
        Date(
            title="Last printing",
            description="The date of this work's most recent printing.",
        )
    )
    # Don't try this at home! Float is a bad choice for a 'price'
    # field because it's imprecise. Decimal is a better choice. But
    # this is just an example and we need a Float field, so...
    price = exported(Float(title="Retail price of the cookbook"))
    recipes = exported(
        CollectionField(
            title="Recipes in this cookbook",
            value_type=Reference(schema=IRecipe),
        )
    )
    cover = exported(Bytes(0, 5000, title="An image of the cookbook's cover."))

    @operation_parameters(
        search=TextLine(title="String to search for in recipe name.")
    )
    @operation_returns_collection_of(IRecipe)
    @export_read_operation()
    def find_recipes(search):
        """Search for recipes in this cookbook."""

    @operation_parameters(
        dish=Reference(title="Dish to search for.", schema=IDish)
    )
    @operation_returns_entry(IRecipe)
    @export_read_operation()
    def find_recipe_for(dish):
        """Find a recipe in this cookbook for a given dish."""

    @export_write_operation()
    def make_more_interesting():
        """Alter a cookbook to make it seem more interesting."""

    def removeRecipe(recipe):
        """Remove one of this cookbook's recipes."""

    @operation_parameters(cover=Bytes(title="New cover"))
    @export_write_operation()
    def replace_cover(cover):
        """Replace the cookbook's cover."""


# Resolve dangling references
IDish["recipes"].value_type.schema = IRecipe
IRecipe["cookbook"].schema = ICookbook


@exported_as_webservice_entry()
class ICookbookSubclass(ICookbook):
    """A published subclass of ICookbook.

    This entry interface is never used, but it acts as a test case for
    a published entry interface that subclasses another published
    entry interface.
    """


class IFeaturedCookbookLink(ITopLevelEntryLink):
    """A marker interface."""


@exported_as_webservice_collection(ICookbook)
class ICookbookSet(IHasGet):
    """The set of all cookbooks, annotated for export to the web service."""

    @collection_default_content()
    def getCookbooks():
        """Return the list of cookbooks."""

    @operation_parameters(
        search=TextLine(title="String to search for in recipe name."),
        vegetarian=Bool(
            title="Whether or not to limit the search to "
            "vegetarian cookbooks.",
            default=False,
        ),
    )
    @operation_returns_collection_of(IRecipe)
    @export_read_operation()
    def find_recipes(search, vegetarian):
        """Search for recipes across cookbooks."""

    @operation_parameters(
        cuisine=Choice(
            vocabulary=Cuisine, title="Cuisine to search for in recipe name."
        )
    )
    @operation_returns_collection_of(ICookbook)
    @export_read_operation()
    def find_for_cuisine(cuisine):
        """Search for cookbooks of a given cuisine."""

    @export_factory_operation(
        ICookbook,
        [
            "name",
            "description",
            "cuisine",
            "copyright_date",
            "last_printing",
            "price",
        ],
    )
    def create(
        name, description, cuisine, copyright_date, last_printing, price
    ):
        """Create a new cookbook."""

    featured = Attribute("The currently featured cookbook.")


@exported_as_webservice_collection(IDish)
class IDishSet(IHasGet):
    """The set of all dishes, annotated for export to the web service."""

    @collection_default_content()
    def getDishes():
        """Return the list of dishes."""


@exported_as_webservice_collection(IRecipe)
class IRecipeSet(IHasGet):
    """The set of all recipes, annotated for export to the web service."""

    @collection_default_content()
    def getRecipes():
        """Return the list of recipes."""

    @export_factory_operation(
        IRecipe, ["id", "cookbook", "dish", "instructions", "private"]
    )
    def createRecipe(id, cookbook, dish, instructions, private=False):
        """Create a new recipe."""

    def removeRecipe(recipe):
        """Remove a recipe from the list."""


class IFileManager(IHasGet):
    """A simple manager for hosted binary files.

    This is just an example for how you might host binary files. It's
    only useful for testing purposes--you'll need to come up with your
    own implementation, or use lazr.librarian.
    """

    def put(name, value):
        """Store a file in the manager."""

    def delete(name):
        """Delete a file from the manager."""


class IFileManagerBackedByteStorage(IByteStorage):

    id = Attribute("The manager ID for this file.")
