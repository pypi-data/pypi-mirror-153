# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Various utility functions."""

__all__ = [
    "camelcase_to_underscore_separated",
    "get_current_browser_request",
    "get_current_web_service_request",
    "implement_from_dict",
    "make_identifier_safe",
    "parse_accept_style_header",
    "safe_hasattr",
    "smartquote",
    "simple_popen2",
    "tag_request_with_version_name",
    "VersionedDict",
    "VersionedObject",
]

import builtins
import collections
import copy
import operator
import re
import string
import subprocess
import warnings

from zope.component import getUtility
from zope.schema import getFieldsInOrder
from zope.interface import alsoProvides, classImplements

from lazr.restful.interfaces import (
    IWebServiceClientRequest,
    IWebServiceVersion,
)


missing = object()


def extract_write_portion(etag):
    """Retrieve the portion of an etag that predicates writes."""
    return etag.split("-", 1)[-1]


def is_total_size_link_active(version, config):
    versions = config.active_versions
    total_size_link_version = config.first_version_with_total_size_link
    # The version "None" is a special marker for the earliest version.
    if total_size_link_version is None:
        total_size_link_version = versions[0]
    # If the version we're being asked about is equal to or later than the
    # version in which we started exposing total_size_link, then we should
    # return True, False otherwise.
    return versions.index(total_size_link_version) <= versions.index(version)


def parse_accept_style_header(value):
    """Parse an HTTP header from the Accept-* family.

    These headers contain a list of possible values, each with an
    optional priority.

    This code is modified from Zope's
    BrowserLanguages#getPreferredLanguages.

    If a value includes parameters other than 'q', they will be preserved.

    :return: All values, in descending order of priority.
    """
    if value is None:
        return []

    values = value.split(",")
    values = [v.strip() for v in values if v != ""]

    accepts = []
    for index, value in enumerate(values):
        value_and_parameters = value.split(";")

        # If not supplied, quality defaults to 1.
        quality = 1.0

        if len(value_and_parameters) > 1:
            # There's at least one parameter, possibly including
            # a quality parameter.
            quality_parameter = None
            bare_value = value_and_parameters[0]
            parameters = value_and_parameters[1:]
            for parameter_index, parameter in enumerate(parameters):
                if parameter.startswith("q="):
                    # We found the quality parameter
                    quality_parameter = parameter
                    q = quality_parameter.split("=", 2)[1]
                    quality = float(q)

            if quality_parameter is not None:
                # Remove the quality parameter from the list of
                # parameters, and re-create the header value without
                # it.
                parameters.remove(quality_parameter)
                if len(parameters) > 0:
                    value = ";".join([bare_value] + parameters)
                else:
                    value = bare_value

        if quality == 1.0:
            # ... but we use 1.9 - 0.001 * position to
            # keep the ordering between all items with
            # 1.0 quality, which may include items with no quality
            # defined, and items with quality defined as 1.
            quality = 1.9 - (0.001 * index)

        accepts.append((quality, value))

    accepts.sort()
    accepts.reverse()
    seen_already = set()
    filtered_accepts = []
    for priority, value in accepts:
        if priority > 0 and value not in seen_already:
            filtered_accepts.append((priority, value))
            seen_already.add(value)
    return [value for quality, value in filtered_accepts]


VersionedObject = collections.namedtuple(
    "VersionedObject", ["version", "object"]
)


