# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Declaration helpers to define a web service."""

__all__ = [
    "COLLECTION_TYPE",
    "ENTRY_TYPE",
    "FIELD_TYPE",
    "LAZR_WEBSERVICE_ACCESSORS",
    "LAZR_WEBSERVICE_EXPORTED",
    "LAZR_WEBSERVICE_MUTATORS",
    "OPERATION_TYPES",
    "REQUEST_USER",
    "accessor_for",
    "cache_for",
    "call_with",
    "collection_default_content",
    "error_status",
    "export_destructor_operation",
    "export_factory_operation",
    "export_operation_as",
    "export_read_operation",
    "export_write_operation",
    "exported",
    "exported_as_webservice_collection",
    "exported_as_webservice_entry",
    "generate_collection_adapter",
    "generate_entry_adapters",
    "generate_entry_interfaces",
    "generate_operation_adapter",
    "mutator_for",
    "operation_for_version",
    "operation_parameters",
    "operation_removed_in_version",
    "operation_returns_entry",
    "operation_returns_collection_of",
    "rename_parameters_as",
    "scoped",
    "webservice_error",
]

from collections import OrderedDict
import copy
import itertools
import sys

from zope.component import getUtility, getGlobalSiteManager
from zope.interface import classImplements
from zope.interface.interface import fromFunction, InterfaceClass, TAGGED_DATA
from zope.interface.interfaces import IInterface, IMethod
from zope.schema import (
    getFields,
    getFieldsInOrder,
)
from zope.schema.interfaces import (
    IField,
    IObject,
)
from zope.security.checker import CheckerPublic
from zope.traversing.browser import absoluteURL

from lazr.delegates import Passthrough

from lazr.restful.fields import (
    CollectionField,
    Reference,
)
from lazr.restful.interface import copy_field
from lazr.restful.interfaces import (
    ICollection,
    IEntry,
    IReference,
    IResourceDELETEOperation,
    IResourceGETOperation,
    IResourcePOSTOperation,
    IWebServiceConfiguration,
    IWebServiceVersion,
    LAZR_WEBSERVICE_NAME,
    LAZR_WEBSERVICE_NS,
)
from lazr.restful import (
    Collection,
    Entry,
    EntryAdapterUtility,
    ResourceOperation,
    ObjectLink,
)
from lazr.restful.security import protect_schema
from lazr.restful.utils import (
    camelcase_to_underscore_separated,
    get_current_web_service_request,
    make_identifier_safe,
    VersionedDict,
    VersionedObject,
)

LAZR_WEBSERVICE_ACCESSORS = "%s.exported.accessors" % LAZR_WEBSERVICE_NS
LAZR_WEBSERVICE_EXPORTED = "%s.exported" % LAZR_WEBSERVICE_NS
LAZR_WEBSERVICE_MUTATORS = "%s.exported.mutators" % LAZR_WEBSERVICE_NS
COLLECTION_TYPE = "collection"
ENTRY_TYPE = "entry"
FIELD_TYPE = "field"
REMOVED_OPERATION_TYPE = "removed_operation"
OPERATION_TYPES = (
    "destructor",
    "factory",
    "read_operation",
    "write_operation",
    REMOVED_OPERATION_TYPE,
)

# These are the only valid keys to be found in an entry's
# version-specific annotation dictionary.
ENTRY_ANNOTATION_KEYS = {
    "contributes_to",
    "exported",
    "plural_name",
    "publish_web_link",
    "singular_name",
}


class REQUEST_USER:
    """Marker class standing in for the user of the current request.

    This is passed in to annotations like @call_with. This is a class
    rather than an object because it's going to be run through
    copy.deepcopy, and we want 'is REQUEST_USER' to succeed on the
    copy.
    """

    pass


def _check_called_from_interface_def(name):
    """
    Make sure that the declaration was used from within a class definition.
    """
    # 2 is our caller's caller.
    frame = sys._getframe(2)
    f_locals = frame.f_locals

    # Try to make sure we were called from a class def.
    if (f_locals is frame.f_globals) or ("__module__" not in f_locals):
        raise TypeError(
            "%s can only be used from within an interface definition." % name
        )


def _check_interface(name, interface):
    """Check that interface provides IInterface or raise a TypeError."""
    if not IInterface.providedBy(interface):
        raise TypeError("%s can only be used on an interface." % name)


def _get_interface_tags():
    """Retrieve the dictionary containing tagged values for the interface.

    This will create it, if it hasn't been defined yet.
    """
    # Our caller is contained within the interface definition.
    f_locals = sys._getframe(2).f_locals
    return f_locals.setdefault(TAGGED_DATA, {})


def _export_as_webservice_entry(
    interface,
    singular_name=None,
    plural_name=None,
    contributes_to=None,
    publish_web_link=True,
    as_of=None,
    versioned_annotations=None,
):
    """Tag an interface as exported on the web service as an entry.

    This is the core of exported_as_webservice_entry.
    """
    annotation_stack = VersionedDict()

    if singular_name is None:
        # By convention, interfaces are called IWord1[Word2...]. The default
        # behavior assumes this convention and yields a singular name of
        # "word1_word2".
        my_singular_name = camelcase_to_underscore_separated(
            interface.__name__[1:]
        )
    else:
        my_singular_name = singular_name

    # Turn the named arguments into a dictionary for the first exported
    # version.
    initial_version = dict(
        type=ENTRY_TYPE,
        singular_name=my_singular_name,
        plural_name=plural_name,
        contributes_to=contributes_to,
        publish_web_link=publish_web_link,
        exported=True,
        _as_of_was_used=(as_of is not None),
    )

    afterwards = versioned_annotations or []
    for version, annotations in itertools.chain(
        [(as_of, initial_version)], afterwards
    ):
        annotation_stack.push(version)

        for key, value in annotations.items():
            if annotations != initial_version:
                # Make sure that the 'annotations' dict contains only
                # recognized annotations.
                if key not in ENTRY_ANNOTATION_KEYS:
                    raise ValueError(
                        'Unrecognized annotation for version "%s": '
                        '"%s"' % (version, key)
                    )
            annotation_stack[key] = value
        # If this version provides a singular name but not a plural name,
        # apply the default pluralization rule.
        if (
            annotations.get("singular_name") is not None
            and annotations.get("plural_name") is None
        ):
            annotation_stack["plural_name"] = (
                annotations["singular_name"] + "s"
            )

    # When called from the @exported_as_webservice_entry decorator, this
    # would overwrite any interface annotations made by method decorators;
    # but there are currently no such annotations that are valid for methods
    # of entry interfaces anyway.
    interface.setTaggedValue(LAZR_WEBSERVICE_EXPORTED, annotation_stack)

    # Set the name of the fields that didn't specify it using the
    # 'export_as' parameter in exported(). This must be done here, because
    # the field's __name__ attribute is only set when the interface is
    # created.
    for name, field in getFields(interface).items():
        tag_stack = field.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag_stack is None or tag_stack.is_empty:
            continue
        if tag_stack["type"] != FIELD_TYPE:
            continue
        for version, tags in tag_stack.stack:
            # Set 'as' for every version in which the field is published but
            # no 'as' is specified. Also set 'original_name' for every
            # version in which the field is published--this will help with
            # performance optimizations around permission checks.
            if tags.get("exported") is not False:
                tags["original_name"] = name
                if tags.get("as") is None:
                    tags["as"] = name

    annotate_exported_methods(interface)


