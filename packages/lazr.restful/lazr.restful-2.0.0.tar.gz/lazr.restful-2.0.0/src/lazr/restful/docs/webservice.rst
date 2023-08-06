********************
RESTful Web Services
********************

lazr.restful builds on Zope conventions to make it easy to expose your model
objects as RESTful HTTP resources. I'll demonstrate these features by defining
a model for managing recipes, and then publishing the model objects as
resources through a web service.

Example model objects
=====================

Here's the interface for a simple set of model objects. This is the
kind of model object you'd find in any Zope application, with no
special knowledge of web services. The model is of a group of
cookbooks. Each cookbook has a known person as the author. Each
cookbook contains multiple recipes. A recipe is a recipe _for_ a dish,
and two or more cookbooks may provide different recipes for the same
dish. Users may comment on cookbooks and on individual recipes.

    >>> from zope.interface import Interface, Attribute
    >>> from zope.schema import Bool, Bytes, Int, Text, TextLine
    >>> from lazr.restful.fields import Reference

    >>> class ITestDataObject(Interface):
    ...     """A marker interface for data objects."""
    ...     path = Attribute("The path portion of this object's URL. "
    ...                      "Defined here for simplicity of testing.")

    >>> class IAuthor(ITestDataObject):
    ...     name = TextLine(title="Name", required=True)
    ...     # favorite_recipe.schema will be set to IRecipe once
    ...     # IRecipe is defined.
    ...     favorite_recipe = Reference(schema=Interface)
    ...     popularity = Int(readonly=True)

    >>> class ICommentTarget(ITestDataObject):
    ...     comments = Attribute('List of comments about this object.')

    >>> class IComment(ITestDataObject):
    ...     target = Attribute('The object containing this comment.')
    ...     text = TextLine(title="Text", required=True)

    >>> class ICookbook(ICommentTarget):
    ...     name = TextLine(title="Name", required=True)
    ...     author = Reference(schema=IAuthor)
    ...     cuisine = TextLine(title="Cuisine", required=False, default=None)
    ...     recipes = Attribute("List of recipes published in this cookbook.")
    ...     cover = Bytes(0, 5000, title="An image of the cookbook's cover.")
    ...     def removeRecipe(recipe):
    ...         """Remove a recipe from this cookbook."""

    >>> class IDish(ITestDataObject):
    ...     name = TextLine(title="Name", required=True)
    ...     recipes = Attribute("List of recipes for this dish.")
    ...     def removeRecipe(recipe):
    ...         """Remove one of the recipes for this dish."""

    >>> class IRecipe(ICommentTarget):
    ...     id = Int(title="Unique ID", required=True)
    ...     dish = Reference(schema=IDish)
    ...     cookbook = Reference(schema=ICookbook)
    ...     instructions = Text(title="How to prepare the recipe.",
    ...         required=True)
    ...     private = Bool(title="Whether the public can see this recipe.",
    ...                    default=False)
    ...     def delete():
    ...         """Delete this recipe."""

    >>> IAuthor['favorite_recipe'].schema = IRecipe

Here's the interface for the 'set' objects that manage the authors,
cookbooks, and dishes. The inconsistent naming is intentional.

    >>> from lazr.restful.interfaces import ITraverseWithGet
    >>> class ITestDataSet(ITestDataObject, ITraverseWithGet):
    ...     """A marker interface."""

    >>> class IAuthorSet(ITestDataSet):
    ...     def getAllAuthors(self):
    ...         "Get all authors."
    ...
    ...     def get(self, request, name):
    ...         "Retrieve a single author by name."

    >>> class ICookbookSet(ITestDataSet):
    ...     def getAll(self):
    ...         "Get all cookbooks."
    ...
    ...     def get(self, request, name):
    ...         "Retrieve a single cookbook by name."
    ...
    ...     def findRecipes(self, name):
    ...         "Find recipes with a given name, across cookbooks."

    >>> class IDishSet(ITestDataSet):
    ...     def getAll(self):
    ...         "Get all dishes."
    ...
    ...     def get(self, request, name):
    ...         "Retrieve a single dish by name."


Here are simple implementations of IAuthor, IComment, ICookbook, IDish,
and IRecipe.

The web service uses the standard Zope protocol for mapping URLs to
object. So a URL is mapped to an object using the IPublishTraverse
interface, and the URL of an object is found by using the IAbsoluteURL
interface.


    >>> from urllib.parse import quote
    >>> from zope.component import (
    ...     adapter, getSiteManager, getMultiAdapter)
    >>> from zope.interface import implementer
    >>> from zope.publisher.interfaces import IPublishTraverse, NotFound
    >>> from zope.publisher.interfaces.browser import IBrowserRequest
    >>> from zope.security.checker import CheckerPublic
    >>> from zope.traversing.browser.interfaces import IAbsoluteURL
    >>> from lazr.restful.security import protect_schema

    >>> @implementer(IAbsoluteURL)
    ... class BaseAbsoluteURL:
    ...     """A basic, extensible implementation of IAbsoluteURL."""
    ...
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request
    ...
    ...     def __str__(self):
    ...         return "http://api.cookbooks.dev/beta/" + self.context.path
    ...
    ...     __call__ = __str__

    >>> sm = getSiteManager()
    >>> sm.registerAdapter(
    ...     BaseAbsoluteURL, [ITestDataObject, IBrowserRequest],
    ...     IAbsoluteURL)

    >>> @implementer(IAuthor)
    ... class Author:
    ...     def __init__(self, name):
    ...         self.name = name
    ...         self.favorite_recipe = None
    ...         self.popularity = 1
    ...
    ...     @property
    ...     def path(self):
    ...         return 'authors/' + quote(self.name)

    >>> protect_schema(Author, IAuthor, write_permission=CheckerPublic)

    >>> @implementer(IComment)
    ... class Comment:
    ...
    ...     def __init__(self, target, text):
    ...         self.target = target
    ...         self.text = text
    ...         self.target.comments.append(self)
    ...

    >>> protect_schema(Comment, IComment, write_permission=CheckerPublic)

    >>> @adapter(IComment, IBrowserRequest)
    ... class CommentAbsoluteURL(BaseAbsoluteURL):
    ...     """Code for generating the URL to a comment.
    ...
    ...     The URL is based on the URL of the ICommentTarget on which
    ...     this is a comment.
    ...     """
    ...
    ...     def __str__(self):
    ...         base = getMultiAdapter((self.context.target, request),
    ...                                IAbsoluteURL)()
    ...         return base + "/comments/%d" % (
    ...             self.context.target.comments.index(self.context)+1)
    ...     __call__ = __str__
    >>> sm.registerAdapter(CommentAbsoluteURL)

    >>> @implementer(ICookbook)
    ... class Cookbook:
    ...     def __init__(self, name, author, cuisine=None):
    ...         self.name = name
    ...         self.author = author
    ...         self.recipes = []
    ...         self.comments = []
    ...         self.cuisine = cuisine
    ...         self.cover = None
    ...
    ...     @property
    ...     def path(self):
    ...         return 'cookbooks/' + quote(self.name)
    ...
    ...     def removeRecipe(self, recipe):
    ...         self.recipes.remove(recipe)

    >>> protect_schema(Cookbook, ICookbook, write_permission=CheckerPublic)

    >>> from urllib.parse import unquote
    >>> @implementer(IPublishTraverse)
    ... @adapter(ICookbook, IBrowserRequest)
    ... class CookbookTraversal:
    ...     traversing = None
    ...
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...
    ...     def publishTraverse(self, request, name):
    ...         name = unquote(name)
    ...         if self.traversing is not None:
    ...             return getattr(self, 'traverse_' + self.traversing)(name)
    ...         elif name in ['comments', 'recipes']:
    ...             self.traversing = name
    ...             return self
    ...         else:
    ...             raise NotFound(self.context, name)
    ...
    ...     def traverse_comments(self, name):
    ...         try:
    ...             return self.context.comments[int(name)-1]
    ...         except (IndexError, TypeError, ValueError):
    ...             raise NotFound(self.context, 'comments/' + name)
    ...
    ...     def traverse_recipes(self, name):
    ...         name = unquote(name)
    ...         for recipe in self.context.recipes:
    ...             if recipe.dish.name == name:
    ...                 return recipe
    ...         raise NotFound(self.context, 'recipes/' + name)
    >>> protect_schema(CookbookTraversal, IPublishTraverse)
    >>> sm.registerAdapter(CookbookTraversal)

    >>> @implementer(IDish)
    ... class Dish:
    ...     def __init__(self, name):
    ...         self.name = name
    ...         self.recipes = []
    ...     @property
    ...     def path(self):
    ...         return 'dishes/' + quote(self.name)
    ...     def removeRecipe(self, recipe):
    ...         self.recipes.remove(recipe)

    >>> protect_schema(Dish, IDish, write_permission=CheckerPublic)

    >>> @implementer(IRecipe)
    ... class Recipe:
    ...     path = ''
    ...     def __init__(self, id, cookbook, dish, instructions,
    ...                  private=False):
    ...         self.id = id
    ...         self.cookbook = cookbook
    ...         self.cookbook.recipes.append(self)
    ...         self.dish = dish
    ...         self.dish.recipes.append(self)
    ...         self.instructions = instructions
    ...         self.comments = []
    ...         self.private = private
    ...     def delete(self):
    ...         self.cookbook.removeRecipe(self)
    ...         self.dish.removeRecipe(self)

    >>> protect_schema(Recipe, IRecipe, read_permission='zope.View',
    ...                write_permission=CheckerPublic)

    >>> @adapter(IRecipe, IBrowserRequest)
    ... class RecipeAbsoluteURL(BaseAbsoluteURL):
    ...     """Code for generating the URL to a recipe.
    ...
    ...     The URL is based on the URL of the cookbook to which
    ...     this recipe belongs.
    ...     """
    ...
    ...     def __str__(self):
    ...         base = getMultiAdapter((self.context.cookbook, request),
    ...                                IAbsoluteURL)()
    ...         return base + "/recipes/%s" % quote(self.context.dish.name)
    ...     __call__ = __str__
    >>> sm.registerAdapter(RecipeAbsoluteURL)

    >>> @adapter(IRecipe, IBrowserRequest)
    ... @implementer(IPublishTraverse)
    ... class RecipeTraversal:
    ...
    ...     saw_comments = False
    ...
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...
    ...     def publishTraverse(self, request, name):
    ...         name = unquote(name)
    ...         if self.saw_comments:
    ...             try:
    ...                 return self.context.comments[int(name)-1]
    ...             except (IndexError, TypeError, ValueError):
    ...                 raise NotFound(self.context, 'comments/' + name)
    ...         elif name == 'comments':
    ...             self.saw_comments = True
    ...             return self
    ...         else:
    ...             raise NotFound(self.context, name)
    >>> protect_schema(RecipeTraversal, IPublishTraverse)
    >>> sm.registerAdapter(RecipeTraversal)