class VersionedDict:
    """A stack of named dictionaries.

    Most access to the stack actually operates on the dictionary on
    top of the stack. Dictionary access doesn't work when the stack is
    empty.

    When you push a named dictionary onto the stack, it is populated
    by a deep copy of the next highest dictionary in the stack. You
    can push an empty dictionary onto the stack by passing empty=True
    in to the push() method.
    """

    missing = object()

    def __init__(self, name=None):
        """Initialize the bleed-through dictionary."""
        self.stack = []
        if name is not None:
            self.push(name)

    def push(self, name, empty=False):
        """Pushes a dictionary onto the stack.

        :arg name: The name of the dictionary to push.
        :arg empty: If True, the dictionary will be created empty
                    rather than being populated with a deep copy of
                    the dictionary below it.
        """
        if empty or len(self.stack) == 0:
            dictionary = {}
        else:
            stack_top = self.stack[-1].object
            dictionary = copy.deepcopy(stack_top)
        self.stack.append(VersionedObject(name, dict(dictionary)))

    def pop(self):
        """Pop a tuple representing a dictionary from the stack.

        :return: A 2-tuple (name, dict). 'name' is the name of the
        dictionary within the VersionedDict; 'dict' is the contents
        of the dictionary.
        """
        return self.stack.pop()

    def dict_for_name(self, version, default=None):
        """Find the first dict for the given version."""
        matches = [
            item.object for item in self.stack if item.version == version
        ]
        if len(matches) == 0:
            return default
        return matches[0]

    def normalize_for_versions(
        self, versions, default_dictionary=None, error_prefix=""
    ):
        """Fill out the stack with something for every given version.

        :param versions: A list of names for dictionaries. By the time
          this method completes, the value of `dict_names` will be the
          same as this list. 'Earlier' versions are presumed to come
          before 'later' versions, but this only affects the error
          message given when annotations are discovered to be out of
          order.

        :param default_dictionary: A dictionary to use for versions that
          can't inherit values from some other dictionary.

        :param error_prefix: A string to prepend to errors when
          raising exceptions.

        :raise ValueError: If the existing dictionary stack includes
           names not present in `versions`, if the names in the stack
           are present in an order other than the one given in
           `versions`, or if any names in the stack are duplicated.
        """
        new_stack = []

        # Do some error checking.
        max_index = -1
        for version, tags in self.stack:
            try:
                version_index = versions.index(version)
            except ValueError:
                raise ValueError(
                    error_prefix + 'Unrecognized version "%s".' % version
                )
            if version_index == max_index:
                raise ValueError(
                    error_prefix + "Duplicate definitions for version "
                    '"%s".' % version
                )
            if version_index < max_index:
                raise ValueError(
                    error_prefix + 'Version "%s" defined after '
                    'the later version "%s".' % (version, versions[max_index])
                )
            max_index = version_index

        # We now know that the versions present in the dictionary are
        # an ordered subset of the versions in `versions`. All we have
        # to do now is fill in the blanks.
        most_recent_dict = default_dictionary or {}
        for version in versions:
            existing_dict = self.dict_for_name(version)
            if existing_dict is None:
                # This version has no dictionary of its own. Use a copy of
                # the most recent dictionary.
                new_stack.append(
                    VersionedObject(version, copy.deepcopy(most_recent_dict))
                )
            else:
                # This version has a dictionary. Use it.
                new_stack.append(VersionedObject(version, existing_dict))
                most_recent_dict = existing_dict
        self.stack = new_stack

    @property
    def dict_names(self):
        """Return the names of dictionaries in the stack."""
        return [item.version for item in self.stack if item is not None]

    @property
    def is_empty(self):
        """Is the stack empty?"""
        return len(self.stack) == 0

    def rename_version(self, old_name, new_name):
        """Change the name of a version."""
        for index, pair in enumerate(self.stack):
            if pair.version == old_name:
                self.stack[index] = VersionedObject(new_name, pair.object)
                break
        else:
            raise KeyError(old_name)

    def setdefault(self, key, value):
        """Get a from the top of the stack, setting it if not present."""
        return self.stack[-1].object.setdefault(key, value)

    def __contains__(self, key):
        """Check whether a key is visible in the stack."""
        return self.get(key, missing) is not missing

    def __getitem__(self, key):
        """Look up an item somewhere in the stack."""
        if self.is_empty:
            raise KeyError(key)
        return self.stack[-1].object[key]

    def get(self, key, default=None):
        """Look up an item somewhere in the stack, with default fallback."""
        if self.is_empty:
            return default
        return self.stack[-1].object.get(key, default)

    def items(self):
        """Return a merged view of the items in the dictionary."""
        if self.is_empty:
            raise IndexError("Stack is empty")
        return self.stack[-1].object.items()

    def __setitem__(self, key, value):
        """Set a value in the dict at the top of the stack."""
        if self.is_empty:
            raise IndexError("Stack is empty")
        self.stack[-1].object[key] = value

    def __delitem__(self, key):
        """Delete a value from the dict at the top of the stack."""
        if self.is_empty:
            raise IndexError("Stack is empty")
        del self.stack[-1].object[key]