class exported_as_webservice_entry:
    """Mark the content interface as exported on the web service as an entry.

    If contributes_to is a non-empty sequence of Interfaces, this entry will
    actually not be exported on its own but instead will contribute its
    attributes/methods to other exported entries.

    :param singular_name: The human-readable singular name of the entry,
        eg. "paintbrush".
    :param plural_name: The human-readable plural name of the entry,
        eg. "paintbrushes"
    :param contributes_to: An optional list of exported interfaces to which
        this interface contributes.
    :param publish_web_link: This parameter is ignored unless there is
        a correspondence between this web service's entries and the
        pages on some website. If that is so, and if this parameter is
        set to True, the representation of this entry will include a
        web_link pointing to the corresponding page on the website. If
        False, web_link will be omitted.
    :param as_of: The first version of the web service to feature this entry.
    :param versioned_annotations: A list of 2-tuples (version,
        {params}), with more recent web service versions earlier in
        the list and older versions later in the list.

        A 'params' dictionary may contain the key 'exported', which
        controls whether or not to publish the entry at all in the
        given version. It may also contain the keys 'singular_name',
        'plural_name', 'contributes_to', or 'publish_web_link', which
        work just like the corresponding arguments to this method.
    """

    def __init__(
        self,
        singular_name=None,
        plural_name=None,
        contributes_to=None,
        publish_web_link=True,
        as_of=None,
        versioned_annotations=None,
    ):
        self.singular_name = singular_name
        self.plural_name = plural_name
        self.contributes_to = contributes_to
        self.publish_web_link = publish_web_link
        self.as_of = as_of
        self.versioned_annotations = versioned_annotations

    def __call__(self, interface):
        _check_interface("exported_as_webservice_entry()", interface)
        _export_as_webservice_entry(
            interface,
            singular_name=self.singular_name,
            plural_name=self.plural_name,
            contributes_to=self.contributes_to,
            publish_web_link=self.publish_web_link,
            as_of=self.as_of,
            versioned_annotations=self.versioned_annotations,
        )
        return interface


def exported(field, *versioned_annotations, **kwparams):
    """Mark the field as part of the entry data model.

    :param versioned_annotations: A list of (version, param) 2-tuples,
        with more recent web service versions earlier in the list and older
        versions later in the list. The 'param' objects can either be a
        string name for the field in the given version (None means to
        use the field's internal name), or a dictionary.

        The dictionary may contain the key 'exported', which controls
        whether or not to publish this field at all in the given
        version, and the key 'exported_as', which controls the name to
        use when publishing the field. exported_as=None means to use
        the field's internal name.

    :param as_of: The name of the earliest version to contain this field.

    :param exported_as: the name under which the field is published in
        the entry the first time it shows up (ie. in the 'as_of'
        version). By default, the field's internal name is used.

    :raises TypeError: if called on an object which doesn't provide IField.
    :returns: The field with an added tagged value.
    """
    if not IField.providedBy(field):
        raise TypeError("exported() can only be used on IFields.")

    if IObject.providedBy(field) and not IReference.providedBy(field):
        raise TypeError("Object exported; use Reference instead.")

    # The first step is to turn the arguments into a VersionedDict
    # describing the different ways this field is exposed in different
    # versions.
    annotation_stack = VersionedDict()
    first_version_name = kwparams.pop("as_of", None)
    annotation_stack.push(first_version_name)
    annotation_stack["type"] = FIELD_TYPE

    if first_version_name is not None:
        # The user explicitly said to start publishing this field in a
        # particular version.
        annotation_stack["_as_of_was_used"] = True
        annotation_stack["exported"] = True

    annotation_key_for_argument_key = {
        "exported_as": "as",
        "exported": "exported",
        "readonly": "readonly",
    }

    # If keyword parameters are present, they define the field's
    # behavior for the first exposed version. Incorporate them into
    # the VersionedDict.
    for (key, annotation_key) in annotation_key_for_argument_key.items():
        if key in kwparams:
            if (
                key == "exported"
                and kwparams[key] is False
                and first_version_name is not None
            ):
                raise ValueError(
                    (
                        "as_of=%s says to export %s, but exported=False "
                        "says not to."
                    )
                    % (first_version_name, field.__class__.__name__)
                )
            annotation_stack[annotation_key] = kwparams.pop(key)

    # If any keywords are left over, raise an exception.
    if len(kwparams) > 0:
        raise TypeError(
            "exported got an unexpected keyword "
            "argument '%s'" % list(kwparams)[0]
        )

    # Now incorporate the list of named dicts into the VersionedDict.
    for version, annotations in reversed(versioned_annotations):
        # Push it onto the stack.
        annotation_stack.push(version)
        # Make sure that the 'annotations' dict contains only
        # recognized annotations.
        for key in annotations:
            if key not in annotation_key_for_argument_key:
                raise ValueError(
                    'Unrecognized annotation for version "%s": '
                    '"%s"' % (version, key)
                )
            annotation_stack[
                annotation_key_for_argument_key[key]
            ] = annotations[key]

    # Now we can annotate the field object with the VersionedDict.
    field.setTaggedValue(LAZR_WEBSERVICE_EXPORTED, annotation_stack)

    # We track the field's mutator and accessor information separately
    # because it's defined in the named operations, not in the fields.
    # The last thing we want to do is try to insert a foreign value into
    # an already created annotation stack.
    field.setTaggedValue(LAZR_WEBSERVICE_MUTATORS, {})
    field.setTaggedValue(LAZR_WEBSERVICE_ACCESSORS, {})

    return field


def _check_collection_default_content(name, interface):
    """Check that the interface has a method providing the default content."""
    tag = interface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED, {})
    if "collection_default_content" not in tag:
        raise TypeError(
            "%s is missing a method tagged with @collection_default_content."
            % name
        )


class exported_as_webservice_collection:
    """Mark the interface as exported on the web service as a collection.

    :raises TypeError: if the interface doesn't have a method decorated with
        @collection_default_content.
    """

    def __init__(self, entry_schema):
        if not IInterface.providedBy(entry_schema):
            raise TypeError("entry_schema must be an interface.")
        self.entry_schema = entry_schema

    def __call__(self, interface):
        _check_interface("exported_as_webservice_collection()", interface)
        _check_collection_default_content(
            "exported_as_webservice_collection()", interface
        )
        tag = interface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag is None:
            tag = {}
            interface.setTaggedValue(LAZR_WEBSERVICE_EXPORTED, tag)
        tag["type"] = COLLECTION_TYPE
        tag["collection_entry_schema"] = self.entry_schema
        annotate_exported_methods(interface)
        return interface


