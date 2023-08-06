# Copyright 2008 Canonical Ltd.  All rights reserved.

"""ZCML registration directives for the LAZR webservice framework."""

__all__ = []


import collections
import inspect
import itertools

from zope.component import (
    adapter,
    getGlobalSiteManager,
    getUtility,
)
from zope.component.zcml import handler
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.processlifetime import IProcessStarting

from lazr.restful.declarations import (
    COLLECTION_TYPE,
    ENTRY_TYPE,
    LAZR_WEBSERVICE_EXPORTED,
    OPERATION_TYPES,
    REMOVED_OPERATION_TYPE,
    generate_collection_adapter,
    generate_entry_adapters,
    generate_entry_interfaces,
    generate_operation_adapter,
)
from lazr.restful.error import WebServiceExceptionView

from lazr.restful.interfaces import (
    ICollection,
    ICollectionField,
    IEntry,
    IReference,
    IResourceDELETEOperation,
    IResourceGETOperation,
    IResourcePOSTOperation,
    IWebServiceClientRequest,
    IWebServiceConfiguration,
    IWebServiceVersion,
)

from lazr.restful.utils import VersionedObject


# Keep track of entry and operation registrations so we can
# coherence-check them later.
REGISTERED_ENTRIES = []
REGISTERED_OPERATIONS = []

# Keep a global mapping of each interface's contributors, registered by
# contribute_to_interface and inspected by the entry generators.
REGISTERED_CONTRIBUTORS = collections.defaultdict(list)


def reset_globals():
    del REGISTERED_ENTRIES[:]
    del REGISTERED_OPERATIONS[:]
    REGISTERED_CONTRIBUTORS.clear()


try:
    from zope.testing.cleanup import addCleanUp
except ImportError:
    pass
else:
    addCleanUp(reset_globals)


class IRegisterDirective(Interface):
    """
    Directive to hook up webservice based on the declarations in a module.
    """

    module = GlobalObject(
        title="Module which will be inspected for webservice declarations"
    )


def contribute_to_interface(interface, info):
    tag = interface.getTaggedValue(LAZR_WEBSERVICE_EXPORTED)
    for iface in tag["contributes_to"]:
        if iface.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED) is None:
            raise AttemptToContributeToNonExportedInterface(
                "Interface %s contributes to %s, which is not "
                "exported." % (interface.__name__, iface.__name__)
            )

        # Check that no names conflict with the extended interface or
        # its contributors.
        contributors = REGISTERED_CONTRIBUTORS[iface]
        names = {}
        for iface in itertools.chain([iface, interface], contributors):
            for name, f in iface.namesAndDescriptions(all=True):
                if f.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED) is not None:
                    L = names.setdefault(name, [])
                    L.append(iface)
        for name, interfaces in names.items():
            if len(interfaces) > 1:
                raise ConflictInContributingInterfaces(name, interfaces)
        contributors.append(interface)


def generate_and_register_entry_adapters(interface, info, repository=None):
    """Generate an entry adapter for every version of the web service.

    This code generates an IEntry subinterface for every version, each
    subinterface based on the annotations in `interface` for that
    version. It then generates a set of factory classes for each
    subinterface, and registers each as an adapter for the appropriate
    version and version-specific interface.
    """
    # Get the list of versions.
    config = getUtility(IWebServiceConfiguration)
    versions = list(config.active_versions)
    contributors = REGISTERED_CONTRIBUTORS[interface]

    # Generate an interface and an adapter for every version.
    web_interfaces = generate_entry_interfaces(
        interface, contributors, *versions
    )
    web_factories = generate_entry_adapters(
        interface, contributors, web_interfaces
    )
    for index, (interface_version, web_interface) in enumerate(web_interfaces):
        factory_version, factory = web_factories[index]
        assert factory_version == interface_version, (
            "Generated interface and factory versions don't match up! "
            "%s vs. %s" % (factory_version, interface_version)
        )

        # If this is the earliest version, register against a generic
        # request interface rather than a version-specific one.  This
        # will make certain tests require less setup.
        if interface_version == versions[0]:
            interface_version = None
        register_adapter_for_version(
            factory, interface, interface_version, IEntry, "", info
        )

        # If we were given a repository, add the interface and version
        # to it.
        if repository is not None:
            repository.append(
                VersionedObject(interface_version, web_interface)
            )