def implement_from_dict(class_name, interface, values, superclass=object):
    """Return a class that implements an interface's attributes.

    :param interface: The interface to implement.
    :param superclass: The superclass of the class to be generated.
    :param values: A dict of values to use when generating the class.
    :return: A class that implements 'interface'. Any attributes given
             values in 'values' will have those values in the generated
             interface. Other attributes will have their default
             values as defined in the interface. Attributes with no
             default values, will not be present.
    """
    class_dict = {}
    for name, field in getFieldsInOrder(interface):
        if field.default is not None:
            class_dict[name] = field.default
    class_dict.update(values)

    if not isinstance(superclass, tuple):
        superclass = (superclass,)
    new_class = type(class_name, superclass, class_dict)
    classImplements(new_class, interface)
    return new_class


def make_identifier_safe(name):
    """Change a string so it can be used as a Python identifier.

    Changes all characters other than letters, numbers, and underscore
    into underscore. If the first character is not a letter or
    underscore, prepends an underscore.
    """
    if name is None:
        raise ValueError("Cannot make None value identifier-safe.")
    name = re.sub("[^A-Za-z0-9_]", "_", name)
    if len(name) == 0 or (
        name[0] not in string.ascii_letters and name[0] != "_"
    ):
        name = "_" + name
    return name


def camelcase_to_underscore_separated(name):
    """Convert 'ACamelCaseString' to 'a_camel_case_string'"""

    def prepend_underscore(match):
        return "_" + match.group(1)

    return re.sub(r"\B([A-Z])", prepend_underscore, name).lower()


def safe_hasattr(ob, name):
    """hasattr() that doesn't hide exceptions.

    This is no longer useful in Python >= 3.2.
    """
    warnings.warn(
        "safe_hasattr is deprecated; use the hasattr builtin instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return hasattr(ob, name)


def smartquote(str):
    """Return a copy of the string, with typographical quote marks applied."""
    # Using builtins.str here is weird, but it lets us cope with the
    # unfortunate naming of our positional argument without breaking API.
    str = builtins.str(str)
    str = re.compile('(^| )(")([^" ])').sub("\\1\u201c\\3", str)
    str = re.compile('([^ "])(")($|[\\s.,;:!?])').sub("\\1\u201d\\3", str)
    return str


def get_current_browser_request():
    """Return the current browser request, looked up from the interaction.

    If there is no suitable request, then return None.

    Returns only requests that provide IHTTPApplicationRequest.
    """
    from zope.security.management import queryInteraction
    from zope.publisher.interfaces.http import IHTTPApplicationRequest

    interaction = queryInteraction()
    if interaction is None:
        return None
    requests = [
        participation
        for participation in interaction.participations
        if IHTTPApplicationRequest.providedBy(participation)
    ]
    if not requests:
        return None
    assert len(requests) == 1, (
        "We expect only one IHTTPApplicationRequest in the interaction."
        " Got %s." % len(requests)
    )
    return requests[0]


def get_current_web_service_request():
    """Return the current web service request.

    This may be a new request object based on the browser request (if
    the client is a web browser that might make AJAX calls to a
    separate web service) or it may be the same as the browser request
    (if the client is a web service client accessing the service
    directly).

    :return: An object providing IWebserviceClientRequest.
    """
    request = get_current_browser_request()
    if request is None:
        return None
    return IWebServiceClientRequest(request)


def tag_request_with_version_name(request, version):
    """Tag a request with a version name and marker interface."""
    request.annotations[request.VERSION_ANNOTATION] = version
    # Find the version-specific marker interface this request should
    # provide, and provide it.
    to_provide = getUtility(IWebServiceVersion, name=version)
    alsoProvides(request, to_provide)
    request.version = version


def simple_popen2(command, input, env=None, in_bufsize=1024, out_bufsize=128):
    """Run a command, give it input on its standard input, and capture its
    standard output.

    Returns the data from standard output.

    This function is needed to avoid certain deadlock situations. For example,
    if you popen2() a command, write its standard input, then read its
    standard output, this can deadlock due to the parent process blocking on
    writing to the child, while the child process is simultaneously blocking
    on writing to its parent. This function avoids that problem by using
    subprocess.Popen.communicate().
    """

    p = subprocess.Popen(
        command,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    (output, nothing) = p.communicate(input)
    return output


def sorted_named_things(things):
    """Return a list of things (functions and/or classes) sorted by name."""
    name = operator.attrgetter("__name__")
    return sorted(things, key=name)
