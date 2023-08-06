This is a very simple webservice that demonstrates how to use contributing
interfaces to add fields to an existing webservice using a plugin-like
pattern.

Here we've just added a 'comments' field to the IRecipe entry.

    >>> from lazr.restful.testing.webservice import WebServiceCaller
    >>> webservice = WebServiceCaller(domain='cookbooks.dev')

    # The comments DB for this webservice is empty so we'll add some comments
    # to the recipe with ID=1
    >>> from lazr.restful.example.base_extended.comments import comments_db
    >>> comments_db[1] = ['Comment 1', 'Comment 2']

And as we can see below, a recipe's representation now include its comments.

    >>> print("\n".join(webservice.get('/recipes/1').jsonBody()['comments']))
    Comment 1
    Comment 2

    >>> webservice.get('/recipes/2').jsonBody()['comments']
    []