def ensure_correct_version_ordering(name, version_list):
    """Make sure that a list mentions versions from earliest to latest.

    If an earlier version shows up after a later version, this is a
    sign that a developer was confused about version names when
    annotating the web service.

    :param name: The name of the object annotated with the
        possibly mis-ordered versions.

    :param version_list: The list of versions found in the interface.

    :raise AssertionError: If the given version list is not a
        earlier-to-later ordering of a subset of the web service's
        versions.
    """
    configuration = getUtility(IWebServiceConfiguration)
    actual_versions = configuration.active_versions
    # Replace None with the actual version number of the earliest
    # version.
    try:
        earliest_version_pos = version_list.index(None)
        version_list = list(version_list)
        version_list[earliest_version_pos] = actual_versions[0]
    except ValueError:
        # The earliest version was not mentioned in the version list.
        # Do nothing.
        pass

    # Sort version_list according to the list of actual versions.
    # If the sorted list is different from the unsorted list, at
    # least one version is out of place.
    sorted_version_list = sorted(version_list, key=actual_versions.index)
    if sorted_version_list != version_list:
        bad_versions = '", "'.join(version_list)
        good_versions = '", "'.join(sorted_version_list)
        msg = (
            'Annotations on "%s" put an earlier version on top of a '
            'later version: "%s". The correct order is: "%s".'
        )
        raise AssertionError(msg % (name, bad_versions, good_versions))


def register_adapter_for_version(
    factory, interface, version_name, provides, name, info
):
    """A version-aware wrapper for the registerAdapter operation.

    During web service generation we often need to register an adapter
    for a particular version of the web service. The way to do this is
    to register a multi-adapter using the interface being adapted to,
    plus the marker interface for the web service version.

    These marker interfaces are not available when the web service is
    being generated, but the version strings are available. So methods
    like register_webservice_operations use this function as a handler
    for the second stage of ZCML processing.

    This function simply looks up the appropriate marker interface and
    calls Zope's handler('registerAdapter').
    """
    if version_name is None:
        # This adapter is for the earliest supported version. Register
        # it against the generic IWebServiceClientRequest interface,
        # which is the superclass of the marker interfaces for every
        # specific version.
        marker = IWebServiceClientRequest
    else:
        # Look up the marker interface for the given version. This
        # will also ensure the given version string has an
        # IWebServiceVersion utility registered for it, and is not
        # just a random string.
        marker = getUtility(IWebServiceVersion, name=version_name)

    handler(
        "registerAdapter", factory, (interface, marker), provides, name, info
    )


def _is_exported_interface(member):
    """Helper for find_exported_interfaces; a predicate to inspect.getmembers.

    Returns True if member is a webservice-aware Exception or interface.
    """
    if (
        inspect.isclass(member)
        and issubclass(member, Exception)
        and getattr(member, "__lazr_webservice_error__", None) is not None
    ):
        # This is a webservice-aware Exception.
        return True
    if IInterface.providedBy(member):
        tag = member.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag is not None and tag["type"] in [ENTRY_TYPE, COLLECTION_TYPE]:
            # This is a webservice-aware interface.
            return True
    return False


def find_exported_interfaces(module):
    """Find all the interfaces in a module marked for export.

    It also includes exceptions that represents errors on the webservice.

    :return: iterator of interfaces.
    """
    try:
        module_all = set(module.__all__)

        def is_exported_name(name):
            return name in module_all

    except AttributeError:

        def is_exported_name(name):
            return not name.startswith("_")

    return (
        interface
        for name, interface in inspect.getmembers(
            module, _is_exported_interface
        )
        if is_exported_name(name)
    )


class ConflictInContributingInterfaces(Exception):
    """More than one interface tried to contribute a given attribute/method to
    another interface.
    """

    def __init__(self, name, interfaces):
        self.msg = (
            "'%s' is exported in more than one contributing interface: %s"
            % (name, ", ".join(i.__name__ for i in interfaces))
        )

    def __str__(self):
        return self.msg


class AttemptToContributeToNonExportedInterface(Exception):
    """An interface contributes to another one which is not exported."""