class collection_default_content:
    """Decorates the method that provides the default values of a collection.

    :raises TypeError: if called from within an interface exported as
        something other than a collection, or if used more than once for the
        same version in the same interface.
    """

    def __init__(self, version=None, **params):
        """Create the decorator marking the default collection method.

        :param version: The first web service version that should use this
            method as the collection's default content.
        :param params: Optional parameter values to use when calling the
            method. This is to be used when the method has required
            parameters.
        """
        _check_called_from_interface_def("@collection_default_content")

        # We used to check that this decorator is being used from within an
        # interface exported as a collection.  However, it isn't possible to
        # do this when using the @exported_as_webservice_collection
        # decorator rather than the old export_as_webservice_collection
        # function (which was based on class advice, and so cannot work in
        # Python 3): that decorator isn't called until the rest of the
        # interface has been defined, so it hasn't had a chance to set any
        # tags on the interface by the time decorators of methods in that
        # interface are called.  The best we can do is to check that we
        # don't already positively know that the interface is exported as an
        # entry instead.
        tags = _get_interface_tags()
        tag = tags.setdefault(LAZR_WEBSERVICE_EXPORTED, {})
        if "type" in tag and tag["type"] != COLLECTION_TYPE:
            raise TypeError(
                "@collection_default_content can only be used from within an "
                "interface exported as a collection."
            )

        default_content_methods = tag.setdefault(
            "collection_default_content", {}
        )

        if version in default_content_methods:
            raise TypeError(
                "Only one method can be marked with "
                "@collection_default_content for version '%s'."
                % (_version_name(version))
            )
        self.version = version
        self.params = params

    def __call__(self, f):
        """Annotates the collection with the name of the method to call."""
        tag = _get_interface_tags()[LAZR_WEBSERVICE_EXPORTED]
        tag["collection_default_content"][self.version] = (
            f.__name__,
            self.params,
        )
        return f


WEBSERVICE_ERROR = "__lazr_webservice_error__"


def webservice_error(status):
    """Mark the exception with the HTTP status code to use.

    That status code will be used by the view used to handle that kind of
    exceptions on the web service.

    This is only effective when the exception is raised from within a
    published method.  For example, if the exception is raised by the field's
    validation its specified status won't propagate to the response.
    """
    frame = sys._getframe(1)
    f_locals = frame.f_locals

    # Try to make sure we were called from a class def.
    if (f_locals is frame.f_globals) or ("__module__" not in f_locals):
        raise TypeError(
            "webservice_error() can only be used from within an exception "
            "definition."
        )

    f_locals[WEBSERVICE_ERROR] = int(status)


def error_status(status):
    """Make a class decorator for the given status.

    Usage 1:
        @error_status(400)
        class FooBreakage(Exception):
            pass

    Usage 2 (legacy):
        class FooBreakage(Exception):
            pass
        error_status(400)(FooBreakage)

    That status code will be used by the view used to handle that kind of
    exceptions on the web service.

    This is only effective when the exception is raised from within a
    published method.  For example, if the exception is raised by the field's
    validation, its specified status won't propagate to the response.
    """
    status = int(status)

    def func(value):
        if not issubclass(value, Exception):
            raise TypeError("Annotated value must be an exception class.")
        old = getattr(value, WEBSERVICE_ERROR, None)
        if old is not None and old != status:
            raise ValueError("Exception already has an error status", old)
        setattr(value, WEBSERVICE_ERROR, status)
        return value

    return func


class _method_annotator:
    """Base class for decorators annotating a method.

    The actual method will be wrapped in an IMethod specification once the
    Interface is complete. So we save the annotations in an attribute of the
    method, and the @exported_as_webservice_entry() and
    @exported_as_webservice_collection() decorators will do the final
    tagging.
    """

    def __call__(self, method):
        """Annotates the function with the fixed arguments."""
        # Everything in the function dictionary ends up as tagged value
        # in the interface method specification.
        annotations = method.__dict__.get(LAZR_WEBSERVICE_EXPORTED, None)
        if annotations is None:
            # Create a new versioned dict which associates
            # annotation data with the earliest active version of the
            # web service. Future @webservice_version annotations will
            # push later versions onto the VersionedDict, allowing
            # new versions to specify annotation data that conflicts
            # with old versions.
            #
            # Because we don't know the name of the earliest version
            # published by the web service (we won't know this until
            # runtime), we'll use None as the name of the earliest
            # version.
            annotations = VersionedDict()
            annotations.push(None)

            # The initial presumption is that an operation is not
            # published in the earliest version of the web service. An
            # @export_*_operation declaration will modify
            # annotations['type'] in place to signal that it is in
            # fact being published.
            annotations["type"] = REMOVED_OPERATION_TYPE
            method.__dict__[LAZR_WEBSERVICE_EXPORTED] = annotations
        self.annotate_method(method, annotations)
        return method

    def annotate_method(self, method, annotations):
        """Add annotations for method.

        This method must be implemented by subclasses.

        :param f: the method being annotated.
        :param annotations: the dict containing the method annotations.

        The annotations will be copied to the lazr.webservice.exported tag
        by a class decorator.
        """
        raise NotImplementedError


def annotate_exported_methods(interface):
    """Sets the 'lazr.webservice.exported' tag on exported method."""

    for name, method in interface.namesAndDescriptions(True):
        if not IMethod.providedBy(method):
            continue
        annotation_stack = method.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if annotation_stack is None:
            continue
        if annotation_stack.get("type") is None:
            continue

        # Make sure that each version of the web service defines
        # a self-consistent view of this method.
        for version, annotations in annotation_stack.stack:
            if annotations["type"] == REMOVED_OPERATION_TYPE:
                # The method is published in other versions of the web
                # service, but not in this one. Don't try to validate this
                # version's annotations.
                continue

            # Method is exported under its own name by default.
            if "as" not in annotations:
                annotations["as"] = method.__name__

            # It's possible that call_with, operation_parameters, and/or
            # operation_returns_* weren't used.
            annotations.setdefault("call_with", {})
            annotations.setdefault("params", {})
            annotations.setdefault("return_type", None)

            # Make sure that all parameters exist and that we miss none.
            info = method.getSignatureInfo()
            defined_params = set(info["optional"])
            defined_params.update(info["required"])
            exported_params = set(annotations["params"])
            exported_params.update(annotations["call_with"])
            undefined_params = exported_params.difference(defined_params)
            if undefined_params and info["kwargs"] is None:
                raise TypeError(
                    'method "%s" doesn\'t have the following exported '
                    'parameters in version "%s": %s.'
                    % (
                        method.__name__,
                        _version_name(version),
                        ", ".join(sorted(undefined_params)),
                    )
                )
            missing_params = set(info["required"]).difference(exported_params)
            if missing_params:
                raise TypeError(
                    'method "%s" is missing definitions for parameter(s) '
                    'exported in version "%s": %s'
                    % (
                        method.__name__,
                        _version_name(version),
                        ", ".join(sorted(missing_params)),
                    )
                )

            _update_default_and_required_params(annotations["params"], info)


def _update_default_and_required_params(params, method_info):
    """Set missing default/required based on the method signature."""
    optional = method_info["optional"]
    required = method_info["required"]
    for name, param_def in params.items():
        # If the method parameter is optional and the param didn't have
        # a default, set it to the same as the method.
        if name in optional and param_def.default is None:
            default = optional[name]
            param_def.default = default
            param_def.required = False
        elif name in required and param_def.default is not None:
            # A default was provided, so the parameter isn't required.
            param_def.required = False
        else:
            # Nothing to do for that case.
            pass


class call_with(_method_annotator):
    """Decorator specifying fixed parameters for exported methods."""

    def __init__(self, **params):
        """Specify fixed values for parameters."""
        _check_called_from_interface_def("%s()" % self.__class__.__name__)
        self.params = params

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations["call_with"] = self.params


