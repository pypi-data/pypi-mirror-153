# Copyright 2009 Canonical Ltd.  All rights reserved.

"""Data model objects for the LAZR example web service."""

__all__ = [
    "Cookbook",
    "CookbookServiceRootResource",
    "CookbookSet",
    "CookbookWebServiceObject",
    "WebServiceConfiguration",
]

from datetime import date

import grokcore.component

from zope.interface import implementer
from zope.location.interfaces import ILocation
from zope.component import getMultiAdapter, getUtility
from zope.schema.interfaces import IBytes
from zope.security.proxy import removeSecurityProxy

from lazr.restful import directives, ServiceRootResource

from lazr.restful.interfaces import (
    IByteStorage,
    IEntry,
    IServiceRootResource,
    ITopLevelEntryLink,
    IWebServiceConfiguration,
)
from lazr.restful.example.base.interfaces import (
    AlreadyNew,
    Cuisine,
    ICookbook,
    ICookbookSet,
    IDish,
    IDishSet,
    IFileManager,
    IRecipe,
    IRecipeSet,
    IHasGet,
    NameAlreadyTaken,
)
from lazr.restful.simple import BaseWebServiceConfiguration
from lazr.restful.testing.webservice import WebServiceTestPublication
from lazr.restful.utils import get_current_web_service_request


# Entry classes.
class CookbookWebServiceObject:
    """A basic object published through the web service."""


@implementer(IByteStorage, ILocation)
class SimpleByteStorage(
    CookbookWebServiceObject, grokcore.component.MultiAdapter
):
    """A simple IByteStorage implementation"""

    grokcore.component.adapts(IEntry, IBytes)
    grokcore.component.provides(IByteStorage)

    def __init__(self, entry, field):
        self.entry = entry
        self.field = field
        self.is_stored = getattr(self.entry, field.__name__, None) is not None
        if self.is_stored:
            self.filename = getattr(self.entry, field.__name__).filename
            self.id = getattr(self.entry, field.__name__).id
        else:
            self.filename = field.__name__
            self.id = None

        # AbsoluteURL implementation.
        self.__parent__ = self.entry.context
        self.__name__ = self.field.__name__

    @property
    def alias_url(self):
        """The URL to the managed file.

        This URL will always contain the name of the latest version, no
        matter the version of the original request. This is not ideal,
        but it's acceptable because 1) this is just a test
        implementation, and 2) the ByteStorage implementation cannot
        change between versions.
        """
        return "http://cookbooks.dev/%s/filemanager/%s" % (
            getUtility(IWebServiceConfiguration).active_versions[-1],
            self.id,
        )

    def createStored(self, mediaType, representation, filename=None):
        self.representation = representation
        if filename is None:
            filename = self.field.__name__
        self.id = getUtility(IFileManager).put(
            mediaType, representation, filename
        )
        self.filename = filename
        setattr(self.entry, self.field.__name__, self)

    def deleteStored(self):
        getUtility(IFileManager).delete(self.id)
        setattr(self.entry, self.field.__name__, None)


@implementer(ICookbook)
class Cookbook(CookbookWebServiceObject):
    """An object representing a cookbook"""

    def __init__(
        self,
        name,
        description,
        cuisine,
        copyright_date,
        last_printing=None,
        price=0,
        confirmed=False,
    ):
        self.name = name
        self.cuisine = cuisine
        self.description = description
        self.recipes = []
        self.copyright_date = copyright_date
        self.last_printing = last_printing
        self.price = price
        self.confirmed = confirmed
        self.cover = None
        self.revision_number = 0

    @property
    def __name__(self):
        return self.name

    @property
    def __parent__(self):
        return getUtility(ICookbookSet)

    def get(self, name):
        """See `IHasGet`."""
        match = [recipe for recipe in self.recipes if recipe.dish.name == name]
        if len(match) > 0:
            return match[0]
        return None

    def find_recipes(self, search):
        """See `ICookbook`."""
        recipes = []
        for recipe in self.recipes:
            if search in recipe.dish.name:
                recipes.append(recipe)
        return recipes

    def make_more_interesting(self):
        """See `ICookbook`."""
        if self.name.find("The New ") == 0:
            raise AlreadyNew(
                "The 'New' trick can't be used on this cookbook "
                "because its name already starts with 'The New'."
            )
        self.name = "The New " + self.name

    def find_recipe_for(self, dish):
        """See `ICookbook`."""
        for recipe in self.recipes:
            if recipe.dish == dish:
                return recipe
        return None

    def removeRecipe(self, recipe):
        """See `ICookbook`."""
        self.recipes.remove(recipe)

    def replace_cover(self, cover):
        entry = getMultiAdapter(
            (self, get_current_web_service_request()), IEntry
        )
        storage = SimpleByteStorage(entry, ICookbook["cover"])
        storage.createStored("application/octet-stream", cover, "cover")


