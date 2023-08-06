..
    This file is part of lazr.restful.

    lazr.restful is free software: you can redistribute it and/or modify it
    under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, version 3 of the License.

    lazr.restful is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with lazr.restful.  If not, see <http://www.gnu.org/licenses/>.

************
lazr.restful
************

lazr.restful is a library for publishing Python objects through a
RESTful web service. To tell lazr.restful which objects you want
exposed and how, you annotate your existing Zope interfaces.


The WSGI example web service
============================

The example web service in src/lazr/restful/example/wsgi/ is the best
place to start understanding lazr.restful. It's a very simple web
service that uses a subset of lazr.restful's features and can be run
as a standalone WSGI application. An explanation of the code can be
found in src/lazr/restful/example/wsgi/README.txt

The full example web service
============================

To understand all of lazr.restful, you should look at the web service
defined in src/lazr/restful/example/base/. It defines a simple
application serving information about cookbooks and recipes. The
interfaces (interfaces.py) are annotated with lazr.restful decorators
that say which fields and methods to publish from IRecipe, ICookbook,
and so on. The implementations of those interfaces are in root.py.

The machinery of lazr.restful takes the decorators in interfaces.py,
and generates an interface that maps incoming HTTP requests to
operations on the actual objects defined in root.py. You don't have to
do any HTTP server programming to get it to work (though at the moment
you do have to know a fair amount about Zope).

You can test the example web service by running `bin/test`. The
doctests in src/lazr/restful/example/base/tests use a fake httplib2
connection to simulate HTTP requests to the web service. You can watch
the tests make GET, PUT, POST, PATCH, and DELETE requests to the web
service. Start with root.txt.

Other code
==========

Two other pieces of code might be of interest when you're starting
out.

* declarations.py contains all the Python
  decorators. docs/webservice-declarations.txt shows how to use them.

* docs/webservice.txt shows an example of a webservice that creates
  Entry and Collection classes directly rather than generating them
  with the declarations. If you want to use lazr.restful without using
  zope.schema, this is the test to look at.

..
    end-pypi

===============
Other Documents
===============

.. toctree::
   :glob:

   webservice
   webservice-declarations
   webservice-error
   webservice-marshallers
   webservice-request
   fields
   interface
   absoluteurl
   utils
   checker-utilities
   multiversion
   debug
   django
   CONTRIBUTING
   NEWS