class mutator_for(_method_annotator):
    """Decorator indicating that an exported method mutates a field.

    The method can be invoked through POST, or by setting a value for
    the given field as part of a PUT or PATCH request.
    """

    def __init__(self, field):
        """Specify the field for which this method is a mutator."""
        self.field = field

    def annotate_method(self, method, annotations):
        """See `_method_annotator`.

        Store information about the mutator method with the field.
        """

        if not self.field.readonly:
            raise TypeError(
                "Only a read-only field can have a mutator " "method."
            )

        # The mutator method must take only one argument, not counting
        # arguments with values fixed by call_with().
        free_params = _free_parameters(method, annotations)
        if len(free_params) != 1:
            raise TypeError(
                "A mutator method must take one and only one "
                "non-fixed argument. %s takes %d."
                % (method.__name__, len(free_params))
            )

        # We need to keep mutator annotations in a separate dictionary
        # from the field's main annotations because we're not
        # processing the field.  We're processing a named operation,
        # and we have no idea where the named operation's current
        # version fits into the field's annotations.
        version, method_annotations = annotations.stack[-1]
        mutator_annotations = self.field.queryTaggedValue(
            LAZR_WEBSERVICE_MUTATORS
        )
        if version in mutator_annotations:
            raise TypeError(
                "A field can only have one mutator method for version %s; "
                "%s makes two." % (_version_name(version), method.__name__)
            )
        mutator_annotations[version] = (method, dict(method_annotations))
        method_annotations["is_mutator"] = True


class accessor_for(_method_annotator):
    """Decorator indicating that an method is an accessor for a field.

    The method can be invoked by accessing the field's URL.
    """

    def __init__(self, field):
        """Specify the field for which this method is a mutator."""
        self.field = field

    def annotate_method(self, method, annotations):
        """See `_method_annotator`.

        Store information about the accessor method with the field.
        """
        # We need to keep accessor annotations in a separate dictionary
        # from the field's main annotations because we're not processing
        # the field.  We're processing a named operation, and we have no
        # idea where the named operation's current version fits into the
        # field's annotations.
        version, method_annotations = annotations.stack[-1]
        accessor_annotations = self.field.queryTaggedValue(
            LAZR_WEBSERVICE_ACCESSORS
        )
        if version in accessor_annotations:
            raise TypeError(
                "A field can only have one accessor method for version %s; "
                "%s makes two." % (_version_name(version), method.__name__)
            )
        accessor_annotations[version] = (method, dict(method_annotations))
        method_annotations["is_accessor"] = True


def _free_parameters(method, annotations):
    """Figure out which of a method's parameters are free.

    Parameters that have values fixed by call_with() are not free.
    """
    signature = fromFunction(method).getSignatureInfo()
    return set(signature["required"]) - set(
        annotations.get("call_with", {}).keys()
    )


class operation_for_version(_method_annotator):
    """Decorator specifying which version of the webservice is defined.

    Decorators processed after this one will decorate the given web
    service version and, by default, subsequent versions will inherit
    their values. Subsequent versions may provide conflicting values,
    but those values will not affect this version.
    """

    def __init__(self, version):
        _check_called_from_interface_def("%s()" % self.__class__.__name__)
        self.version = version

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        # The annotations dict is a VersionedDict. Push a new dict
        # onto its stack, labeled with the version number, and copy in
        # the old version's annotations so that this version can
        # modify those annotations without destroying them.
        annotations.push(self.version)


class operation_removed_in_version(operation_for_version):
    """Decoration removing this operation from the web service.

    This operation will not be present in the given version of the web
    service, or any subsequent version, unless it's re-published with
    an export_*_operation method.
    """

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        # The annotations dict is a VersionedDict. Push a new dict
        # onto its stack, labeled with the version number. Make sure the
        # new dict is empty rather than copying the old annotations
        annotations.push(self.version, True)

        # We need to set a special 'type' so that lazr.restful can
        # easily distinguish a method that's not present in the latest
        # version from a method that was incompletely annotated.
        annotations["type"] = REMOVED_OPERATION_TYPE


class export_operation_as(_method_annotator):
    """Decorator specifying the name to export the method as."""

    def __init__(self, name):
        _check_called_from_interface_def("%s()" % self.__class__.__name__)
        self.name = name

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations["as"] = self.name


class rename_parameters_as(_method_annotator):
    """Decorator specifying the name to export the method parameters as."""

    def __init__(self, **params):
        """params is of the form method_parameter_name=webservice_name."""
        _check_called_from_interface_def("%s()" % self.__class__.__name__)
        self.params = params

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        param_defs = annotations.get("params")
        if param_defs is None:
            raise TypeError(
                '"%s" isn\'t exported on the webservice.' % method.__name__
            )
        for name, export_as in self.params.items():
            if name not in param_defs:
                raise TypeError(
                    'rename_parameters_as(): no "%s" parameter is exported.'
                    % name
                )
            param_defs[name].__name__ = export_as


class operation_parameters(_method_annotator):
    """Specify the parameters taken by the exported operation.

    The decorator takes a list of `IField` describing the parameters. The name
    of the underlying method parameter is taken from the argument name.
    """

    def __init__(self, **params):
        """params is of the form method_parameter_name=Field()."""
        _check_called_from_interface_def("%s()" % self.__class__.__name__)
        self.params = params

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        # It's possible that another decorator already created the params
        # annotation.
        params = annotations.setdefault("params", {})
        for name, param in self.params.items():
            if not IField.providedBy(param):
                raise TypeError(
                    'export definition of "%s" in method "%s" must '
                    "provide IField: %r" % (name, method.__name__, param)
                )
            if name in params:
                raise TypeError("'%s' parameter is already defined." % name)

            # By default, parameters are exported under their own name.
            param.__name__ = name

            params[name] = param


class operation_returns_entry(_method_annotator):
    """Specify that the exported operation returns an entry.

    The decorator takes a single argument: an interface that's been
    exported as an entry.
    """

    def __init__(self, schema):
        _check_called_from_interface_def("%s()" % self.__class__.__name__)
        if not IInterface.providedBy(schema):
            raise TypeError(
                "Entry type %s does not provide IInterface." % schema
            )
        self.return_type = Reference(schema=schema)

    def annotate_method(self, method, annotations):
        annotations["return_type"] = self.return_type


class operation_returns_collection_of(_method_annotator):
    """Specify that the exported operation returns a collection.

    The decorator takes one required argument, "schema", an interface that's
    been exported as an entry.
    """

    def __init__(self, schema):
        _check_called_from_interface_def("%s()" % self.__class__.__name__)
        if not IInterface.providedBy(schema):
            raise TypeError(
                "Collection value type %s does not provide "
                "IInterface." % schema
            )
        self.return_type = CollectionField(value_type=Reference(schema=schema))

    def annotate_method(self, method, annotations):
        annotations["return_type"] = self.return_type


class _export_operation(_method_annotator):
    """Basic implementation for the webservice operation method decorators."""

    # Should be overriden in subclasses with the string to use as 'type'.
    type = None

    def __init__(self):
        _check_called_from_interface_def("%s()" % self.__class__.__name__)

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations["type"] = self.type