Here are the "model objects" themselves:

    >>> A1 = Author("Julia Child")
    >>> A2 = Author("Irma S. Rombauer")
    >>> A3 = Author("James Beard")
    >>> AUTHORS = [A1, A2, A3]

    >>> C1 = Cookbook("Mastering the Art of French Cooking", A1)
    >>> C2 = Cookbook("The Joy of Cooking", A2)
    >>> C3 = Cookbook("James Beard's American Cookery", A3)
    >>> COOKBOOKS = [C1, C2, C3]

    >>> D1 = Dish("Roast chicken")
    >>> C1_D1 = Recipe(1, C1, D1, "You can always judge...")
    >>> C2_D1 = Recipe(2, C2, D1, "Draw, singe, stuff, and truss...")
    >>> C3_D1 = Recipe(3, C3, D1, "A perfectly roasted chicken is...")

    >>> D2 = Dish("Baked beans")
    >>> C2_D2 = Recipe(4, C2, D2, "Preheat oven to...")
    >>> C3_D2 = Recipe(5, C3, D2, "Without doubt the most famous...", True)

    >>> D3 = Dish("Foies de voilaille en aspic")
    >>> C1_D3 = Recipe(6, C1, D3, "Chicken livers sauteed in butter...")

    >>> COM1 = Comment(C2_D1, "Clear and concise.")
    >>> COM2 = Comment(C2, "A kitchen staple.")

    >>> A1.favorite_recipe = C1_D1
    >>> A2.favorite_recipe = C2_D2
    >>> A3.favorite_recipe = C3_D2

Here's a simple CookbookSet with a predefined list of cookbooks.

    >>> from lazr.restful.simple import TraverseWithGet
    >>> @implementer(ICookbookSet)
    ... class CookbookSet(BaseAbsoluteURL, TraverseWithGet):
    ...     path = 'cookbooks'
    ...
    ...     def __init__(self):
    ...         self.cookbooks = COOKBOOKS
    ...
    ...     def newCookbook(self, author_name, title, cuisine):
    ...         authors = AuthorSet()
    ...         author = authors.get(None, author_name)
    ...         if author is None:
    ...             author = authors.newAuthor(author_name)
    ...         cookbook = Cookbook(title, author, cuisine)
    ...         self.cookbooks.append(cookbook)
    ...         return cookbook
    ...
    ...     def getAll(self):
    ...         return self.cookbooks
    ...
    ...     def get(self, request, name):
    ...         match = [c for c in self.cookbooks if c.name == name]
    ...         if len(match) > 0:
    ...             return match[0]
    ...         return None
    ...
    ...     def findRecipes(self, name):
    ...         """Find recipes for a given dish across cookbooks."""
    ...         matches = []
    ...         for c in self.cookbooks:
    ...             for r in c.recipes:
    ...                 if r.dish.name == name:
    ...                     matches.append(r)
    ...                     break
    ...         # A somewhat arbitrary and draconian bit of error handling
    ...         # for the sake of demonstration.
    ...         if len(matches) == 0:
    ...             raise ValueError("No matches for %s" % name)
    ...         return matches

    >>> protect_schema(CookbookSet, ICookbookSet)
    >>> sm.registerUtility(CookbookSet(), ICookbookSet)

Here's a simple AuthorSet with predefined authors.

    >>> @implementer(IAuthorSet)
    ... class AuthorSet(BaseAbsoluteURL, TraverseWithGet):
    ...     path = 'authors'
    ...
    ...     def __init__(self):
    ...         self.authors = AUTHORS
    ...
    ...     def newAuthor(self, name):
    ...         author = Author(name)
    ...         self.authors.append(author)
    ...         return author
    ...
    ...     def getAllAuthors(self):
    ...         return self.authors
    ...
    ...     def get(self, request, name):
    ...         match = [p for p in self.authors if p.name == name]
    ...         if len(match) > 0:
    ...             return match[0]
    ...         return None

    >>> sm.registerAdapter(
    ...     TraverseWithGet, [ITestDataObject, IBrowserRequest])
    >>> protect_schema(AuthorSet, IAuthorSet)
    >>> sm.registerUtility(AuthorSet(), IAuthorSet)

Here's a vocabulary of authors, for a field that presents a Choice
among authors.

    >>> from zope.schema.interfaces import IVocabulary
    >>> @implementer(IVocabulary)
    ... class AuthorVocabulary:
    ...     def __iter__(self):
    ...         """Iterate over the authors."""
    ...         return AuthorSet().getAllAuthors().__iter__()
    ...
    ...     def __len__(self):
    ...         """Return the number of authors."""
    ...         return len(AuthorSet().getAllAuthors())
    ...
    ...     def getTerm(self, name):
    ...         """Retrieve an author by name."""
    ...         return AuthorSet().get(name)

Finally, a simple DishSet with predefined dishes.

    >>> @implementer(IDishSet)
    ... class DishSet(BaseAbsoluteURL, TraverseWithGet):
    ...     path = 'dishes'
    ...     def __init__(self):
    ...         self.dishes = [D1, D2, D3]
    ...
    ...     def getAll(self):
    ...         return self.dishes
    ...
    ...     def get(self, request, name):
    ...         match = [d for d in self.dishes if d.name == name]
    ...         if len(match) > 0:
    ...             return match[0]
    ...         return None

    >>> protect_schema(DishSet, IDishSet)
    >>> sm.registerUtility(DishSet(), IDishSet)

Security
========

The webservice uses the normal zope.security API to check for
permission. For this example, let's register a simple policy that
denies access to private recipes.

    >>> from zope.security.permission import Permission
    >>> from zope.security.management import setSecurityPolicy
    >>> from zope.security.simplepolicies import PermissiveSecurityPolicy
    >>> from zope.security.proxy import removeSecurityProxy

    >>> sm.registerUtility(Permission('zope.View'), name='zope.View')

    >>> class SimpleSecurityPolicy(PermissiveSecurityPolicy):
    ...     def checkPermission(self, permission, object):
    ...         if IRecipe.providedBy(object):
    ...             return not removeSecurityProxy(object).private
    ...         else:
    ...             return True

    >>> setSecurityPolicy(SimpleSecurityPolicy)
    <class ...>

Web Service Infrastructure Initialization
=========================================

The lazr.restful package contains a set of default adapters and
definitions to implement the web service.

    >>> from zope.configuration import xmlconfig
    >>> zcmlcontext = xmlconfig.string("""
    ... <configure xmlns="http://namespaces.zope.org/zope">
    ...   <include package="lazr.restful" file="basic-site.zcml"/>
    ...   <utility
    ...       factory="lazr.restful.example.base.filemanager.FileManager" />
    ... </configure>
    ... """)

A IWebServiceConfiguration utility is also expected to be defined which
defines common configuration option for the webservice.

    >>> from lazr.restful import directives
    >>> from lazr.restful.interfaces import IWebServiceConfiguration
    >>> from lazr.restful.simple import BaseWebServiceConfiguration
    >>> from lazr.restful.testing.webservice import WebServiceTestPublication

    >>> class WebServiceConfiguration(BaseWebServiceConfiguration):
    ...     hostname = 'api.cookbooks.dev'
    ...     use_https = False
    ...     active_versions = ['beta', 'devel']
    ...     code_revision = 'test'
    ...     max_batch_size = 100
    ...     directives.publication_class(WebServiceTestPublication)
    ...     first_version_with_total_size_link = 'devel'

    >>> from grokcore.component.testing import grok_component
    >>> ignore = grok_component(
    ...     'WebServiceConfiguration', WebServiceConfiguration)

    >>> from zope.component import getUtility
    >>> webservice_configuration = getUtility(IWebServiceConfiguration)

We also need to define a marker interface for each version of the web
service, so that incoming requests can be marked with the appropriate
version string. The configuration above defines two versions, 'beta'
and 'devel'.

    >>> from lazr.restful.interfaces import IWebServiceClientRequest
    >>> class IWebServiceRequestBeta(IWebServiceClientRequest):
    ...     pass

    >>> class IWebServiceRequestDevel(IWebServiceClientRequest):
    ...     pass

    >>> versions = ((IWebServiceRequestBeta, 'beta'),
    ...             (IWebServiceRequestDevel, 'devel'))

    >>> from lazr.restful import register_versioned_request_utility
    >>> for cls, version in versions:
    ...     register_versioned_request_utility(cls, version)


Defining the resources
======================

lazr.restful provides an interface, ``IEntry``, used by an individual model
object exposed through a specific resource. This interface defines only one
attribute ``schema`` which should contain a schema describing the data fields
available in the entry. The same kind of fields defined by a model interface
like ``IRecipe``. It is expected that the entry adapter also provides that
schema itself.

