from zope.component import adapter
from zope.interface import implementer, Interface
from zope.schema import List, Text

from lazr.restful.example.base.interfaces import IRecipe

from lazr.restful.declarations import (
    exported,
    exported_as_webservice_entry,
)


@exported_as_webservice_entry(contributes_to=[IRecipe])
class IHasComments(Interface):
    comments = exported(
        List(title="Comments made by users", value_type=Text())
    )


@implementer(IHasComments)
@adapter(IRecipe)
class RecipeToHasCommentsAdapter:
    def __init__(self, recipe):
        self.recipe = recipe

    @property
    def comments(self):
        return comments_db.get(self.recipe.id, [])


# A fake database for storing comments. Monkey-patch this to test the
# IHasComments adapter.
comments_db = {}