class export_factory_operation(_export_operation):
    """Decorator marking a method as being a factory on the webservice."""

    type = "factory"

    def __init__(self, interface, field_names):
        """Creates a factory decorator.

        :param interface: The interface where fields specified in field_names
            are looked-up.
        :param field_names: The names of the fields in the schema that
            are used as parameters by this factory.
        """
        # pylint: disable-msg=W0231
        _check_called_from_interface_def("%s()" % self.__class__.__name__)
        self.interface = interface
        self.params = OrderedDict()
        for name in field_names:
            field = interface.get(name)
            if field is None:
                raise TypeError(
                    "%s doesn't define '%s'." % (interface.__name__, name)
                )
            if not IField.providedBy(field):
                raise TypeError(
                    "%s.%s doesn't provide IField."
                    % (interface.__name__, name)
                )
            self.params[name] = copy_field(field)

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        super().annotate_method(method, annotations)
        annotations["creates"] = self.interface
        annotations["params"] = self.params
        annotations["return_type"] = ObjectLink(schema=self.interface)


class cache_for(_method_annotator):
    """Decorator specifying how long a response may be cached by a client."""

    def __init__(self, duration):
        """Specify the duration, in seconds, of the caching resource."""
        if not isinstance(duration, int):
            raise TypeError(
                "Caching duration should be an integer type, not %s"
                % duration.__class__.__name__
            )
        if duration <= 0:
            raise ValueError(
                "Caching duration should be a positive number: %s" % duration
            )
        self.duration = duration

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations["cache_for"] = self.duration


class scoped(_method_annotator):
    """Decorator assigning scopes to a method.

    This may be used to grant authentication tokens that are only valid for
    certain webservice operations.

    The decorator takes a collection of scope names as positional arguments.
    """

    def __init__(self, *scopes):
        for scope in scopes:
            if not isinstance(scope, str):
                raise TypeError(
                    "Scope should be a string type, not %s"
                    % scope.__class__.__name__
                )
        self.scopes = scopes

    def annotate_method(self, method, annotations):
        """See `_method_annotator`."""
        annotations["scopes"] = list(self.scopes)


class export_read_operation(_export_operation):
    """Decorator marking a method for export as a read operation."""

    type = "read_operation"


class export_write_operation(_export_operation):
    """Decorator marking a method for export as a write operation."""

    type = "write_operation"


class export_destructor_operation(_export_operation):
    """Decorator indicating that an exported method destroys an entry.

    The method will be invoked when the client sends a DELETE request to
    the entry.
    """

    type = "destructor"

    def annotate_method(self, method, annotation_stack):
        """See `_method_annotator`.

        Store information about the mutator method with the method.

        Every version must have a self-consistent set of annotations.
        """
        super().annotate_method(method, annotation_stack)
        # The mutator method must take no arguments, not counting
        # arguments with values fixed by call_with().
        for version, annotations in annotation_stack.stack:
            if annotations["type"] == REMOVED_OPERATION_TYPE:
                continue
            free_params = _free_parameters(method, annotations)
            if len(free_params) != 0:
                raise TypeError(
                    "A destructor method must take no non-fixed arguments. "
                    'In version %s, the "%s" method takes %d: "%s".'
                    % (
                        _version_name(version),
                        method.__name__,
                        len(free_params),
                        '", "'.join(free_params),
                    )
                )


def _check_tagged_interface(interface, type):
    """Make sure that the interface is exported under the proper type."""
    if not isinstance(interface, InterfaceClass):
        raise TypeError("not an interface.")

    tag = interface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    if tag is None:
        raise TypeError(
            "'%s' isn't tagged for webservice export." % interface.__name__
        )
    elif tag["type"] != type:
        art = "a"
        if type == "entry":
            art = "an"
        raise TypeError(
            "'%s' isn't exported as %s %s." % (interface.__name__, art, type)
        )


def generate_entry_interfaces(interface, contributors=[], *versions):
    """Create IEntry subinterfaces based on the tags in `interface`.

    :param interface: The data model interface to use as the basis
        for a number of IEntry subinterfaces.
    :param versions: The list of versions published by this service, earliest
        versions first.
    :return: A list of 2-tuples (version, interface), in the same order
        as `versions`.
    """

    _check_tagged_interface(interface, "entry")
    versions = list(versions)

    # Make sure any given version defines only one destructor method.
    destructor_for_version = {}
    for name, method in interface.namesAndDescriptions(True):
        if not IMethod.providedBy(method):
            continue
        method_annotations = method.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if method_annotations is None:
            continue
        for version, annotations in method_annotations.stack:
            if annotations.get("type") == export_destructor_operation.type:
                destructor = destructor_for_version.get(version)
                if destructor is not None:
                    raise TypeError(
                        "An entry can only have one destructor method for "
                        "version %s; %s and %s make two."
                        % (
                            _version_name(version),
                            method.__name__,
                            destructor.__name__,
                        )
                    )
                destructor_for_version[version] = method

    # Build a data set describing this entry, as it appears in each
    # version of the web service in which it appears at all.
    entry_tags = interface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    stack = entry_tags.stack

    earliest_version = versions[0]
    # Now that we know the name of the earliest version, get rid of
    # any None at the beginning of the stack.
    if stack[0].version is None:
        entry_tags.rename_version(None, earliest_version)

    # If require_explicit_versions is set, make sure the first version
    # to set 'exported' also sets '_as_of_was_used'.
    _enforce_explicit_version(entry_tags, 'Entry "%s": ' % interface.__name__)

    # Make sure there's one set of entry tags for every version of the
    # web service, including versions in which this entry is not
    # published.
    entry_tags.normalize_for_versions(
        versions,
        {"type": ENTRY_TYPE, "exported": False},
        'Interface "%s": ' % interface.__name__,
    )

    # Next, we'll normalize each published field. A normalized field
    # has a set of annotations for every version in which the entry is
    # published. We'll make a list of the published fields, which
    # we'll iterate over once for each version.
    tags_for_published_fields = []
    for iface in itertools.chain([interface], contributors):
        for name, field in getFieldsInOrder(iface):
            tag_stack = field.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
            if tag_stack is None:
                # This field is not published at all.
                continue
            error_message_prefix = 'Field "%s" in interface "%s": ' % (
                name,
                iface.__name__,
            )
            _normalize_field_annotations(field, versions, error_message_prefix)
            tags_for_published_fields.append((name, field, tag_stack))

    generated_interfaces = []
    entry_tags = interface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    for version in versions:
        entry_tags_this_version = entry_tags.dict_for_name(version)
        if entry_tags_this_version.get("exported") is False:
            # Don't define an entry interface for this version at all.
            continue
        attrs = {}
        for name, field, tag_stack in tags_for_published_fields:
            tags = tag_stack.dict_for_name(version)
            if tags.get("exported") is False:
                continue
            mutated_by, mutated_by_annotations = tags.get(
                "mutator_annotations", (None, {})
            )
            readonly = field.readonly and mutated_by is None
            if "readonly" in tags:
                publish_as_readonly = tags.get("readonly")
                if readonly and not publish_as_readonly:
                    raise TypeError(
                        (
                            "%s.%s is defined as a read-only field, so you "
                            "can't just declare it to be read-write in "
                            "the web service: you must define a mutator."
                        )
                        % (interface.__name__, field.__name__)
                    )
                if not readonly and publish_as_readonly:
                    # The field is read-write internally, but the
                    # developer wants it to be read-only through the web
                    # service.
                    readonly = True
            attrs[tags["as"]] = copy_field(
                field, __name__=tags["as"], readonly=readonly
            )
        class_name = _versioned_class_name(
            "%sEntry" % interface.__name__, version
        )
        entry_interface = InterfaceClass(
            class_name,
            bases=(IEntry,),
            attrs=attrs,
            __doc__=interface.__doc__,
            __module__=interface.__module__,
        )

        versioned_tag = entry_tags.dict_for_name(version)
        entry_interface.setTaggedValue(
            LAZR_WEBSERVICE_NAME,
            dict(
                singular=versioned_tag["singular_name"],
                plural=versioned_tag["plural_name"],
                publish_web_link=versioned_tag["publish_web_link"],
            ),
        )
        generated_interfaces.append(VersionedObject(version, entry_interface))
    return generated_interfaces