If there's not much to an interface, you can expose it through the web service
exactly as it's defined, by defining a class that inherits from both the
interface and ``IEntry``. Since ``IAuthor`` and ``IComment`` are so simple, we
can define ``IAuthorEntry`` and ``ICommentEntry`` very simply.

The only extra and unusual step we have to take is to annotate the interfaces
with human-readable names for the objects we're exposing.

    >>> from zope.interface import taggedValue
    >>> from lazr.restful.interfaces import IEntry, LAZR_WEBSERVICE_NAME
    >>> class IAuthorEntry(IAuthor, IEntry):
    ...     """The part of an author we expose through the web service."""
    ...     taggedValue(
    ...         LAZR_WEBSERVICE_NAME,
    ...         dict(
    ...             singular="author", plural="authors",
    ...             publish_web_link=True))

    >>> class ICommentEntry(IComment, IEntry):
    ...     """The part of a comment we expose through the web service."""
    ...     taggedValue(
    ...         LAZR_WEBSERVICE_NAME,
    ...         dict(
    ...             singular="comment", plural="comments",
    ...             publish_web_link=True))

Most of the time, it doesn't work to expose to the web service the same data
model we expose internally. Usually there are fields we don't want to expose,
synthetic fields we do want to expose, fields we want to expose as a different
type under a different name, and so on. This is why we have ``IEntry`` in the
first place: the ``IEntry`` interface defines the interface we _do_ want to
expose through the web service.

The reason we can't just define ``IDishEntry(IDish, IEntry)`` is that
``IDish`` defines the "recipes" collection as an ``Attribute``. ``Attribute``
is about as generic as "object", and doesn't convey any information about what
kind of object is in the collection, or even that "recipes" is a collection at
all. To expose the corresponding field to the web service we use
``CollectionField``.

    >>> from lazr.restful.fields import CollectionField
    >>> class IDishEntry(IEntry):
    ...     "The part of a dish that we expose through the web service."
    ...     recipes = CollectionField(value_type=Reference(schema=IRecipe))
    ...     taggedValue(
    ...         LAZR_WEBSERVICE_NAME,
    ...         dict(
    ...             singular="dish", plural="dishes",
    ...             publish_web_link=True))

In the following code block we define an interface that exposes the underlying
``Recipe``'s name but not its ID. References to associated objects (like the
recipe's cookbook) are represented with the ``zope.schema.Object`` type: this
makes it possible to serve a link from a recipe to its cookbook.

    >>> class IRecipeEntry(IEntry):
    ...     "The part of a recipe that we expose through the web service."
    ...     cookbook = Reference(schema=ICookbook)
    ...     dish = Reference(schema=IDish)
    ...     instructions = Text(title="Name", required=True)
    ...     comments = CollectionField(value_type=Reference(schema=IComment))
    ...     taggedValue(
    ...         LAZR_WEBSERVICE_NAME,
    ...         dict(
    ...             singular="recipe", plural="recipes",
    ...             publish_web_link=True))

    >>> from lazr.restful.fields import ReferenceChoice
    >>> class ICookbookEntry(IEntry):
    ...     name = TextLine(title="Name", required=True)
    ...     cuisine = TextLine(title="Cuisine", required=False, default=None)
    ...     author = ReferenceChoice(
    ...         schema=IAuthor, vocabulary=AuthorVocabulary())
    ...     recipes = CollectionField(value_type=Reference(schema=IRecipe))
    ...     comments = CollectionField(value_type=Reference(schema=IComment))
    ...     cover = Bytes(0, 5000, title="An image of the cookbook's cover.")
    ...     taggedValue(
    ...         LAZR_WEBSERVICE_NAME,
    ...         dict(
    ...             singular="cookbook", plural="cookbooks",
    ...             publish_web_link=True))

The ``author`` field is a choice between ``Author`` objects. To make sure
that the ``Author`` objects are properly marshalled to JSON, we need to
define an adapter to ``IFieldMarshaller``.

    >>> from zope.schema.interfaces import IChoice
    >>> from lazr.restful.marshallers import (
    ...     ObjectLookupFieldMarshaller)
    >>> from lazr.restful.interfaces import (
    ...     IFieldMarshaller, IWebServiceClientRequest)
    >>> sm.registerAdapter(
    ...     ObjectLookupFieldMarshaller,
    ...     [IChoice, IWebServiceClientRequest, AuthorVocabulary],
    ...     IFieldMarshaller)

Implementing the resources
==========================

Here's the implementation of ``IAuthorEntry``: a simple decorator on the
original model object. It subclasses ``Entry``, a simple base class that
defines a constructor. (See http://pypi.python.org/pypi/lazr.delegates for
more on ``delegate_to()``.)

    >>> from zope.component import adapter
    >>> from zope.interface.verify import verifyObject
    >>> from lazr.delegates import delegate_to
    >>> from lazr.restful import Entry
    >>> from lazr.restful.testing.webservice import FakeRequest

    >>> class FakeDict(dict):
    ...     def __init__(self, interface):
    ...         super().__init__()
    ...         self.interface = interface
    ...     def __getitem__(self, key):
    ...         return self.interface

    >>> @adapter(IAuthor)
    ... @delegate_to(IAuthorEntry)
    ... class AuthorEntry(Entry):
    ...     """An author, as exposed through the web service."""
    ...     schema = IAuthorEntry
    ...     # This dict is normally generated by lazr.restful, but since we
    ...     # create the adapters manually here, we need to do the same for
    ...     # this dict.
    ...     _orig_interfaces = FakeDict(IAuthor)

    >>> request = FakeRequest()
    >>> verifyObject(IAuthorEntry, AuthorEntry(A1, request))
    True

The ``schema`` attribute points to the interface class that defines the
attributes exposed through the web service. Above, ``schema`` is
``IAuthorEntry``, which exposes only ``name``.

``IEntry`` also defines an invariant that enforces that it can be adapted to
the interface defined in the schema attribute. This is usually not a problem,
since the schema is usually the interface itself.

    >>> IAuthorEntry.validateInvariants(AuthorEntry(A1, request))

But the invariant will complain if that isn't true.

    >>> @delegate_to(IAuthorEntry)
    ... class InvalidAuthorEntry(Entry):
    ...     schema = ICookbookEntry

    >>> verifyObject(IAuthorEntry, InvalidAuthorEntry(A1, request))
    True
    >>> IAuthorEntry.validateInvariants(InvalidAuthorEntry(A1, request))
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
      ...
    zope.interface.exceptions.Invalid: InvalidAuthorEntry doesn't provide its ICookbookEntry schema.

Other entries are defined similarly.

    >>> @delegate_to(ICookbookEntry)
    ... class CookbookEntry(Entry):
    ...     """A cookbook, as exposed through the web service."""
    ...     schema = ICookbookEntry
    ...     # This dict is normally generated by lazr.restful, but since we
    ...     # create the adapters manually here, we need to do the same for
    ...     # this dict.
    ...     _orig_interfaces = FakeDict(ICookbook)

    >>> @delegate_to(IDishEntry)
    ... class DishEntry(Entry):
    ...     """A dish, as exposed through the web service."""
    ...     schema = IDishEntry
    ...     # This dict is normally generated by lazr.restful, but since we
    ...     # create the adapters manually here, we need to do the same for
    ...     # this dict.
    ...     _orig_interfaces = FakeDict(IDish)

    >>> @delegate_to(ICommentEntry)
    ... class CommentEntry(Entry):
    ...     """A comment, as exposed through the web service."""
    ...     schema = ICommentEntry
    ...     # This dict is normally generated by lazr.restful, but since we
    ...     # create the adapters manually here, we need to do the same for
    ...     # this dict.
    ...     _orig_interfaces = FakeDict(IComment)

    >>> @delegate_to(IRecipeEntry)
    ... class RecipeEntry(Entry):
    ...     schema = IRecipeEntry
    ...     # This dict is normally generated by lazr.restful, but since we
    ...     # create the adapters manually here, we need to do the same for
    ...     # this dict.
    ...     _orig_interfaces = FakeDict(IRecipe)

We need to register these entries as a multiadapter adapter from
(e.g.) ``IAuthor`` and ``IWebServiceClientRequest`` to (e.g.)
``IAuthorEntry``. In ZCML a registration would look like this::

    <adapter for="my.app.rest.IAuthor
                  lazr.restful.interfaces.IWebServiceClientRequest"
             factory="my.app.rest.AuthorEntry" />

Since we're in the middle of a Python example we can do the equivalent
in Python code for each entry class:

    >>> for entry_class, adapts_interface, provided_interface in [
    ...     [AuthorEntry, IAuthor, IAuthorEntry],
    ...     [CookbookEntry, ICookbook, ICookbookEntry],
    ...     [DishEntry, IDish, IDishEntry],
    ...     [CommentEntry, IComment, ICommentEntry],
    ...     [RecipeEntry, IRecipe, IRecipeEntry]]:
    ...         sm.registerAdapter(
    ...             entry_class, [adapts_interface, IWebServiceClientRequest],
    ...             provided=provided_interface)