def register_webservice(context, module):
    """Generate and register web service adapters.

    All interfaces in the module are inspected, and appropriate interfaces and
    adapters are generated and registered for the ones marked for export on
    the web service.
    """
    if not inspect.ismodule(module):
        raise TypeError(
            "module attribute must be a module: %s, %s" % module, type(module)
        )

    for interface in find_exported_interfaces(module):
        if issubclass(interface, Exception):
            register_exception_view(context, interface)
            continue

        tag = interface.getTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag["type"] == ENTRY_TYPE:
            if tag.get("contributes_to"):
                # This isn't a standalone entry, so just register its
                # contributions in the global map. This has to be done
                # before entry and operation adapter generation, so we
                # customise the order.
                context.action(
                    discriminator=("webservice entry contributor", interface),
                    callable=contribute_to_interface,
                    args=(interface, context.info),
                    order=1,
                )
            else:
                context.action(
                    discriminator=("webservice entry interface", interface),
                    callable=generate_and_register_entry_adapters,
                    args=(interface, context.info, REGISTERED_ENTRIES),
                    order=2,
                )
        elif tag["type"] == COLLECTION_TYPE:
            for version in tag["collection_default_content"].keys():
                factory = generate_collection_adapter(interface, version)
                provides = ICollection
                context.action(
                    discriminator=(
                        "webservice versioned adapter",
                        interface,
                        provides,
                        "",
                        version,
                    ),
                    callable=register_adapter_for_version,
                    args=(
                        factory,
                        interface,
                        version,
                        provides,
                        "",
                        context.info,
                    ),
                )
        else:
            raise AssertionError("Unknown export type: %s" % tag["type"])
        context.action(
            discriminator=("webservice versioned operations", interface),
            args=(context, interface, REGISTERED_OPERATIONS),
            callable=generate_and_register_webservice_operations,
            order=2,
        )


@adapter(IProcessStarting)
def webservice_coherence_checks(registration):
    """Ensure the web service contains no references to unpublished objects.

    We are worried about fields that link to unpublished objects, and
    operations that have arguments or return values that are
    unpublished. An unpublished object may not be published at all, or
    it may not be published in the same version in which it's
    referenced.
    """
    global REGISTERED_ENTRIES
    global REGISTERED_OPERATIONS

    # Create a mapping of marker interfaces to version names.
    versions = getUtility(IWebServiceConfiguration).active_versions
    version_for_marker = {IWebServiceClientRequest: versions[0]}
    for version in versions:
        marker_interface = getUtility(IWebServiceVersion, name=version)
        version_for_marker[marker_interface] = version

    # For each version, build a list of all of the IEntries published
    # in that version's web service. This works because every IEntry
    # is explicitly registered for every version, even if there's been
    # no change since the last version. For the sake of performance,
    # the list is stored as a set of VersionedObject 2-tuples.
    available_registrations = set()
    registrations = getGlobalSiteManager().registeredAdapters()
    for registration in registrations:
        if not IInterface.providedBy(
            registration.provided
        ) or not registration.provided.isOrExtends(IEntry):
            continue
        interface, version_marker = registration.required
        available_registrations.add(
            VersionedObject(version_for_marker[version_marker], interface)
        )

    # Check every Reference and CollectionField field in every IEntry
    # interface, making sure that they only reference entries that are
    # published in that version.
    for version, interface in REGISTERED_ENTRIES:
        for name, field in interface.namesAndDescriptions():
            referenced_interface, what = _extract_reference_type(field)
            if referenced_interface is not None:
                _assert_interface_registered_for_version(
                    version,
                    referenced_interface,
                    available_registrations,
                    (
                        "%(interface)s.%(field)s is %(what)s"
                        % dict(
                            interface=interface.__name__,
                            field=field.__name__,
                            what=what,
                        )
                    ),
                )

    # For every version, check the return value and arguments to every
    # named operation published in that version, making sure that
    # there are no references to IEntries not published in that
    # version.
    for version, method in REGISTERED_OPERATIONS:
        tags = method.getTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        return_type = tags.get("return_type")
        referenced_interface, what = _extract_reference_type(return_type)
        if referenced_interface is not None:
            _assert_interface_registered_for_version(
                version,
                referenced_interface,
                available_registrations,
                "named operation %s returns %s" % (tags["as"], what),
            )

        if "params" not in tags:
            continue

        for name, field in tags["params"].items():
            referenced_interface, what = _extract_reference_type(field)
            if referenced_interface is not None:
                _assert_interface_registered_for_version(
                    version,
                    referenced_interface,
                    available_registrations,
                    "named operation %s accepts %s" % (tags["as"], what),
                )
    del REGISTERED_OPERATIONS[:]
    del REGISTERED_ENTRIES[:]


def _extract_reference_type(field):
    """Determine what kind of object the given field is a reference to.

    This is a helper method used by the coherence checker.

    :return: A 2-tuple (reference_type, human_readable): If
    `field` is a reference to a scalar entry, human_readable is
    the name of the interface. If `field` is a collection of
    entries, human_readable is the string "a collection of
    [interface name]". If `field` is not a reference to an
    entry, both values are None.
    """
    if IReference.providedBy(field):
        schema = field.schema
        return (schema, schema.__name__)
    elif ICollectionField.providedBy(field):
        schema = field.value_type.schema
        return (schema, "a collection of %s" % schema.__name__)
    else:
        return (None, None)