@implementer(IDish)
class Dish(CookbookWebServiceObject):
    def __init__(self, name):
        self.name = name
        self.recipes = []

    @property
    def __name__(self):
        return self.name

    @property
    def __parent__(self):
        return getUtility(IDishSet)

    def removeRecipe(self, recipe):
        self.recipes.remove(recipe)


@implementer(IRecipe)
class Recipe(CookbookWebServiceObject):
    def __init__(self, id, cookbook, dish, instructions, private=False):
        self.id = id
        self.dish = dish
        removeSecurityProxy(self.dish.recipes).append(self)
        self.cookbook = cookbook
        removeSecurityProxy(self.cookbook.recipes).append(self)
        self.instructions = instructions
        self.private = private
        self.prepared_image = None

    @property
    def __name__(self):
        return str(self.id)

    @property
    def __parent__(self):
        return getUtility(IRecipeSet)

    def delete(self):
        getUtility(IRecipeSet).removeRecipe(self)


# Top-level objects.
@implementer(ILocation)
class CookbookTopLevelObject(
    CookbookWebServiceObject, grokcore.component.GlobalUtility
):
    """An object published at the top level of the web service."""

    @property
    def __parent__(self):
        return getUtility(IServiceRootResource)

    @property
    def __name__(self):
        raise NotImplementedError()


@implementer(ITopLevelEntryLink)
class FeaturedCookbookLink(CookbookTopLevelObject):
    """A link to the currently featured cookbook."""

    grokcore.component.provides(ITopLevelEntryLink)

    @property
    def __parent__(self):
        return getUtility(ICookbookSet)

    __name__ = "featured"

    link_name = "featured_cookbook"
    entry_type = ICookbook


@implementer(ICookbookSet)
class CookbookSet(CookbookTopLevelObject):
    """The set of all cookbooks."""

    grokcore.component.provides(ICookbookSet)

    __name__ = "cookbooks"

    def __init__(self, cookbooks=None):
        if cookbooks is None:
            cookbooks = COOKBOOKS
        self.cookbooks = list(cookbooks)
        self.featured = self.cookbooks[0]

    def getCookbooks(self):
        return self.cookbooks

    def get(self, name):
        match = [c for c in self.cookbooks if c.name == name]
        if len(match) > 0:
            return match[0]
        return None

    def find_recipes(self, search, vegetarian=False):
        recipes = []
        for cookbook in self.cookbooks:
            if not vegetarian or cookbook.cuisine == Cuisine.VEGETARIAN:
                recipes.extend(cookbook.find_recipes(search))
        return recipes

    def find_for_cuisine(self, cuisine):
        """See `ICookbookSet`"""
        cookbooks = []
        for cookbook in self.cookbooks:
            if cookbook.cuisine == cuisine:
                cookbooks.append(cookbook)
        return cookbooks

    def create(
        self,
        name,
        description,
        cuisine,
        copyright_date,
        last_printing=None,
        price=0,
    ):
        for cookbook in self.cookbooks:
            if cookbook.name == name:
                raise NameAlreadyTaken(
                    'A cookbook called "%s" already exists.' % name
                )
        cookbook = Cookbook(
            name, description, cuisine, copyright_date, last_printing, price
        )
        self.cookbooks.append(cookbook)
        return cookbook


@implementer(IDishSet)
class DishSet(CookbookTopLevelObject):
    """The set of all dishes."""

    grokcore.component.provides(IDishSet)

    __name__ = "dishes"

    def __init__(self, dishes=None):
        if dishes is None:
            dishes = DISHES
        self.dishes = list(dishes)

    def getDishes(self):
        return self.dishes

    def get(self, name):
        match = [d for d in self.dishes if d.name == name]
        if len(match) > 0:
            return match[0]
        return None