lazr.restful also defines an interface and a base class for collections of
objects. I'll use it to expose the ``AuthorSet`` collection and other
top-level collections through the web service. A collection must define a
method called find(), which returns the model objects in the collection.

    >>> from lazr.restful import Collection
    >>> from lazr.restful.interfaces import ICollection

    >>> class AuthorCollection(Collection):
    ...     """A collection of authors, as exposed through the web service."""
    ...
    ...     entry_schema = IAuthorEntry
    ...
    ...     def find(self):
    ...        """Find all the authors."""
    ...        return self.context.getAllAuthors()

    >>> sm.registerAdapter(AuthorCollection,
    ...                   (IAuthorSet, IWebServiceClientRequest),
    ...                   provided=ICollection)

    >>> verifyObject(ICollection, AuthorCollection(AuthorSet(), request))
    True

    >>> @adapter(ICookbookSet)
    ... class CookbookCollection(Collection):
    ...     """A collection of cookbooks, as exposed through the web service.
    ...     """
    ...
    ...     entry_schema = ICookbookEntry
    ...
    ...     def find(self):
    ...        """Find all the cookbooks."""
    ...        return self.context.getAll()
    >>> sm.registerAdapter(CookbookCollection,
    ...                   (ICookbookSet, IWebServiceClientRequest),
    ...                   provided=ICollection)

    >>> @adapter(IDishSet)
    ... class DishCollection(Collection):
    ...     """A collection of dishes, as exposed through the web service."""
    ...
    ...     entry_schema = IDishEntry
    ...
    ...     def find(self):
    ...        """Find all the dishes."""
    ...        return self.context.getAll()

    >>> sm.registerAdapter(DishCollection,
    ...                   (IDishSet, IWebServiceClientRequest),
    ...                   provided=ICollection)

Like ``Entry``, ``Collection`` is a simple base class that defines a
constructor. The ``entry_schema`` attribute gives a ``Collection`` class
knowledge about what kind of entry it's supposed to contain.

    >>> DishCollection.entry_schema
    <InterfaceClass __builtin__.IDishEntry>

We also need to define a collection of the recipes associated with a cookbook.
We say that the collection of recipes is scoped to a cookbook. Scoped
collections adapters are looked for based on the type of the scope, and the
type of the entries contained in the scoped collection. There is a default
``ScopedCollection`` adapter that works whenever the scoped collection is
available as an iterable attribute of the context.

    >>> from lazr.restful.interfaces import IScopedCollection

    >>> def scope_collection(parent, child, name):
    ...     """A helper method that simulates a scoped collection lookup."""
    ...     parent_entry = getMultiAdapter((parent, request), IEntry)
    ...     child_entry = getMultiAdapter((child, request), IEntry)
    ...     scoped = getMultiAdapter((parent_entry, child_entry, request),
    ...                               IScopedCollection)
    ...     scoped.relationship = parent_entry.schema.get(name)
    ...     return scoped

The default adapter works just fine with the collection of recipes for
a cookbook.

    >>> scoped_collection = scope_collection(C1, C1_D1, 'recipes')
    >>> scoped_collection
    <lazr.restful...ScopedCollection...>

Like a regular collection, a scoped collection knows what kind of object is
inside it. Recall that the 'recipes' collection of a cookbook was defined as
one that contains objects with a schema of ``IRecipe``. This information is
available to the ``ScopedCollection`` object.

    >>> scoped_collection.entry_schema
    <InterfaceClass __builtin__.IRecipeEntry>

Field ordering
--------------

When an entry's fields are modified, it's important that the
modifications happen in a deterministic order, to minimize (or at
least make deterministic) bad interactions between fields. The helper
function get_entry_fields_in_write_order() handles this.

Ordinarily, fields are written to in the same order they are found in
the underlying schema.

    >>> author_entry = getMultiAdapter((A1, request), IEntry)
    >>> from lazr.restful._resource import get_entry_fields_in_write_order
    >>> def print_fields_in_write_order(entry):
    ...     for name, field in get_entry_fields_in_write_order(entry):
    ...         print(name)

    >>> print_fields_in_write_order(author_entry)
    name
    favorite_recipe
    popularity

The one exception is if a field is wrapped in a subclass of the
Passthrough class defined by the lazr.delegates library. Classes
generated through lazr.restful's annotations use a Passthrough
subclass to control a field that triggers complex logic when its value
changes. To minimize the risk of bad interactions, all the simple
fields are changed before any of the complex fields.

Here's a simple subclass of Passthrough.

    >>> from lazr.delegates import Passthrough
    >>> class MyPassthrough(Passthrough):
    ...     pass

When we replace 'favorite_recipe' with an instance of this subclass,
that field shows up at the end of the list of fields.

    >>> old_favorite_recipe = AuthorEntry.favorite_recipe
    >>> AuthorEntry.favorite_recipe = MyPassthrough('favorite_recipe', A1)
    >>> print_fields_in_write_order(author_entry)
    name
    popularity
    favorite_recipe

When we replace 'name' with a Passthrough subclass, it also shows up
at the end--but it still shows up before 'favorite_recipe', because it
comes before 'favorite_recipe' in the schema.

    >>> old_name = AuthorEntry.name
    >>> AuthorEntry.name = MyPassthrough('name', A1)
    >>> print_fields_in_write_order(author_entry)
    popularity
    name
    favorite_recipe

Cleanup to restore the old AuthorEntry implementation:

    >>> AuthorEntry.favorite_recipe = old_favorite_recipe
    >>> AuthorEntry.name = old_name

Custom operations
=================

The ``CookbookSet`` class defines a method called 'findRecipes'. This is
exposed through the cookbook collection resource as a custom operation called
``find_recipes``. Each custom operation is implemented as a class that
implements ``IResourceGETOperation``.

    >>> from lazr.restful import ResourceGETOperation
    >>> from zope.publisher.interfaces.http import IHTTPApplicationRequest
    >>> from lazr.restful.fields import Reference
    >>> from lazr.restful.interfaces import IResourceGETOperation
    >>> @implementer(IResourceGETOperation)
    ... @adapter(ICookbookSet, IHTTPApplicationRequest)
    ... class FindRecipesOperation(ResourceGETOperation):
    ...    """An operation that searches for recipes across cookbooks."""
    ...
    ...    params = [ TextLine(__name__='name') ]
    ...    return_type = CollectionField(value_type=Reference(schema=IRecipe))
    ...
    ...    def call(self, name):
    ...        try:
    ...            return self.context.findRecipes(name)
    ...        except ValueError as e:
    ...            self.request.response.setStatus(400)
    ...            return str(e)

To register the class we just defined as implementing the ``find_recipes``
operation, we need to register it as a named adapter providing
``IResourceGETOperation`` for the ``ICookbookSet`` interface.

    >>> sm.registerAdapter(FindRecipesOperation, name="find_recipes")

The same underlying method is exposed through the recipe entry
resource as a custom operation called ``find_similar_recipes``.

    >>> @implementer(IResourceGETOperation)
    ... @adapter(IRecipe, IHTTPApplicationRequest)
    ... class FindSimilarRecipesOperation(ResourceGETOperation):
    ...    """Finds recipes with the same name."""
    ...    params = []
    ...    return_type = CollectionField(value_type=Reference(schema=IRecipe))
    ...
    ...    def call(self):
    ...        try:
    ...            return CookbookSet().findRecipes(self.context.dish.name)
    ...        except AssertionError as e:
    ...            self.request.response.setStatus(400)
    ...            return str(e)

    >>> sm.registerAdapter(
    ...     FindSimilarRecipesOperation, name="find_similar_recipes")

Named GET operations are read-only operations like searches, but
resources can also expose named write operations, through POST. Here's
a named factory operation for creating a new cookbook.

    >>> from lazr.restful.interfaces import IResourcePOSTOperation
    >>> from lazr.restful import ResourcePOSTOperation
    >>> @implementer(IResourcePOSTOperation)
    ... @adapter(ICookbookSet, IHTTPApplicationRequest)
    ... class CookbookFactoryOperation(ResourcePOSTOperation):
    ...     """An operation that creates a new cookbook."""
    ...     params = (
    ...         TextLine(__name__='author_name'),
    ...         TextLine(__name__='title'),
    ...         TextLine(
    ...             __name__='cuisine', default='Brazilian', required=False),
    ...     )
    ...     return_type = Reference(schema=IRecipe)
    ...
    ...     def call(self, author_name, title, cuisine):
    ...         cookbook = CookbookSet().newCookbook(
    ...             author_name, title, cuisine)
    ...         self.request.response.setStatus(201)
    ...         self.request.response.setHeader(
    ...             "Location", absoluteURL(cookbook, self.request))
    ...         return cookbook

    >>> sm.registerAdapter(
    ...     CookbookFactoryOperation, name="create_cookbook")

Here's a named POST operation that's not a factory operation: it makes a
cookbook's cuisine sound more interesting.

    >>> @implementer(IResourcePOSTOperation)
    ... @adapter(ICookbook, IHTTPApplicationRequest)
    ... class MakeMoreInterestingOperation(ResourcePOSTOperation):
    ...     params = ()
    ...     return_type = None
    ...     send_modification_event = True
    ...
    ...     def call(self):
    ...         cookbook = self.context
    ...         cookbook.cuisine = "Nouvelle " + cookbook.cuisine

    >>> sm.registerAdapter(
    ...     MakeMoreInterestingOperation, name="make_more_interesting")

Operations are also used to implement DELETE on entries. This code
implements DELETE for IRecipe objects.

    >>> from lazr.restful.interfaces import IResourceDELETEOperation
    >>> from lazr.restful import ResourceDELETEOperation
    >>> @implementer(IResourceDELETEOperation)
    ... @adapter(IRecipe, IHTTPApplicationRequest)
    ... class RecipeDeleteOperation(ResourceDELETEOperation):
    ...     params = ()
    ...     return_type = None
    ...
    ...     def call(self):
    ...         self.context.delete()
    >>> sm.registerAdapter(
    ...     RecipeDeleteOperation, name="")


Resource objects
================

lazr.restful ``Resource`` objects are the objects that actually handle
incoming HTTP requests. There are a few very common types of HTTP resources,
and LAZR defines classes for some of them. For instance, there's the
"collection" resource that responds to GET (to get the items in the
collection) and POST (to invoke named operations on the collection).
lazr.restful implements this as a ``CollectionResource`` which uses the HTTP
arguments to drive ``Collection`` methods like find().