def _assert_interface_registered_for_version(
    version, interface, available_registrations, error_message_insert
):
    """A helper method for the coherence checker.

    See if the given entry interface is published in the given version
    (as determined by the contents of `available_registrations`), and
    if it's not, raise an exception.

    :param version: The version in which `interface` should be published.
    :param interface: The interface that ought to be published.
    :param available_registrations: A set of (version, interface) pairs
        to check.
    :param error_message_insert: A snippet of text explaining the significance
        if `interface`, eg. "IMyInterface.myfield is IOughtToBePublished" or
        "named operation my_named_operation returns IOughtToBePublished".
    """

    if version is None:
        version = getUtility(IWebServiceConfiguration).active_versions[0]

    to_check = VersionedObject(version, interface)
    if to_check not in available_registrations:
        raise ValueError(
            "In version %(version)s, %(problem)s, but version %(version)s "
            "of the web service does not publish %(reference)s as "
            "an entry. (It may not be published at all.)"
            % dict(
                version=version,
                problem=error_message_insert,
                reference=interface.__name__,
            )
        )


def generate_and_register_webservice_operations(
    context, interface, repository=None
):
    """Create and register adapters for all exported methods.

    Different versions of the web service may publish the same
    operation differently or under different names.
    """
    # First of all, figure out when to stop publishing field mutators
    # as named operations.
    config = getUtility(IWebServiceConfiguration)
    if config.last_version_with_mutator_named_operations is None:
        no_mutator_operations_after = None
        block_mutator_operations_as_of_version = None
    else:
        no_mutator_operations_after = config.active_versions.index(
            config.last_version_with_mutator_named_operations
        )
        if len(config.active_versions) > no_mutator_operations_after + 1:
            block_mutator_operations_as_of_version = config.active_versions[
                no_mutator_operations_after + 1
            ]
        else:
            block_mutator_operations_as_of_version = None
    registered_adapters = set()
    block_mutator_operations = set()

    methods = list(interface.namesAndDescriptions(True))
    for iface in REGISTERED_CONTRIBUTORS[interface]:
        methods.extend(iface.namesAndDescriptions(True))

    for name, method in methods:
        tag = method.queryTaggedValue(LAZR_WEBSERVICE_EXPORTED)
        if tag is None or tag["type"] not in OPERATION_TYPES:
            # This method is not published as a named operation.
            continue

        human_readable_name = interface.__name__ + "." + method.__name__
        if config.require_explicit_versions and tag.stack[0][0] is None:
            # We have annotations for an implicitly defined version, which
            # is prohibited. But don't panic--these might just be the
            # default annotations set by the system. We only need to raise
            # an exception if the method is actually *published*.
            version, annotations = tag.stack[0]
            if annotations.get("type") != REMOVED_OPERATION_TYPE:
                version = config.active_versions[0]
                raise ValueError(
                    (
                        "%s: Implicitly tagged for export to web service "
                        'version "%s", but the service configuration requires '
                        "all version declarations to be explicit. You should "
                        'add @operation_for_version("%s") to the bottom of '
                        "the annotation stack."
                    )
                    % (human_readable_name, version, version)
                )

        # Make sure that this method was annotated with the
        # versions in the right order.
        ensure_correct_version_ordering(human_readable_name, tag.dict_names)

        operation_name = None
        # If an operation's name does not change between version n and
        # version n+1, we want lookups for requests that come in for
        # version n+1 to find the registered adapter for version n. This
        # happens automatically. But if the operation name changes
        # (because the operation is now published under a new name, or
        # because the operation has been removed), we need to register a
        # masking adapter: something that will stop version n+1's lookups
        # from finding the adapter registered for version n. To this end
        # we keep track of what the operation looked like in the previous
        # version.
        previous_operation_name = None
        previous_operation_provides = None
        for version, tag in tag.stack:
            if version is None:
                this_version_index = 0
            else:
                this_version_index = config.active_versions.index(version)

            if tag["type"] == REMOVED_OPERATION_TYPE:
                # This operation is not present in this version.
                # We'll represent this by setting the operation_name
                # to None. If the operation was not present in the
                # previous version either (or there is no previous
                # version), previous_operation_name will also be None
                # and nothing will happen. If the operation was
                # present in the previous version,
                # previous_operation_name will not be None, and the
                # code that handles name changes will install a
                # masking adapter.
                operation_name = None
                operation_provides = None
                factory = None

                # If there are any other tags besides 'type', it means
                # that the developer tried to annotate a method for a
                # version where the method isn't published. Let's warn
                # them about it.
                #
                # (We can't make this check when the annotation
                # happens, because it will reject a method that uses
                # an annotation like @export_operation_as before using
                # an annotation like @export_read_operation. That's a
                # little sloppy, but it's not bad enough to warrant an
                # exception.)
                tag_names = list(tag.keys())
                if tag_names != ["type"]:
                    tag_names.remove("type")
                    raise AssertionError(
                        'Method "%s" contains annotations for version "%s", '
                        "even though it's not published in that version. "
                        'The bad annotations are: "%s".'
                        % (
                            method.__name__,
                            version,
                            '", "'.join(sorted(tag_names)),
                        )
                    )
            else:
                if tag["type"] == "read_operation":
                    operation_provides = IResourceGETOperation
                elif tag["type"] in ["factory", "write_operation"]:
                    operation_provides = IResourcePOSTOperation
                elif tag["type"] in ["destructor"]:
                    operation_provides = IResourceDELETEOperation
                else:
                    # We know it's not REMOVED_OPERATION_TYPE, because
                    # that case is handled above.
                    raise AssertionError(
                        "Unknown operation type: %s" % tag["type"]
                    )

                operation_name = tag.get("as")
                if tag["type"] in ["destructor"]:
                    operation_name = ""

                if tag.get("is_mutator", False) and (
                    no_mutator_operations_after is None
                    or no_mutator_operations_after < this_version_index
                ):
                    # This is a mutator method, and in this version,
                    # mutator methods are not published as named
                    # operations at all. Block any lookup of the named
                    # operation from succeeding.
                    #
                    # This will save us from having to do another
                    # de-registration later.
                    factory = _mask_adapter_registration
                else:
                    factory = generate_operation_adapter(method, version)

            # Operations are looked up by name. If the operation's
            # name has changed from the previous version to this
            # version, or if the operation was removed in this
            # version, we need to block lookups of the previous name
            # from working.
            if (
                operation_name != previous_operation_name
                and previous_operation_name is not None
            ):
                register_adapter_for_version(
                    _mask_adapter_registration,
                    interface,
                    version,
                    previous_operation_provides,
                    previous_operation_name,
                    context.info,
                )
                registered_adapters.add(
                    (
                        previous_operation_name,
                        version,
                        previous_operation_provides,
                    )
                )

            # If the operation exists in this version (ie. its name is
            # not None), register it using this version's name.
            if operation_name is not None:
                register_adapter_for_version(
                    factory,
                    interface,
                    version,
                    operation_provides,
                    operation_name,
                    context.info,
                )
                registered_adapters.add(
                    (operation_name, version, operation_provides)
                )
                if (
                    tag.get("is_mutator")
                    and block_mutator_operations_as_of_version is not None
                ):
                    defined_in = this_version_index
                    blocked_as_of = config.active_versions.index(
                        block_mutator_operations_as_of_version
                    )
                    if defined_in < blocked_as_of:
                        # In this version, this mutator is also a
                        # named operation. But in a later version
                        # mutators stop being named operations, and
                        # the operation registration for this mutator
                        # will need to be blocked.
                        block_mutator_operations.add(
                            (
                                operation_name,
                                block_mutator_operations_as_of_version,
                                operation_provides,
                            )
                        )
                if repository is not None:
                    repository.append(VersionedObject(version, method))
            previous_operation_name = operation_name
            previous_operation_provides = operation_provides

    for operation_key in block_mutator_operations:
        if operation_key not in registered_adapters:
            operation_name, version, operation_provides = operation_key
            # The operation was registered as a mutator, back in the
            # days when mutator operations were also named operations,
            # and it never got de-registered. De-register it now.
            register_adapter_for_version(
                _mask_adapter_registration,
                interface,
                version,
                operation_provides,
                operation_name,
                context.info,
            )


def _mask_adapter_registration(*args):
    """A factory function that stops an adapter lookup from succeeding.

    This function is registered when it's necessary to explicitly stop
    some part of web service version n from being visible to version n+1.
    """
    return None


def register_exception_view(context, exception):
    """
    Register WebServiceExceptionView to handle exception on the webservice.
    """
    context.action(
        discriminator=(
            "view",
            exception,
            "index.html",
            IWebServiceClientRequest,
            IWebServiceClientRequest,
        ),
        callable=handler,
        args=(
            "registerAdapter",
            WebServiceExceptionView,
            (exception, IWebServiceClientRequest),
            Interface,
            "index.html",
            context.info,
        ),
    )