def generate_entry_adapters(
    content_interface, contributors, webservice_interfaces
):
    """Create classes adapting from content_interface to webservice_interfaces.

    Unlike with generate_collection_adapter and
    generate_operation_adapter, the simplest implementation generates
    an entry adapter for every version at the same time.

    :param content_interface: The original data model interface being exported.

    :param webservice_interfaces: A list of 2-tuples
     (version string, webservice interface) containing the generated
     interfaces for each version of the web service.

    :param return: A list of 2-tuples (version string, adapter class)
    """
    _check_tagged_interface(content_interface, "entry")

    # Go through the fields and build up a picture of what this entry looks
    # like for every version.
    adapters_by_version = {}
    fields = list(getFields(content_interface).items())
    for version, iface in webservice_interfaces:
        fields.extend(getFields(iface).items())
    for name, field in fields:
        tag_stack = field.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag_stack is None:
            continue
        for tags_version, tags in tag_stack.stack:
            # Has this version been mentioned before? If not, add a
            # dictionary to adapters_by_version. This dictionary will
            # be turned into an adapter class for this version.
            adapter_dict = adapters_by_version.setdefault(tags_version, {})

            # Set '_orig_interfaces' as early as possible as we want that
            # attribute (even if empty) on all adapters.
            orig_interfaces = adapter_dict.setdefault("_orig_interfaces", {})

            # Figure out the mutator for this version and add it to
            # this version's adapter class dictionary.
            if tags.get("exported") is False:
                continue
            mutator, mutator_annotations = tags.get(
                "mutator_annotations", (None, {})
            )
            accessor, accessor_annotations = tags.get(
                "accessor_annotations", (None, {})
            )

            # Always use the field's original_name here as we've combined
            # fields from the content interface with fields of the webservice
            # interfaces (where they may have different names).
            orig_name = tags["original_name"]

            # Some fields may be provided by an adapter of the content class
            # instead of being provided directly by the content class. In
            # these cases we'd need to adapt the content class before trying
            # to access the field, so to simplify things we always do the
            # adaptation and rely on the fact that it will be a no-op when an
            # we adapt an object into an interface it already provides.
            orig_iface = content_interface
            for contributor in contributors:
                if orig_name in contributor:
                    orig_iface = contributor
            assert orig_name in orig_iface, (
                "Could not find interface where %s is defined" % orig_name
            )

            if accessor is not None and mutator is not None:
                prop = PropertyWithAccessorAndMutator(
                    orig_name,
                    "context",
                    accessor,
                    accessor_annotations,
                    mutator,
                    mutator_annotations,
                    orig_iface,
                )
            elif mutator is not None and accessor is None:
                prop = PropertyWithMutator(
                    orig_name,
                    "context",
                    mutator,
                    mutator_annotations,
                    orig_iface,
                )
            elif accessor is not None and mutator is None:
                prop = PropertyWithAccessor(
                    orig_name,
                    "context",
                    accessor,
                    accessor_annotations,
                    orig_iface,
                )
            else:
                prop = _ScopeChecker(orig_name, "context", orig_iface)

            adapter_dict[tags["as"]] = prop

            # A dict mapping field names to the interfaces where they came
            # from.
            orig_interfaces[name] = orig_iface

    adapters = []
    for version, webservice_interface in webservice_interfaces:
        if not isinstance(webservice_interface, InterfaceClass):
            raise TypeError("webservice_interface is not an interface.")
        class_dict = adapters_by_version.get(version, {})

        # If this interface doesn't export a single field/operation,
        # class_dict will be empty, and so we'll add '_orig_interfaces'
        # manually as it should be always available, even if empty.
        if class_dict == {}:
            class_dict["_orig_interfaces"] = {}

        class_dict["schema"] = webservice_interface
        class_dict["__doc__"] = webservice_interface.__doc__
        # The webservice interface class name already includes the version
        # string, so there's no reason to add it again to the end
        # of the class name.
        classname = "%sAdapter" % webservice_interface.__name__[1:]
        factory = type(classname, (Entry,), class_dict)
        classImplements(factory, webservice_interface)
        protect_schema(
            factory, webservice_interface, write_permission=CheckerPublic
        )
        adapters.append(VersionedObject(version, factory))
    return adapters


def params_with_dereferenced_user(params):
    """Make a copy of the given parameters with REQUEST_USER dereferenced."""
    params = params.copy()
    for name, value in params.items():
        if value is REQUEST_USER:
            params[name] = getUtility(
                IWebServiceConfiguration
            ).get_request_user()
    return params


def _check_request(context, required_scopes):
    """Check whether the current request may call a particular method.

    See `IWebServiceConfiguration.checkRequest`.
    """
    check_request = getattr(
        getUtility(IWebServiceConfiguration), "checkRequest", None
    )
    if check_request is not None:
        check_request(context, required_scopes)


class _ScopeChecker(Passthrough):
    """Check scopes before allowing access to properties."""

    def __get__(self, inst, cls=None):
        context = getattr(inst, self.contextvar)
        if self.adaptation is not None:
            context = self.adaptation(context)
        _check_request(context, None)
        return super().__get__(inst, cls=cls)

    def __set__(self, inst, value):
        context = getattr(inst, self.contextvar)
        if self.adaptation is not None:
            context = self.adaptation(context)
        _check_request(context, None)
        return super().__set__(inst, value)


class _AccessorWrapper:
    """A wrapper class for properties with accessors.

    We define this separately from PropertyWithAccessor and
    PropertyWithAccessorAndMutator to avoid multiple inheritance issues.
    """

    def __get__(self, obj, *args):
        """Call the accessor method to get the value."""
        params = params_with_dereferenced_user(
            self.accessor_annotations.get("call_with", {})
        )
        context = getattr(obj, self.contextvar)
        if self.adaptation is not None:
            context = self.adaptation(context)
        _check_request(context, None)
        # Error checking code in accessor_for() guarantees that there
        # is one and only one non-fixed parameter for the accessor
        # method.
        return getattr(context, self.accessor)(**params)