Of course, a ``CollectionResource`` has to expose a collection _of_
something. That's why each ``CollectionResource`` is associated with some
concrete implementation of ``ICollection``, like ``AuthorCollection``. All you
have to do is define the behaviour of the collection, and
``CollectionResource`` takes care of exposing the collection through HTTP.

Similarly, you can implement ``RecipeEntry`` to the ``IEntry`` interface, and
expose it through the web as an ``EntryResource``.

The Service Root Resource
=========================

How are these ``Resource`` objects connected to the web? Through the
``ServiceRootResource``. This is a special resource that represents the
root of the object tree.

    >>> from lazr.restful.interfaces import IServiceRootResource
    >>> from lazr.restful import ServiceRootResource
    >>> from zope.traversing.browser.interfaces import IAbsoluteURL

    >>> @implementer(IAbsoluteURL)
    ... class MyServiceRootResource(ServiceRootResource, TraverseWithGet):
    ...     path = ''
    ...
    ...     top_level_names = {
    ...         'dishes': DishSet(),
    ...         'cookbooks': CookbookSet(),
    ...         'authors': AuthorSet()}
    ...
    ...     def get(self, request, name):
    ...         return self.top_level_names.get(name)

It's the responsibility of each web service to provide an implementation of
``IAbsoluteURL`` and ``IPublishTraverse`` for their service root resource.

    >>> sm.registerAdapter(
    ...     BaseAbsoluteURL, [MyServiceRootResource, IBrowserRequest])

    >>> app = MyServiceRootResource()
    >>> sm.registerUtility(app, IServiceRootResource)

If you call the service root resource, and pass in an HTTP request, it
will act as though you had performed a GET on the URL
'http://api.cookbooks.dev/beta/'.

    >>> webservice_configuration.root = app
    >>> from lazr.restful.testing.webservice import (
    ...     create_web_service_request)

    >>> request = create_web_service_request('/beta/')
    >>> ignore = request.traverse(app)

The response document is a JSON document full of links to the
top-level collections of authors, cookbooks, and dishes. It's the
'home page' for the web service.

    >>> import simplejson
    >>> response = app(request)
    >>> representation = simplejson.loads(response)

    >>> print(representation["authors_collection_link"])
    http://api.cookbooks.dev/beta/authors

    >>> print(representation["cookbooks_collection_link"])
    http://api.cookbooks.dev/beta/cookbooks

    >>> print(representation["dishes_collection_link"])
    http://api.cookbooks.dev/beta/dishes

The standard ``absoluteURL()`` function can be used to generate URLs to
content objects published on the web service. It works for the web service
root, so long as you've given it an ``IAbsoluteURL`` implementation.

    >>> from zope.traversing.browser import absoluteURL
    >>> absoluteURL(app, request)
    'http://api.cookbooks.dev/beta/'

WADL documents
==============

Every resource can serve a WADL representation of itself. The main
WADL document is the WADL representation of the server root. It
describes the capabilities of the web service as a whole.

    >>> wadl_headers = {'HTTP_ACCEPT' : 'application/vd.sun.wadl+xml'}
    >>> wadl_request = create_web_service_request(
    ...     '/beta/', environ=wadl_headers)
    >>> wadl_resource = wadl_request.traverse(app)
    >>> print(wadl_resource(wadl_request).decode('UTF-8'))
    <?xml version="1.0"?>
    <!DOCTYPE...
    <wadl:application ...>
    ...
    </wadl:application>

If the resources are improperly configured, the WADL can't be generated.
Here's an example, where ``DishCollection`` is registered as an adapter twice.
Earlier it was registered as the adapter for ``IDishSet``; here it's also
registered as the adapter for ``IAuthorSet``. The WADL generation doesn't know
whether to describe ``DishCollection`` using the named operations defined
against ``IAuthorSet`` or the named operations defined against ``IDishSet``,
so there's an ``AssertionError``.

    >>> sm.registerAdapter(DishCollection, [IAuthorSet], ICollection)
    >>> print(wadl_resource(wadl_request))
    Traceback (most recent call last):
    ...
    AssertionError: There must be one (and only one) adapter
    from DishCollection to ICollection.

Collection resources
====================

The default root navigation defined in our model contains the top-level
Set objects that should be published. When these sets are published on
the web service, they will we wrapped in the appropriate
``CollectionResource``.

The following example is equivalent to requesting
'http://api.cookbooks.dev/cookbooks/'. The code will traverse to the
``CookbookSet`` published normally at '/cookbooks' and it will be wrapped into
a ``CollectionResource``.

    >>> request = create_web_service_request('/beta/cookbooks')
    >>> collection = request.traverse(app)
    >>> collection
    <lazr.restful...CollectionResource object ...>

Calling the collection resource yields a JSON document, which can be
parsed with standard tools.

    >>> def load_json(s):
    ...     """Convert a JSON string to Unicode and then load it."""
    ...     return simplejson.loads(s)

    >>> representation = load_json(collection())
    >>> print(representation['resource_type_link'])
    http://api.cookbooks.dev/beta/#cookbooks

Pagination
==========

``Collections`` are paginated and served one page at a time. This particular
collection is small enough to fit on one page; it's only got three entries.

    >>> for key in sorted(representation.keys()):
    ...     print(key)
    entries
    resource_type_link
    start
    total_size
    >>> len(representation['entries'])
    3
    >>> representation['total_size']
    3

But if we ask for a page size of two, we can see how pagination
works. Here's page one, with two cookbooks on it.

    >>> request = create_web_service_request(
    ...     '/beta/cookbooks', environ={'QUERY_STRING' : 'ws.size=2'})
    >>> collection = request.traverse(app)
    >>> representation = load_json(collection())

    >>> for key in sorted(representation.keys()):
    ...     print(key)
    entries
    next_collection_link
    resource_type_link
    start
    total_size
    >>> print(representation['next_collection_link'])
    http://api.cookbooks.dev/beta/cookbooks?ws.size=2&memo=2&ws.start=2
    >>> len(representation['entries'])
    2
    >>> representation['total_size']
    3

Follow the ``next_collection_link`` and you'll end up at page two, which
has the last cookbook on it.

    >>> request = create_web_service_request(
    ...     '/beta/cookbooks',
    ...     environ={'QUERY_STRING' : 'ws.start=2&ws.size=2'})
    >>> collection = request.traverse(app)
    >>> representation = load_json(collection())

    >>> for key in sorted(representation.keys()):
    ...     print(key)
    entries
    prev_collection_link
    resource_type_link
    start
    total_size
    >>> print(representation['prev_collection_link'])
    http://api.cookbooks.dev/beta/cookbooks?ws.size=2&direction=backwards&memo=2
    >>> len(representation['entries'])
    1

Custom operations
=================

A collection may also expose a number of custom operations through
GET. The cookbook collection exposes a custom GET operation called
``find_recipes``, which searches for recipes with a given name across
cookbooks.

    >>> request = create_web_service_request(
    ...    '/beta/cookbooks',
    ...    environ={'QUERY_STRING' :
    ...             'ws.op=find_recipes&name=Roast%20chicken'})
    >>> operation_resource = request.traverse(app)
    >>> chicken_recipes = load_json(operation_resource())
    >>> for instruction in sorted(
    ...         [c['instructions'] for c in chicken_recipes['entries']]):
    ...     print(instruction)
    A perfectly roasted chicken is...
    Draw, singe, stuff, and truss...
    You can always judge...

Custom operations may include custom error checking. Error messages
are passed along to the client.

    >>> request = create_web_service_request(
    ...    '/beta/cookbooks',
    ...    environ={'QUERY_STRING' :
    ...             'ws.op=find_recipes&name=NoSuchRecipe'})
    >>> operation_resource = request.traverse(app)
    >>> print(operation_resource())
    No matches for NoSuchRecipe

Collections may also support named POST operations. These requests
have two effects on the server side: they modify the dataset, and they
may also trigger event notifications. Here are two simple handlers set
up to print a message whenever we modify a cookbook or the cookbook
set.

    >>> def modified_cookbook(object, event):
    ...     """Print a message when triggered."""
    ...     print("You just modified a cookbook.")

    >>> from lazr.lifecycle.interfaces import IObjectModifiedEvent
    >>> from lazr.restful.testing.event import TestEventListener
    >>> cookbook_listener = TestEventListener(
    ...     ICookbook, IObjectModifiedEvent, modified_cookbook)

    >>> def modified_cookbook_set(object, event):
    ...     """Print a message when triggered."""
    ...     print("You just modified the cookbook set.")

Here we create a new cookbook for an existing author. Because the
operation's definition doesn't set send_modified_event to True, no
event will be sent and modified_cookbook_set() won't be called.

    >>> body = (b"ws.op=create_cookbook&title=Beard%20on%20Bread&"
    ...         b"author_name=James%20Beard")
    >>> request = create_web_service_request(
    ...     '/beta/cookbooks', 'POST', body,
    ...     {'CONTENT_TYPE' : 'application/x-www-form-urlencoded'})
    >>> operation_resource = request.traverse(app)
    >>> result = operation_resource()

    >>> request.response.getStatus()
    201
    >>> request.response.getHeader('Location')
    'http://api.cookbooks.dev/beta/cookbooks/Beard%20on%20Bread'

Here we create a cookbook for a new author.

    >>> body = (b"ws.op=create_cookbook&title=Everyday%20Greens&"
    ...         b"author_name=Deborah%20Madison")
    >>> request = create_web_service_request(
    ...     '/beta/cookbooks', 'POST', body,
    ...     {'CONTENT_TYPE' : 'application/x-www-form-urlencoded'})
    >>> operation_resource = request.traverse(app)
    >>> result = operation_resource()
    >>> request.response.getStatus()
    201
    >>> request.response.getHeader('Location')
    'http://api.cookbooks.dev/beta/cookbooks/Everyday%20Greens'