@implementer(IRecipeSet)
class RecipeSet(CookbookTopLevelObject):
    """The set of all recipes."""

    grokcore.component.provides(IRecipeSet)

    __name__ = "recipes"

    def __init__(self, recipes=None):
        if recipes is None:
            recipes = RECIPES
        self.recipes = list(recipes)

    def getRecipes(self):
        return self.recipes

    def get(self, id):
        id = int(id)
        match = [r for r in self.recipes if r.id == id]
        if len(match) > 0:
            return match[0]
        return None

    def createRecipe(self, id, cookbook, dish, instructions, private=False):
        recipe = Recipe(id, cookbook, dish, instructions, private=private)
        self.recipes.append(recipe)
        return recipe

    def removeRecipe(self, recipe):
        self.recipes.remove(recipe)
        removeSecurityProxy(recipe.cookbook).removeRecipe(recipe)
        removeSecurityProxy(recipe.dish).removeRecipe(recipe)


# Define some globally accessible sample data.
def year(year):
    """Turn a year into a datetime.date object."""
    return date(year, 1, 1)


C1 = Cookbook(
    "Mastering the Art of French Cooking", "", Cuisine.FRANCAISE, year(1961)
)
C2 = Cookbook("The Joy of Cooking", "", Cuisine.GENERAL, year(1995), price=20)
C3 = Cookbook(
    "James Beard's American Cookery", "", Cuisine.AMERICAN, year(1972)
)
C4 = Cookbook("Everyday Greens", "", Cuisine.VEGETARIAN, year(2003))
C5 = Cookbook("I'm Just Here For The Food", "", Cuisine.GENERAL, year(2002))
C6 = Cookbook("Cooking Without Recipes", "", Cuisine.GENERAL, year(1959))
C7 = Cookbook("Construsions un repas", "", Cuisine.FRANCAISE, year(2007))
COOKBOOKS = [C1, C2, C3, C4, C5, C6, C7]

D1 = Dish("Roast chicken")
C1_D1 = Recipe(1, C1, D1, "You can always judge...")
C2_D1 = Recipe(2, C2, D1, "Draw, singe, stuff, and truss...")
C3_D1 = Recipe(3, C3, D1, "A perfectly roasted chicken is...")

D2 = Dish("Baked beans")
C2_D2 = Recipe(4, C2, D2, "Preheat oven to...")
C3_D2 = Recipe(5, C3, D2, "Without doubt the most famous...", True)

D3 = Dish("Foies de voilaille en aspic")
C1_D3 = Recipe(6, C1, D3, "Chicken livers sauteed in butter...")

DISHES = [D1, D2, D3]
RECIPES = [C1_D1, C2_D1, C3_D1, C2_D2, C3_D2, C1_D3]


# Define classes for the service root.
@implementer(IHasGet)
class CookbookServiceRootResource(ServiceRootResource):
    """A service root for the cookbook web service.

    Traversal to top-level resources is handled with the get() method.
    The top-level objects are stored in the top_level_names dict.
    """

    @property
    def top_level_names(self):
        """Access or create the list of top-level objects."""
        return {
            "cookbooks": getUtility(ICookbookSet),
            "dishes": getUtility(IDishSet),
            "recipes": getUtility(IRecipeSet),
            "filemanager": getUtility(IFileManager),
        }

    def get(self, name):
        """Traverse to a top-level object."""
        obj = self.top_level_names.get(name)
        return obj


# Define the web service configuration.
class WebServiceConfiguration(BaseWebServiceConfiguration):
    directives.publication_class(WebServiceTestPublication)
    caching_policy = [10000, 2]
    code_revision = "test.revision"
    default_batch_size = 5
    hostname = "cookbooks.dev"
    match_batch_size = 50
    active_versions = ["1.0", "devel"]
    service_description = """<p>This is a web service.</p>
    <p>It's got resources!</p>"""
    version_descriptions = {
        "devel": """<p>The unstable development
    version.</p>

    <p>Don't use this unless you like changing things.</p>"""
    }
    last_version_with_mutator_named_operations = None
    first_version_with_total_size_link = None
    use_https = False
    view_permission = "lazr.restful.example.base.View"