class _MutatorWrapper:
    """A wrapper class for properties with mutators.

    We define this separately from PropertyWithMutator and
    PropertyWithAccessorAndMutator to avoid multiple inheritance issues.
    """

    def __set__(self, obj, new_value):
        """Call the mutator method to set the value."""
        params = params_with_dereferenced_user(
            self.mutator_annotations.get("call_with", {})
        )
        context = getattr(obj, self.contextvar)
        if self.adaptation is not None:
            context = self.adaptation(context)
        _check_request(context, None)
        # Error checking code in mutator_for() guarantees that there
        # is one and only one non-fixed parameter for the mutator
        # method.
        getattr(context, self.mutator)(new_value, **params)


class PropertyWithAccessor(_AccessorWrapper, _ScopeChecker):
    """A property with a accessor method."""

    def __init__(
        self, name, context, accessor, accessor_annotations, adaptation
    ):
        super().__init__(name, context, adaptation)
        self.accessor = accessor.__name__
        self.accessor_annotations = accessor_annotations


class PropertyWithMutator(_MutatorWrapper, _ScopeChecker):
    """A property with a mutator method."""

    def __init__(
        self, name, context, mutator, mutator_annotations, adaptation
    ):
        super().__init__(name, context, adaptation)
        self.mutator = mutator.__name__
        self.mutator_annotations = mutator_annotations


class PropertyWithAccessorAndMutator(
    _AccessorWrapper, _MutatorWrapper, Passthrough
):
    """A Property with both an accessor an a mutator."""

    def __init__(
        self,
        name,
        context,
        accessor,
        accessor_annotations,
        mutator,
        mutator_annotations,
        adaptation,
    ):
        super().__init__(name, context, adaptation)
        self.accessor = accessor.__name__
        self.accessor_annotations = accessor_annotations
        self.mutator = mutator.__name__
        self.mutator_annotations = mutator_annotations


class CollectionEntrySchema:
    """A descriptor for converting a model schema into an entry schema.

    The entry schema class for a resource may not have been defined at
    the time the collection adapter is generated, but the data model
    class certainly will have been. This descriptor performs the lookup
    as needed, at runtime.
    """

    def __init__(self, model_schema):
        """Initialize with a model schema."""
        self.model_schema = model_schema

    def __get__(self, instance, owner):
        """Look up the entry schema that adapts the model schema."""
        if instance is None or instance.request is None:
            request = get_current_web_service_request()
        else:
            request = instance.request
        request_interface = getUtility(
            IWebServiceVersion, name=request.version
        )
        entry_class = getGlobalSiteManager().adapters.lookup(
            (self.model_schema, request_interface), IEntry
        )
        if entry_class is None:
            return None
        return EntryAdapterUtility(entry_class).entry_interface


class BaseCollectionAdapter(Collection):
    """Base for generated ICollection adapter."""

    # These attributes will be set in the generated subclass.
    method_name = None
    params = None

    def find(self):
        """See `ICollection`."""
        method = getattr(self.context, self.method_name)
        params = params_with_dereferenced_user(self.params)
        return method(**params)


def generate_collection_adapter(interface, version=None):
    """Create a class adapting from interface to ICollection."""
    _check_tagged_interface(interface, "collection")

    tag = interface.getTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    default_content_by_version = tag["collection_default_content"]
    assert (
        version in default_content_by_version
    ), "'%s' isn't tagged for export to web service " "version '%s'." % (
        interface.__name__,
        version,
    )
    method_name, params = default_content_by_version[version]
    entry_schema = tag["collection_entry_schema"]
    class_dict = {
        "entry_schema": CollectionEntrySchema(entry_schema),
        "method_name": method_name,
        "params": params,
        "__doc__": interface.__doc__,
    }
    classname = _versioned_class_name(
        "%sCollectionAdapter" % interface.__name__[1:], version
    )
    factory = type(classname, (BaseCollectionAdapter,), class_dict)

    protect_schema(factory, ICollection)
    return factory


class BaseResourceOperationAdapter(ResourceOperation):
    """Base class for generated operation adapters."""

    def _getMethod(self):
        return getattr(self._orig_iface(self.context), self._method_name)

    def _getMethodParameters(self, kwargs):
        """Return the method parameters.

        This takes the validated parameters list and handle any possible
        renames, and adds the parameters fixed using @call_with.

        :returns: a dictionary.
        """
        # Handle renames.
        renames = {
            param_def.__name__: orig_name
            for orig_name, param_def in self._export_info["params"].items()
            if param_def.__name__ != orig_name
        }
        params = OrderedDict()
        for name, value in kwargs.items():
            name = renames.get(name, name)
            params[name] = value

        # Handle fixed parameters.
        params.update(
            params_with_dereferenced_user(self._export_info["call_with"])
        )
        return params

    def call(self, **kwargs):
        """See `ResourceOperation`."""
        params = self._getMethodParameters(kwargs)

        # For responses to GET requests, tell the client to cache the
        # response.
        if (
            IResourceGETOperation.providedBy(self)
            and "cache_for" in self._export_info
        ):
            self.request.response.setHeader(
                "Cache-control", "max-age=%i" % self._export_info["cache_for"]
            )

        _check_request(self.context, self._export_info.get("scopes", []))
        result = self._getMethod()(**params)
        return self.encodeResult(result)


class BaseFactoryResourceOperationAdapter(BaseResourceOperationAdapter):
    """Base adapter class for factory operations."""

    def call(self, **kwargs):
        """See `ResourceOperation`.

        Factory uses the 201 status code on success and sets the Location
        header to the URL to the created object.
        """
        params = self._getMethodParameters(kwargs)
        result = self._getMethod()(**params)
        response = self.request.response
        response.setStatus(201)
        response.setHeader("Location", absoluteURL(result, self.request))
        return ""


def generate_operation_adapter(method, version=None):
    """Create an IResourceOperation adapter for the exported method.

    :param version: The name of the version for which to generate an
      operation adapter. None means to generate an adapter for the
      earliest version. If
      IWebServiceConfiguration.require_explicit_versions is set,
      passing in None will cause an error.
    """
    if not IMethod.providedBy(method):
        raise TypeError("%r doesn't provide IMethod." % method)
    tag = method.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    if tag is None:
        raise TypeError(
            "'%s' isn't tagged for webservice export." % method.__name__
        )
    match = tag.dict_for_name(version)
    if match is None:
        raise AssertionError(
            "'%s' isn't tagged for export to web service "
            "version '%s'" % (method.__name__, version)
        )
    config = getUtility(IWebServiceConfiguration)
    if version is None:
        # This code path is not currently used except in a test, since
        # generate_and_register_webservice_operations never passes in
        # None for `version`.
        version = config.active_versions[0]
        if config.require_explicit_versions:
            raise ValueError(
                '"%s" is implicitly tagged for export to web service '
                'version "%s", but the service configuration requires '
                "all version declarations to be explicit. You should add "
                '@operation_for_version("%s") to the bottom of the '
                "annotation stack." % (method.__name__, version, version)
            )

    bases = (BaseResourceOperationAdapter,)
    operation_type = match["type"]
    if operation_type == "read_operation":
        prefix = "GET"
        provides = IResourceGETOperation
    elif operation_type in ("factory", "write_operation"):
        provides = IResourcePOSTOperation
        prefix = "POST"
        if operation_type == "factory":
            bases = (BaseFactoryResourceOperationAdapter,)
    elif operation_type == "destructor":
        provides = IResourceDELETEOperation
        prefix = "DELETE"
    else:
        raise AssertionError("Unknown method export type: %s" % operation_type)

    return_type = match["return_type"]
    scopes = match.get("scopes") or []

    name = _versioned_class_name(
        "%s_%s_%s" % (prefix, method.interface.__name__, match["as"]), version
    )
    class_dict = {
        "params": tuple(match["params"].values()),
        "return_type": return_type,
        "scopes": tuple(scopes),
        "_orig_iface": method.interface,
        "_export_info": match,
        "_method_name": method.__name__,
        "__doc__": method.__doc__,
    }

    if operation_type == "write_operation":
        class_dict["send_modification_event"] = True
    factory = type(name, bases, class_dict)
    classImplements(factory, provides)
    protect_schema(factory, provides)

    return factory