The new Author object is created implicitly and is published as a
resource afterwards.

    >>> path = '/beta/authors/Deborah%20Madison'
    >>> request = create_web_service_request(path)
    >>> author = request.traverse(app)
    >>> print(load_json(author())['name'])
    Deborah Madison

Here we modify a cookbook's cuisine using a named operation. Because
this operation's definition does set send_modified_event to True, an
event will be sent and modified_cookbook_set() will be called.

    >>> body = b"ws.op=make_more_interesting"
    >>> request = create_web_service_request(
    ...     '/beta/cookbooks/Everyday%20Greens', 'POST', body,
    ...     {'CONTENT_TYPE' : 'application/x-www-form-urlencoded'})
    >>> operation_resource = request.traverse(app)
    >>> result = operation_resource()
    You just modified a cookbook.
    >>> request.response.getStatus()
    200

    >>> path = '/beta/cookbooks/Everyday%20Greens'
    >>> request = create_web_service_request(path)
    >>> cookbook = request.traverse(app)
    >>> print(load_json(cookbook())['cuisine'])
    Nouvelle Brazilian


Entry resources
===============

The collection resource is a list of entries. Each entry has some
associated information (like 'name'), a ``self_link`` (the URL to the
entry's resource), and possibly links to associated resources.

    >>> import operator
    >>> request = create_web_service_request('/beta/cookbooks')
    >>> collection = request.traverse(app)
    >>> representation = load_json(collection())
    >>> entries = sorted(representation['entries'],
    ...                  key=operator.itemgetter('name'))
    >>> print(entries[0]['self_link'])
    http://api.cookbooks.dev/beta/cookbooks/Beard%20on%20Bread

Regular data fields are exposed with their given names. The 'name'
field stays 'name'.

    >>> print(entries[0]['name'])
    Beard on Bread

Fields that are references to other objects -- ``Object``, ``Reference``, and
``ReferenceChoice`` -- are exposed as links to those objects. Each cookbook
has such a link to its author.

    >>> print(entries[0]['author_link'])
    http://api.cookbooks.dev/beta/authors/James%20Beard

Fields that are references to externally hosted files (Bytes) are also
exposed as links to those files. Each cookbook has such a link to its
cover image.

    >>> print(entries[0]['cover_link'])
    http://api.cookbooks.dev/beta/cookbooks/Beard%20on%20Bread/cover

Fields that are references to collections of objects are exposed as
links to those collections. Each cookbook has such a link to its
recipes.

    >>> print(entries[0]['recipes_collection_link'])
    http://api.cookbooks.dev/beta/cookbooks/Beard%20on%20Bread/recipes

Calling the ``CollectionResource`` object makes it process the incoming
request. Since this is a GET request, calling the resource publishes the
resource to the web. A ``CollectionResource`` is made up of a bunch of
``EntryResources``, and the base ``EntryResource`` class knows how to use the
entry schema class (in this case, ``IRecipeEntry``) to publish a JSON
document.

The same way collections are wrapped into ``CollectionResource``, navigating
to an object that has an ``IEntry`` adapter, will wrap it into an
``EntryResource``.

For instance, creating a new cookbook and making a request to its URL
will wrap it into an ``EntryResource``.

    >>> body = (b"ws.op=create_cookbook&title=Feijoada&"
    ...         b"author_name=Fernando%20Yokota")
    >>> request = create_web_service_request(
    ...     '/beta/cookbooks', 'POST', body,
    ...     {'CONTENT_TYPE' : 'application/x-www-form-urlencoded'})
    >>> operation_resource = request.traverse(app)
    >>> result = operation_resource()
    >>> request.response.getHeader('Location')
    'http://api.cookbooks.dev/beta/cookbooks/Feijoada'
    >>> request = create_web_service_request('/beta/cookbooks/Feijoada')
    >>> feijoada_resource = request.traverse(app)
    >>> feijoada_resource
    <lazr.restful...EntryResource object ...>
    >>> feijoada = load_json(feijoada_resource())

Notice how the request above didn't specify the book's cuisine,
but since that is not a required field our application used the default
value (Brazilian) specified in ``CookbookFactoryOperation`` for it.

    >>> from lazr.restful.testing.webservice import (
    ...     pprint_collection,
    ...     pprint_entry,
    ...     )

    >>> pprint_entry(feijoada)
    author_link: 'http://api.cookbooks.dev/beta/authors/Fernando%20Yokota'
    comments_collection_link:
        'http://api.cookbooks.dev/beta/cookbooks/Feijoada/comments'
    cover_link: 'http://api.cookbooks.dev/beta/cookbooks/Feijoada/cover'
    cuisine: 'Brazilian'
    name: 'Feijoada'
    recipes_collection_link:
        'http://api.cookbooks.dev/beta/cookbooks/Feijoada/recipes'
    resource_type_link: 'http://api.cookbooks.dev/beta/#cookbook'
    self_link: 'http://api.cookbooks.dev/beta/cookbooks/Feijoada'

You can also traverse from an entry to an item in a scoped collection:

    >>> request = create_web_service_request(
    ...     quote('/beta/cookbooks/The Joy of Cooking/recipes/Roast chicken'))
    >>> chicken_recipe_resource = request.traverse(app)
    >>> chicken_recipe = load_json(chicken_recipe_resource())
    >>> pprint_entry(chicken_recipe)
    comments_collection_link:
        'http://api...Joy%20of%20Cooking/recipes/Roast%20chicken/comments'
    cookbook_link:
        'http://api.cookbooks.dev/beta/cookbooks/The%20Joy%20of%20Cooking'
    dish_link: 'http://api.cookbooks.dev/beta/dishes/Roast%20chicken'
    instructions: 'Draw, singe, stuff, and truss...'
    self_link: 'http://api.../The%20Joy%20of%20Cooking/recipes/Roast%20chicken'

Another example traversing to a comment:

    >>> roast_chicken_comments_url = quote(
    ... '/beta/cookbooks/The Joy of Cooking/recipes/Roast chicken/comments')
    >>> request = create_web_service_request(roast_chicken_comments_url)
    >>> comments_resource = request.traverse(app)

    >>> comments = load_json(comments_resource())
    >>> for c in comments['entries']:
    ...     print(c['text'])
    Clear and concise.

    >>> request = create_web_service_request(
    ...     roast_chicken_comments_url + '/1')
    >>> comment_one_resource = request.traverse(app)
    >>> comment_one = load_json(comment_one_resource())
    >>> pprint_entry(comment_one)
    resource_type_link: 'http://api.cookbooks.dev/beta/#comment'
    self_link:
        'http://api...Joy%20of%20Cooking/recipes/Roast%20chicken/comments/1'
    text: 'Clear and concise.'

An entry may expose a number of custom operations through GET. The
recipe entry exposes a custom GET operation called
'find_similar_recipes', which searches for recipes with the same name
across cookbooks.

    >>> request = create_web_service_request(
    ...     '/beta/cookbooks/The%20Joy%20of%20Cooking/recipes/Roast%20chicken',
    ...     environ={'QUERY_STRING' : 'ws.op=find_similar_recipes'})
    >>> operation_resource = request.traverse(app)
    >>> chicken_recipes = load_json(operation_resource())
    >>> for instruction in sorted(
    ...         [c['instructions'] for c in chicken_recipes['entries']]):
    ...     print(instruction)
    A perfectly roasted chicken is...
    Draw, singe, stuff, and truss...
    You can always judge...

Named operation return values
=============================

The return value of a named operation is serialized to a JSON data
structure, and the response's Content-Type header is set to
application/json. These examples show how different return values are
serialized.

    >>> class SampleOperation(ResourceGETOperation):
    ...
    ...     params = ()
    ...     result = None
    ...     return_type = None
    ...
    ...     def call(self):
    ...         return self.result

    >>> def make_sample_operation_request(result):
    ...    request = create_web_service_request('/beta/')
    ...    ignore = request.traverse(app)
    ...    operation = SampleOperation(None, request)
    ...    operation.result = result
    ...    return request, operation

Scalar Python values like strings and booleans are serialized as you'd
expect.

    >>> request, operation = make_sample_operation_request("A string.")
    >>> print(operation())
    "A string."
    >>> request.response.getStatus()
    200
    >>> print(request.response.getHeader('Content-Type'))
    application/json

    >>> request, operation = make_sample_operation_request(True)
    >>> operation()
    'true'

    >>> request, operation = make_sample_operation_request(10)
    >>> operation()
    '10'

    >>> request, operation = make_sample_operation_request(None)
    >>> operation()
    'null'

    >>> request, operation = make_sample_operation_request(1.3)
    >>> operation()
    '1.3'

When a named operation returns an object that has an ``IEntry``
implementation, the object is serialized to a JSON hash.

    >>> request, operation = make_sample_operation_request(D2)
    >>> operation()
    '{...}'

A named operation can return a data structure that incorporates
objects with ``IEntry`` implementations. Here's a dictionary that contains
a ``Dish`` object. The ``Dish`` object is serialized as a JSON dictionary
within the larger dictionary.

    >>> request, operation = make_sample_operation_request({'dish': D2})
    >>> operation()
    '{"dish": {...}}'

When a named operation returns a list or tuple of objects, we serve
the whole thing as a JSON list.

    >>> request, operation = make_sample_operation_request([1,2,3])
    >>> operation()
    '[1, 2, 3]'

    >>> request, operation = make_sample_operation_request((C1_D1, C2_D1))
    >>> operation()
    '[{...}, {...}]'

When a named operation returns a non-builtin object that provides the
iterator protocol, we don't return the whole list. The object probably
provides access to a potentially huge dataset, like a list of database
results. In this case we do the same thing we do when serving a
collection resource. We fetch one batch of results and represent it as
a JSON hash containing a list of entries.

    >>> class StubResultSet:
    ...     results = [C1_D1, C2_D1]
    ...
    ...     def __iter__(self):
    ...         return iter(self.results)
    ...
    ...     def __len__(self):
    ...         return len(self.results)
    ...
    ...     def __getitem__(self, index):
    ...         return self.results[index]

    >>> recipes = StubResultSet()
    >>> request, operation = make_sample_operation_request(recipes)
    >>> response = operation()
    >>> pprint_collection(simplejson.loads(response))
    start: ...
    total_size: 2
    ---
    ...
    ---
    ...
    ---

When a named operation returns an object that has an ``ICollection``
implementation, the result is similar: we return a JSON hash describing one
batch from the collection.

    >>> request, operation = make_sample_operation_request(DishSet())
    >>> response = operation()
    >>> pprint_collection(simplejson.loads(response))
    resource_type_link: 'http://api.cookbooks.dev/beta/#dishes'
    start: ...
    total_size: 3
    ---
    ...
    ---
    ...
    ---
    ...
    ---

If the return value can't be converted into JSON, you'll get an
exception.

    >>> request, operation = make_sample_operation_request(object())
    >>> operation()
    Traceback (most recent call last):
    ...
    TypeError: Could not serialize object <object...> to JSON.

    >>> request, operation = make_sample_operation_request(
    ...     {'anobject' : object()})
    >>> operation()
    Traceback (most recent call last):
    ...
    TypeError: Could not serialize object {'anobject': <object...>} to JSON.

    >>> request, operation = make_sample_operation_request([object()])
    >>> operation()
    Traceback (most recent call last):
    ...
    TypeError: Could not serialize object [<object object...>] to JSON.

ETags
=====

Every entry resource has a short opaque string called an ETag that
summarizes the resource's current state. The ETag is sent as the
response header 'ETag'.

    >>> julia_object = A1
    >>> julia_url = quote('/beta/authors/Julia Child')
    >>> get_request = create_web_service_request(julia_url)
    >>> ignored = get_request.traverse(app)()
    >>> etag_original = get_request.response.getHeader('ETag')

The ETag is different across revisions of the software, but within a
release it'll always the same for a given resource with a given state.

    >>> get_request = create_web_service_request(julia_url)
    >>> ignored = get_request.traverse(app)()
    >>> etag_after_get = get_request.response.getHeader('ETag')

    >>> etag_after_get == etag_original
    True

A client can use a previously obtained ETag as the value of
If-None-Match when making a request. If the ETags match, it means the
resource hasn't changed since the client's last request. The server
sends a response code of 304 ("Not Modified") instead of sending the
same representation again.

First, let's define a helper method to request a specific entry
resource, and gather the entity-body and the response object into an
easily accessible data structure.

    >>> def get_julia(etag=None):
    ...     headers = {'CONTENT_TYPE' : 'application/json'}
    ...     if etag is not None:
    ...         headers['HTTP_IF_NONE_MATCH'] = etag
    ...     get_request = create_web_service_request(
    ...         julia_url, environ=headers)
    ...     entity_body = get_request.traverse(app)()
    ...     if isinstance(entity_body, bytes):
    ...         entity_body = entity_body.decode()
    ...     return dict(entity_body=entity_body,
    ...                 response=get_request.response)

    >>> print(get_julia(etag_original)['response'].getStatus())
    304

If the ETags don't match, the server assumes the client has an old
representation, and sends the new representation.

    >>> print(get_julia('bad etag')['entity_body'])
    {...}

Change the state of the resource, and the ETag changes.

    >>> julia_object.favorite_recipe = C2_D2
    >>> etag_after_modification = get_julia()['response'].getHeader('ETag')

    >>> etag_after_modification == etag_original
    False

The client can't modify read-only fields, but they might be modified
behind the scenes. If one of them changes, the ETag will change.

    >>> julia_object.popularity = 5
    >>> etag_after_readonly_change = get_julia()['response'].getHeader(
    ...     'ETag')
    >>> etag_after_readonly_change == etag_original
    False

compensate_for_mod_compress_etag_modification
---------------------------------------------

Apache's mod_compress transparently modifies outgoing ETags, but
doesn't remove the modifications when the ETags are sent back in. The
configuration setting 'compensate_for_mod_compress_etag_modification'
makes lazr.restful compensate for this behavior, so that you can use
mod_compress to save bandwidth.

Different versions of mod_compress modify outgoing ETags in different
ways. lazr.restful handles both cases.

   >>> etag = get_julia()['response'].getHeader('ETag')
   >>> modified_etag_1 = etag + '-gzip'
   >>> modified_etag_2 = etag[:-1] + '-gzip' + etag[-1]

Under normal circumstances, lazr.restful won't recognize an ETag
modified by mod_compress.

    >>> print(get_julia(modified_etag_1)['entity_body'])
    {...}

When 'compensate_for_mod_compress_etag_modification' is set,
lazr.restful will recognize an ETag modified by mod_compress.

    >>> c = webservice_configuration
    >>> print(c.compensate_for_mod_compress_etag_modification)
    False
    >>> c.compensate_for_mod_compress_etag_modification = True

    >>> print(get_julia(modified_etag_1)['response'].getStatus())
    304

    >>> print(get_julia(modified_etag_2)['response'].getStatus())
    304

Of course, that doesn't mean lazr.restful will recognize any random
ETag.

    >>> print(get_julia(etag + "-not-gzip")['entity_body'])
    {...}

Cleanup.

    >>> c.compensate_for_mod_compress_etag_modification = False

Resource Visibility
===================

Certain resources might not be visible to every user. In this example,
certain recipes have been designated as private and can't be seen by
unauthenticated users. For demonstration purposes, the recipe for
"Baked beans" in "James Beard's American Cookery" has been marked as
private. An unauthorized attempt to GET this resource will result in
an error.

    >>> private_recipe_url = quote(
    ...     "/beta/cookbooks/James Beard's American Cookery/recipes/"
    ...     "Baked beans")
    >>> get_request = create_web_service_request(private_recipe_url)
    >>> recipe_resource = get_request.traverse(app)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.security.interfaces.Unauthorized: (<Recipe object...>, 'dish', ...)

The recipe will not show up in collections:

    >>> recipes_url = quote(
    ...     "/beta/cookbooks/James Beard's American Cookery/recipes")
    >>> get_request = create_web_service_request(recipes_url)
    >>> collection_resource = get_request.traverse(app)
    >>> collection = load_json(collection_resource())

The web service knows about two recipes from James Beard's American
Cookery, but an unauthorized user can only see one of them.

    >>> len(collection['entries'])
    1

Note that the 'total_size' of the collection is slightly inaccurate,
having been generated before invisible recipes were filtered out.

    >>> collection['total_size']
    2

As it happens, the author "James Beard" has his 'favorite_recipe'
attribute set to the "Baked beans" recipe. But an unauthorized user
can't see anything about that recipe, not even its URL.

    >>> beard_url = quote('/beta/authors/James Beard')
    >>> get_request = create_web_service_request(beard_url)
    >>> author_resource = get_request.traverse(app)
    >>> author = load_json(author_resource())

The author's name is public information, so it's visible. But the link
to his favorite recipe has been redacted.

    >>> print(author['name'])
    James Beard
    >>> print(author['favorite_recipe_link'])
    tag:launchpad.net:2008:redacted

It's possible to use a representation that contains redacted
information when sending a PUT or PATCH request back to the
server. The server will know that the client isn't actually trying to
set the field value to 'tag:launchpad.net:2008:redacted'.

    >>> headers = {'CONTENT_TYPE' : 'application/json'}
    >>> body = simplejson.dumps(author).encode()
    >>> put_request = create_web_service_request(
    ...     beard_url, body=body, environ=headers, method='PUT')
    >>> print(put_request.traverse(app)().decode())
    {...}

And since no special permission is necessary to _change_ a person's
'favorite_recipe', it's possible to set it to a visible recipe using
PUT, even when its current value is redacted.

    >>> author['favorite_recipe_link'] = 'http://' + quote(
    ...     'api.cookbooks.dev/beta/cookbooks/'
    ...     'The Joy of Cooking/recipes/Roast chicken')
    >>> body = simplejson.dumps(author).encode()
    >>> put_request = create_web_service_request(
    ...     beard_url, body=body, environ=headers, method='PUT')
    >>> print(put_request.traverse(app)().decode())
    {...}

After that PUT, James Beard's 'favorite_recipe' attribute is no longer
redacted. It's the value set by the PUT request.

    >>> get_request = create_web_service_request(beard_url)
    >>> author_resource = get_request.traverse(app)
    >>> author = load_json(author_resource())
    >>> print(author['favorite_recipe_link'])
    http://api.cookbooks.dev/beta/cookbooks/The%20Joy%20of%20Cooking/recipes/Roast%20chicken

Finally, you can't set an attribute to a value that you wouldn't have
permission to see:

    >>> author['favorite_recipe_link'] = (
    ...     'http://api.cookbooks.dev' + private_recipe_url)
    >>> body = simplejson.dumps(author).encode()
    >>> put_request = create_web_service_request(
    ...     beard_url, body=body, environ=headers, method='PUT')
    >>> print(put_request.traverse(app)())
    (<Recipe object...>, 'dish', ...)

    >>> print(put_request.response.getStatus())
    401

Stored file resources
=====================

Binary files, such as the covers of cookbooks, are stored on an external
server, but they have addresses within the web service. The mapping of binary
resources to the actual hosting of them is handled through the
``IByteStorage`` interface. For this example, let's define simple
implementation that serves all files from the /files path.

    >>> from lazr.restful.interfaces import IByteStorage
    >>> from lazr.restful.example.base.interfaces import (
    ...     IFileManagerBackedByteStorage)
    >>> from lazr.restful.example.base.root import SimpleByteStorage
    >>> protect_schema(SimpleByteStorage, IFileManagerBackedByteStorage)
    >>> sm.registerAdapter(SimpleByteStorage, provided=IByteStorage)

A newly created cookbook has no cover.

    >>> cover_url = quote('/beta/cookbooks/The Joy of Cooking/cover')
    >>> get_request = create_web_service_request(cover_url)
    >>> file_resource = get_request.traverse(app)
    >>> file_resource()  # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: ... name: 'cover'

    >>> print(C2.cover)
    None

A cookbook can be given a cover with PUT.

    >>> headers = {'CONTENT_TYPE' : 'image/png'}
    >>> body = b'Pretend this is an image.'
    >>> put_request = create_web_service_request(
    ...     cover_url, body=body, environ=headers, method='PUT')
    >>> file_resource = put_request.traverse(app)
    >>> file_resource()

    >>> print(C2.cover.representation.decode())
    Pretend...

At this point it exists:

    >>> get_request = create_web_service_request(cover_url)
    >>> file_resource = get_request.traverse(app)
    >>> file_resource()
    >>> get_request.response.getStatus()
    303
    >>> print(get_request.response.getHeader('Location'))
    http://cookbooks.dev/.../filemanager/0

The cover can be deleted with DELETE.

    >>> delete_request = create_web_service_request(
    ...     cover_url, method='DELETE')
    >>> file_resource = delete_request.traverse(app)
    >>> file_resource()

    >>> get_request = create_web_service_request(cover_url)
    >>> file_resource = get_request.traverse(app)
    >>> file_resource()  # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: ... name: 'cover'

    >>> print(C2.cover)
    None

Field resources
===============

An entry's primitive data fields are exposed as subordinate resources.

    >>> field_resource = create_web_service_request(
    ...     '/beta/cookbooks/The%20Joy%20of%20Cooking/name').traverse(app)
    >>> print(field_resource().decode())
    "The Joy of Cooking"

Requesting non available resources
==================================

If the user tries to traverse to a nonexistent object, the result is a
NotFound exception.

Requesting a non-existent top-level collection:

    >>> create_web_service_request('/beta/nosuchcollection').traverse(app)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: ... name: ...'nosuchcollection'

Requesting a non-existent cookbook:

    >>> create_web_service_request('/beta/cookbooks/104').traverse(app)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: ... name: ...'104'

Requesting a non-existent comment:

    >>> create_web_service_request(
    ...  '/beta/cookbooks/The%20Joy%20of%20Cooking/comments/10').traverse(app)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: ... name: ...'comments/10'

Manipulating entries
====================

Most entry resources support write operations by responding to PATCH
requests. The entity-body of a PATCH request should be a JSON document
with new values for some of the entry's attributes. Basically, a set
of assertions about what the object *should* look like.

A PATCH request will automatically result in a modification event
being sent out about the modified object, which means that
modify_cookbook() will be run. Here, we modify the name and the
cuisine of one of the cookbooks. Note that the cuisine contains
non-ASCII characters.

    >>> headers = {'CONTENT_TYPE' : 'application/json'}
    >>> body = b'''{"name" : "The Joy of Cooking (revised)",
    ...             "cuisine" : "\xd7\x97\xd7\x95\xd7\x9e\xd7\x95\xd7\xa1"}'''

    >>> patch_request = create_web_service_request(
    ...     '/beta/cookbooks/The%20Joy%20of%20Cooking', body=body,
    ...     environ=headers, method='PATCH')
    >>> joy_resource_patch = patch_request.traverse(app)
    >>> joy_resource_patch()
    You just modified a cookbook.
    ''

    >>> patch_request.response.getHeader('Location')
    'http://api.../cookbooks/The%20Joy%20of%20Cooking%20%28revised%29'

The new name is reflected in the cookbook's representation, and the
cookbook's URL has changed as well.

    >>> request = create_web_service_request(
    ...     '/beta/cookbooks/The%20Joy%20of%20Cooking%20%28revised%29')
    >>> joy_resource = request.traverse(app)
    >>> joy = load_json(joy_resource())
    >>> print(joy['name'])
    The Joy of Cooking (revised)

An entry that responds to PATCH will also respond to PUT. With PUT you
modify the document you got in response to a GET request, and send the
whole thing back to the server, whereas with PATCH you're creating a
new document that describes a subset of the entry's state.

Here, we use PUT to change the cookbook's name back to what it was
before. Note that we send the entire dictionary back to the
server. Note also that another modification event is sent out and
intercepted by the modified_cookbook() listener.

    >>> joy['name'] = 'The Joy of Cooking'
    >>> body = simplejson.dumps(joy).encode()
    >>> put_request = create_web_service_request(
    ...     '/beta/cookbooks/The%20Joy%20of%20Cooking%20%28revised%29',
    ...     body=body, environ=headers, method='PUT')

    >>> joy_resource_put = put_request.traverse(app)
    >>> joy_resource_put()
    You just modified a cookbook.
    ''

Now that we've proved our point, let's disable the event handler so it
doesn't keep printing those messages.

    >>> cookbook_listener.unregister()

The cookbook's URL has changed back to what it was before.

    >>> put_request.response.getStatus()
    301
    >>> put_request.response.getHeader('Location')
    'http://api.cookbooks.dev/beta/cookbooks/The%20Joy%20of%20Cooking'

So has the cookbook's name.

    >>> joy_resource = create_web_service_request(
    ...     '/beta/cookbooks/The%20Joy%20of%20Cooking').traverse(app)
    >>> joy = load_json(joy_resource())
    >>> print(joy['name'])
    The Joy of Cooking

It's also possible to change the relationships between objects. Here,
we change a cookbook's author. Since all objects are identified by
their URLs, we make the change by modifying the cookbook's
'author_link' field to point to another author.

    >>> def change_joy_author(new_author_link, host='api.cookbooks.dev'):
    ...     representation = {'author_link' : new_author_link}
    ...     resource = create_web_service_request(
    ...         '/beta/cookbooks/The%20Joy%20of%20Cooking',
    ...         body=simplejson.dumps(representation).encode(),
    ...         environ=headers, method='PATCH', hostname=host).traverse(app)
    ...     result = resource()
    ...     if isinstance(result, bytes):
    ...         result = result.decode()
    ...     return result
    >>> path = '/beta/authors/Julia%20Child'

    >>> print(change_joy_author('http://api.cookbooks.dev' + path))
    {...}

    >>> joy_resource = create_web_service_request(
    ...     '/beta/cookbooks/The%20Joy%20of%20Cooking').traverse(app)
    >>> joy = load_json(joy_resource())
    >>> print(joy['author_link'])
    http://api.cookbooks.dev/beta/authors/Julia%20Child

When identifying an object by URL, make sure the hostname of your URL
matches the hostname you're requesting. If they don't match, your
request will fail.

    >>> print(change_joy_author('http://not.the.same.host' + path))
    author_link: No such object...

One possible source of hostname mismatches is the HTTP port. If the
web service is served from a strange port, you'll need to specify that
port in the URLs you send.

    >>> print(change_joy_author('http://api.cookbooks.dev' + path,
    ...                         host='api.cookbooks.dev:9000'))
    author_link: No such object...

    >>> print(change_joy_author('http://api.cookbooks.dev:9000' + path,
    ...                         host='api.cookbooks.dev:9000'))
    {...}

You don't have to specify the default port in the URLs you send, even
if you specified it when you made the request.

    >>> print(change_joy_author('http://api.cookbooks.dev' + path,
    ...                         host='api.cookbooks.dev:80'))
    {...}

    >>> print(change_joy_author('http://api.cookbooks.dev:80' + path,
    ...                         host='api.cookbooks.dev'))
    {...}

    >>> print(change_joy_author('https://api.cookbooks.dev' + path,
    ...                         host='api.cookbooks.dev:443'))
    author_link: No such object...

    >>> webservice_configuration.use_https = True
    >>> print(change_joy_author('https://api.cookbooks.dev' + path,
    ...                         host='api.cookbooks.dev:443'))
    {...}
    >>> webservice_configuration.use_https = False

If an entry has an IResourceDELETEOperation registered for it, you can
activate that operation and delete the entry by sending a DELETE
request.

    >>> recipe_url = quote('/beta/cookbooks/Mastering the Art of '
    ...     'French Cooking/recipes/Foies de voilaille en aspic')

Now you see it...

    >>> resource = create_web_service_request(
    ...     recipe_url, method='GET').traverse(app)
    >>> print(resource().decode())
    {...}

    >>> resource = create_web_service_request(
    ...     recipe_url, method='DELETE').traverse(app)
    >>> ignored = resource()

Now you don't.

    >>> resource = create_web_service_request(
    ...     recipe_url, method='GET').traverse(app)
    ... # doctest: +IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    Traceback (most recent call last):
    ...
    zope.publisher.interfaces.NotFound: ... name: ...'recipes/Foies de voilaille en aspic'


Within a template
=================

A number of TALES adapters give different views on resource
objects. The is_entry() function is a conditional that returns true when
given an object that can be adapted to IEntry.

    >>> from lazr.restful.testing.tales import test_tales
    >>> test_tales("context/webservice:is_entry", context=A1)
    True
    >>> test_tales("context/webservice:is_entry", context=AUTHORS)
    False

The json() function converts generic Python data structures to JSON,
as well as objects that can be adapted to IEntry. It converts markup
characters (<, >, &) into their respective Unicode escape sequences,
since entities within <script> tags are not expanded.

    >>> test_tales("context/webservice:json", context="foobar")
    '"foobar"'
    >>> test_tales("context/webservice:json", context=A1)
    '{..."name": ...}'
    >>> test_tales("context/webservice:json", context="<foo&>")
    '"\\u003cfoo\\u0026\\u003e"'