def _normalize_field_annotations(field, versions, error_prefix=""):
    """Make sure a field has annotations for every published version.

    If a field lacks annotations for a given version, it will not show
    up in that version's adapter interface. This function makes sure
    version n+1 inherits version n's behavior, by copying it that
    behavior over.

    If the earliest version has both an implicit definition (from
    keyword arguments) and an explicit definition, the two definitions
    are consolidated.

    Since we have the list of versions available, this is also a good
    time to do some error checking: make sure that version annotations
    are not duplicated or in the wrong order.

    Finally, this is a good time to integrate the mutator annotations
    into the field annotations.
    """
    versioned_dict = field.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    mutator_annotations = field.queryTaggedValue(LAZR_WEBSERVICE_MUTATORS)
    accessor_annotations = field.queryTaggedValue(LAZR_WEBSERVICE_ACCESSORS)

    earliest_version = versions[0]
    stack = versioned_dict.stack

    if (
        len(stack) >= 2
        and stack[0].version is None
        and stack[1].version == earliest_version
    ):
        # The behavior of the earliest version is defined with keyword
        # arguments, but the first explicitly-defined version also
        # refers to the earliest version. We need to consolidate the
        # versions.
        implicit_earliest_version = stack[0].object
        explicit_earliest_version = stack[1].object
        for key, value in explicit_earliest_version.items():
            if key not in implicit_earliest_version:
                # This key was defined for the earliest version using a
                # configuration dictionary, but not defined at all
                # using keyword arguments.  The configuration
                # dictionary takes precedence.
                continue
            implicit_value = implicit_earliest_version[key]
            if implicit_value == value:
                # The two values are in sync.
                continue
            if key == "as" and implicit_value == field.__name__:
                # The implicit value was set by the system, not by the
                # user. The later value will simply take precedence.
                continue
            raise ValueError(
                error_prefix + 'Annotation "%s" has conflicting values '
                'for the earliest version: "%s" (from keyword arguments) '
                'and "%s" (defined explicitly).' % (key, implicit_value, value)
            )
        stack[0].object.update(stack[1].object)
        stack.remove(stack[1])

    # Now that we know the name of the earliest version, get rid of
    # any None at the beginning of the stack.
    if stack[0].version is None:
        versioned_dict.rename_version(None, earliest_version)

    # If require_explicit_versions is set, make sure the first version
    # to set 'exported' also sets '_as_of_was_used'.
    _enforce_explicit_version(versioned_dict, error_prefix)

    # Make sure there is at most one mutator for the earliest version.
    # If there is one, move it from the mutator-specific dictionary to
    # the normal tag stack.
    implicit_earliest_mutator = mutator_annotations.get(None, None)
    explicit_earliest_mutator = mutator_annotations.get(earliest_version, None)
    if (
        implicit_earliest_mutator is not None
        and explicit_earliest_mutator is not None
    ):
        raise ValueError(
            error_prefix + " Both implicit and explicit mutator definitions "
            "found for earliest version %s." % earliest_version
        )
    earliest_mutator = implicit_earliest_mutator or explicit_earliest_mutator
    if earliest_mutator is not None:
        stack[0].object["mutator_annotations"] = earliest_mutator

    # Make sure there is at most one accessor for the earliest version.
    # If there is one, move it from the accessor-specific dictionary to
    # the normal tag stack.
    implicit_earliest_accessor = accessor_annotations.get(None, None)
    explicit_earliest_accessor = accessor_annotations.get(
        earliest_version, None
    )
    if (
        implicit_earliest_accessor is not None
        and explicit_earliest_accessor is not None
    ):
        raise ValueError(
            error_prefix + " Both implicit and explicit accessor definitions "
            "found for earliest version %s." % earliest_version
        )
    earliest_accessor = (
        implicit_earliest_accessor or explicit_earliest_accessor
    )
    if earliest_accessor is not None:
        stack[0].object["accessor_annotations"] = earliest_accessor

    # Fill out the stack so that there is one set of tags for each
    # version.
    versioned_dict.normalize_for_versions(
        versions, dict(exported=False), error_prefix
    )

    # Make sure that a mutator defined in version N is inherited in
    # version N+1.
    most_recent_mutator_tags = earliest_mutator
    for version in versions[1:]:
        most_recent_mutator_tags = mutator_annotations.get(
            version, most_recent_mutator_tags
        )
        # Install a (possibly inherited) mutator for this field in
        # this version.
        if most_recent_mutator_tags is not None:
            tags_for_version = versioned_dict.dict_for_name(version)
            tags_for_version["mutator_annotations"] = copy.deepcopy(
                most_recent_mutator_tags
            )

    # Make sure that a accessor defined in version N is inherited in
    # version N+1.
    most_recent_accessor_tags = earliest_accessor
    for version in versions[1:]:
        most_recent_accessor_tags = accessor_annotations.get(
            version, most_recent_accessor_tags
        )
        # Install a (possibly inherited) accessor for this field in
        # this version.
        if most_recent_accessor_tags is not None:
            tags_for_version = versioned_dict.dict_for_name(version)
            tags_for_version["accessor_annotations"] = copy.deepcopy(
                most_recent_accessor_tags
            )

    return field


def _enforce_explicit_version(versioned_dict, error_prefix):
    """Raise ValueError if the explicit version requirement is not met.

    If the configuration has `require_explicit_versions` set, then
    the first version in the given VersionedDict to include a True
    value for 'exported' must also include a True value for
    '_as_of_was_used'.

    :param versioned_dict: a VersionedDict.
    :param error_prefix: a string to be prepended onto any error message.
    """
    if not getUtility(IWebServiceConfiguration).require_explicit_versions:
        return

    for version, annotations in versioned_dict.stack:
        if annotations.get("exported", False):
            if not annotations.get("_as_of_was_used", False):
                raise ValueError(
                    error_prefix + "Exported in version %s, but not"
                    " by using as_of. The service configuration"
                    " requires that you use as_of." % version
                )
            break


def _version_name(version):
    """Return a human-readable version name.

    If `version` is None (indicating the as-yet-unknown earliest
    version), returns "(earliest version)". Otherwise returns the version
    name.
    """
    if version is None:
        return "(earliest version)"
    return version


def _versioned_class_name(base_name, version):
    """Create a class name incorporating the given version string."""
    if version is None:
        # We need to incorporate the version into a Python class name,
        # but we won't find out the name of the earliest version until
        # runtime. Use a generic string that won't conflict with a
        # real version string.
        version = "__Earliest"
    name = "%s_%s" % (base_name, version)
    return make_identifier_safe(name)
