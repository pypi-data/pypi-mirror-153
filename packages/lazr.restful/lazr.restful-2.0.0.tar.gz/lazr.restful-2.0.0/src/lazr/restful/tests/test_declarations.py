# Copyright 2008-2011 Canonical Ltd.  All rights reserved.

"""Unit tests for the conversion of interfaces into a web service."""

import testtools
from zope.component import (
    adapter,
    getMultiAdapter,
    getSiteManager,
    getUtility,
)
from zope.interface import (
    Attribute,
    implementer,
    Interface,
)
from zope.interface.interfaces import ComponentLookupError
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema import (
    Int,
    TextLine,
)
from zope.security.checker import (
    MultiChecker,
    ProxyFactory,
)
from zope.security.interfaces import Unauthorized
from zope.security.management import (
    endInteraction,
    newInteraction,
)

from lazr.restful.declarations import (
    accessor_for,
    call_with,
    error_status,
    export_read_operation,
    export_write_operation,
    exported,
    exported_as_webservice_entry,
    generate_entry_interfaces,
    generate_operation_adapter,
    LAZR_WEBSERVICE_NAME,
    mutator_for,
    operation_for_version,
    operation_parameters,
    operation_returns_collection_of,
    operation_returns_entry,
)
from lazr.restful.fields import (
    CollectionField,
    Reference,
)
from lazr.restful.interfaces import (
    IEntry,
    IResourceGETOperation,
    IWebServiceConfiguration,
)
from lazr.restful.marshallers import SimpleFieldMarshaller
from lazr.restful.metazcml import (
    AttemptToContributeToNonExportedInterface,
    ConflictInContributingInterfaces,
    contribute_to_interface,
    find_exported_interfaces,
    generate_and_register_webservice_operations,
)
from lazr.restful._resource import (
    EntryAdapterUtility,
    EntryResource,
)
from lazr.restful.testing.webservice import TestCaseWithWebServiceFixtures
from lazr.restful.testing.helpers import register_test_module
from lazr.restful.utils import VersionedObject


class ContributingInterfacesTestCase(TestCaseWithWebServiceFixtures):
    """Tests for interfaces that contribute fields/operations to others."""

    def setUp(self):
        super().setUp()
        sm = getSiteManager()
        sm.registerAdapter(ProductToHasBugsAdapter)
        sm.registerAdapter(ProjectToHasBugsAdapter)
        sm.registerAdapter(ProductToHasBranchesAdapter)
        sm.registerAdapter(StubFieldMarshaller)
        self.one_zero_request = self.fake_request("1.0")
        self.two_zero_request = self.fake_request("2.0")
        self.product = Product()
        self.project = Project()

    def test_attributes(self):
        # The bug_count field comes from IHasBugs (which IProduct does not
        # provide, although it can be adapted into) but that field is
        # available in the webservice (IEntry) adapter for IProduct, and that
        # adapter knows it needs to adapt the product into an IHasBugs to
        # access .bug_count.
        self.product._bug_count = 10
        register_test_module("testmod", IProduct, IHasBugs)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        self.assertEqual(adapter.bug_count, 10)

    def test_operations(self):
        # Although getBugsCount() is not provided by IProduct, it is available
        # on the webservice adapter as IHasBugs contributes it to IProduct.
        self.product._bug_count = 10
        register_test_module("testmod", IProduct, IHasBugs)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request),
            IResourceGETOperation,
            name="getBugsCount",
        )
        self.assertEqual(adapter(), "10")

    def test_accessor_for(self):
        # The accessor_for annotator can be used to mark a method as an
        # accessor for an attribute. This allows methods with bound
        # parameters to be used in place of properties.
        self.product._branches = [Branch("A branch"), Branch("Another branch")]
        register_test_module("testmod", IBranch, IProduct, IHasBranches)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        self.assertEqual(adapter.branches, self.product._branches)

    def test_accessor_for_at_n_included_at_n_plus_1(self):
        # An accessor_for, when defined for version N, will also appear
        # in version N+1.
        self.product._branches = [Branch("A branch"), Branch("Another branch")]
        register_test_module("testmod", IBranch, IProduct, IHasBranches)
        adapter_10 = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        adapter_20 = getMultiAdapter(
            (self.product, self.two_zero_request), IEntry
        )
        self.assertEqual(adapter_10.branches, adapter_20.branches)

    def test_only_one_accessor_for_version(self):
        # There can only be one accessor defined for a given attribute
        # at a given version.
        def declare_too_many_accessors():
            @exported_as_webservice_entry(contributes_to=[IProduct])
            class IHasTooManyAccessors(Interface):
                needs_an_accessor = exported(
                    TextLine(title="This needs an accessor", readonly=True)
                )

                @accessor_for(needs_an_accessor)
                def get_whatever_it_is(self):
                    pass

                @accessor_for(needs_an_accessor)
                def get_whatever_it_is_again(self):
                    pass

        self.assertRaises(TypeError, declare_too_many_accessors)

    def test_accessors_can_be_superseded(self):
        # Separate accessors can be declared for different versions of
        # an interface.
        self.product._bug_target_name = "Bug target name"
        register_test_module("testmod", IProduct, IHasBugs)
        adapter_10 = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        adapter_20 = getMultiAdapter(
            (self.product, self.two_zero_request), IEntry
        )
        self.assertEqual(
            adapter_10.bug_target_name, self.product._bug_target_name
        )
        self.assertEqual(
            adapter_20.bug_target_name,
            self.product._bug_target_name + " version 2.0",
        )

    def test_accessor_and_mutator_together(self):
        # accessor_for and mutator_for can be used together on a field
        # to present a field that can be manipulated as though it's an
        # attribute whilst using local method calls under-the-hood.
        register_test_module("testmod", IProduct, IHasBugs)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        adapter.bug_target_name = "A bug target name!"
        self.assertEqual(
            "A bug target name!", adapter.context._bug_target_name
        )
        self.assertEqual("A bug target name!", adapter.bug_target_name)

    def test_contributing_interface_with_differences_between_versions(self):
        # In the '1.0' version, IHasBranches.development_branches is exported
        # with its original name whereas for the '2.0' version it's exported
        # as 'development_branch_20'.
        self.product._dev_branch = Branch("A product branch")
        register_test_module("testmod", IBranch, IProduct, IHasBranches)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        self.assertEqual(adapter.development_branch, self.product._dev_branch)

        adapter = getMultiAdapter(
            (self.product, self.two_zero_request), IEntry
        )
        self.assertEqual(
            adapter.development_branch_20, self.product._dev_branch
        )

    def test_mutator_for_just_one_version(self):
        # On the '1.0' version, IHasBranches contributes a read only
        # development_branch field, but on version '2.0' that field can be
        # modified as we define a mutator for it.
        self.product._dev_branch = Branch("A product branch")
        register_test_module("testmod", IBranch, IProduct, IHasBranches)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        try:
            adapter.development_branch = None
        except AttributeError:
            pass
        else:
            self.fail(
                "IHasBranches.development_branch should be read-only "
                "on the 1.0 version"
            )

        adapter = getMultiAdapter(
            (self.product, self.two_zero_request), IEntry
        )
        self.assertEqual(
            adapter.development_branch_20, self.product._dev_branch
        )
        adapter.development_branch_20 = None
        self.assertEqual(adapter.development_branch_20, None)

    def test_contributing_to_multiple_interfaces(self):
        # Check that the webservice adapter for both IProduct and IProject
        # have the IHasBugs attributes, as that interface contributes to them.
        self.product._bug_count = 10
        self.project._bug_count = 100
        register_test_module("testmod", IProduct, IProject, IHasBugs)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        self.assertEqual(adapter.bug_count, 10)

        adapter = getMultiAdapter(
            (self.project, self.one_zero_request), IEntry
        )
        self.assertEqual(adapter.bug_count, 100)

    def test_multiple_contributing_interfaces(self):
        # Check that the webservice adapter for IProduct has the attributes
        # from both IHasBugs and IHasBranches.
        self.product._bug_count = 10
        self.product._dev_branch = Branch("A product branch")
        register_test_module(
            "testmod", IBranch, IProduct, IHasBugs, IHasBranches
        )
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        self.assertEqual(adapter.bug_count, 10)
        self.assertEqual(adapter.development_branch, self.product._dev_branch)

    def test_redacted_fields_for_empty_entry(self):
        # An entry which doesn't export any fields/operations will have no
        # redacted fields.
        @exported_as_webservice_entry()
        class IEmpty(Interface):
            pass

        @implementer(IEmpty)
        class Empty:
            pass

        register_test_module("testmod", IEmpty)
        entry_resource = EntryResource(Empty(), self.one_zero_request)
        self.assertEqual({}, entry_resource.entry._orig_interfaces)
        self.assertEqual([], entry_resource.redacted_fields)

    def test_redacted_fields_with_no_permission_checker(self):
        # When looking up an entry's redacted_fields, we take into account the
        # interface where the field is defined and adapt the context to that
        # interface before accessing that field.
        register_test_module(
            "testmod", IBranch, IProduct, IHasBugs, IHasBranches
        )
        entry_resource = EntryResource(self.product, self.one_zero_request)
        self.assertEqual([], entry_resource.redacted_fields)

    def test_redacted_fields_with_permission_checker(self):
        # When looking up an entry's redacted_fields for an object which is
        # security proxied, we use the security checker for the interface
        # where the field is defined.
        register_test_module(
            "testmod", IBranch, IProduct, IHasBugs, IHasBranches
        )
        newInteraction()
        try:
            secure_product = ProxyFactory(
                self.product, checker=MultiChecker([(IProduct, "zope.Public")])
            )
            entry_resource = EntryResource(
                secure_product, self.one_zero_request
            )
            self.assertEqual([], entry_resource.redacted_fields)
        finally:
            endInteraction()

    def test_duplicate_contributed_attributes(self):
        # We do not allow a given attribute to be contributed to a given
        # interface by more than one contributing interface.
        contribute_to_interface(IHasBugs, {})
        self.assertRaises(
            ConflictInContributingInterfaces,
            contribute_to_interface,
            IHasBugs2,
            {},
        )

    def test_contributing_interface_not_exported(self):
        # Contributing interfaces are not exported by themselves -- they only
        # contribute their exported fields/operations to other entries.
        @implementer(IHasBranches)
        class StubHasBranches:
            pass

        stub = StubHasBranches()
        register_test_module("testmod", IBranch, IProduct, IHasBranches)
        self.assertRaises(
            ComponentLookupError,
            getMultiAdapter,
            (stub, self.one_zero_request),
            IEntry,
        )

    def test_cannot_contribute_to_non_exported_interface(self):
        # A contributing interface can only contribute to exported interfaces.
        class INotExported(Interface):
            pass

        @exported_as_webservice_entry(contributes_to=[INotExported])
        class IContributor(Interface):
            title = exported(TextLine(title="The project title"))

        self.assertRaises(
            AttemptToContributeToNonExportedInterface,
            contribute_to_interface,
            IContributor,
            {},
        )

    def test_duplicate_contributed_methods(self):
        # We do not allow a given method to be contributed to a given
        # interface by more than one contributing interface.
        contribute_to_interface(IHasBugs, {})
        self.assertRaises(
            ConflictInContributingInterfaces,
            contribute_to_interface,
            IHasBugs3,
            {},
        )

    def test_ConflictInContributingInterfaces(self):
        # The ConflictInContributingInterfaces exception states what are the
        # contributing interfaces that caused the conflict.
        e = ConflictInContributingInterfaces("foo", [IHasBugs, IHasBugs2])
        expected_msg = (
            "'foo' is exported in more than one contributing "
            "interface: IHasBugs, IHasBugs2"
        )
        self.assertEqual(str(e), expected_msg)

    def test_type_name(self):
        # Even though the generated adapters will contain stuff from various
        # different adapters, its type name is that of the main interface and
        # not one of its contributors.
        register_test_module("testmod", IProduct, IHasBugs)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        self.assertEqual(
            "product", EntryAdapterUtility(adapter.__class__).singular_type
        )

    def test_accessor_for_with_scopes(self):
        # Users with scopes cannot use accessors.
        self.product._branches = [Branch("A branch"), Branch("Another branch")]
        register_test_module("testmod", IBranch, IProduct, IHasBranches)
        config = getUtility(IWebServiceConfiguration)
        config._scopes = ["scope"]
        self.addCleanup(setattr, config, "_scopes", None)
        adapter = getMultiAdapter(
            (self.product, self.one_zero_request), IEntry
        )
        exception = self.assertRaises(
            Unauthorized, getattr, adapter, "branches"
        )
        self.assertEqual(
            "Current authentication only allows calling scoped methods.",
            str(exception),
        )

    def test_mutator_for_with_scopes(self):
        # Users with scopes cannot use mutators.
        self.product._dev_branch = Branch("A product branch")
        register_test_module("testmod", IBranch, IProduct, IHasBranches)
        config = getUtility(IWebServiceConfiguration)
        config._scopes = ["scope"]
        self.addCleanup(setattr, config, "_scopes", None)
        adapter = getMultiAdapter(
            (self.product, self.two_zero_request), IEntry
        )
        exception = self.assertRaises(
            Unauthorized, setattr, adapter, "development_branch_20", None
        )
        self.assertEqual(
            "Current authentication only allows calling scoped methods.",
            str(exception),
        )


class NotExportedException(Exception):
    pass


@error_status(400)
class ExportedExceptionOne(Exception):
    pass


@error_status(400)
class ExportedExceptionTwo(Exception):
    pass


class INotExported(Interface):
    pass


@exported_as_webservice_entry()
class IExported(Interface):
    pass


class TestFindExportedInterfaces(testtools.TestCase):
    """Tests for find_exported_interfaces."""

    def assertExportsNames(self, module, names):
        self.assertEqual(
            sorted(names),
            sorted(
                iface.__name__ for iface in find_exported_interfaces(module)
            ),
        )

    def test_finds_exported_exceptions(self):
        class Module:
            NotExportedException_copy = NotExportedException
            ExportedExceptionOne_copy = ExportedExceptionOne

        self.assertExportsNames(Module, ["ExportedExceptionOne"])

    def test_finds_exported_interfaces(self):
        class Module:
            INotExported_copy = INotExported
            IExported_copy = IExported

        self.assertExportsNames(Module, ["IExported"])

    def test_honours_all(self):
        class Module:
            __all__ = ["ExportedExceptionOne_copy"]
            ExportedExceptionOne_copy = ExportedExceptionOne
            ExportedExceptionTwo_copy = ExportedExceptionTwo

        self.assertExportsNames(Module, ["ExportedExceptionOne"])

    def test_skips_leading_underscore_without_all(self):
        class Module:
            ExportedExceptionOne_copy = ExportedExceptionOne
            _ExportedExceptionTwo_copy = ExportedExceptionTwo

        self.assertExportsNames(Module, ["ExportedExceptionOne"])


@exported_as_webservice_entry()
class IProduct(Interface):
    title = exported(TextLine(title="The product title"))
    # Need to define the three attributes below because we have a test which
    # wraps a Product object with a security proxy and later uses adapters
    # that access _dev_branch, _branches and _bug_count.
    _dev_branch = Attribute("dev branch")
    _bug_count = Attribute("bug count")
    _branches = Attribute("branches")
    _bug_target_name = Attribute("bug_target_name")


@implementer(IProduct)
class Product:
    title = "A product"
    _bug_count = 0
    _dev_branch = None
    _branches = []
    _bug_target_name = None


@exported_as_webservice_entry()
class IProject(Interface):
    title = exported(TextLine(title="The project title"))


@implementer(IProject)
class Project:
    title = "A project"
    _bug_count = 0


@exported_as_webservice_entry(contributes_to=[IProduct, IProject])
class IHasBugs(Interface):
    bug_count = exported(Int(title="Number of bugs"))
    not_exported = TextLine(title="Not exported")
    bug_target_name = exported(
        TextLine(title="The bug target name of this object.", readonly=True)
    )

    @export_read_operation()
    def getBugsCount():
        pass

    @mutator_for(bug_target_name)
    @export_write_operation()
    @call_with(bound_variable="A string")
    @operation_parameters(bound_variable=TextLine(), new_value=TextLine())
    @operation_for_version("1.0")
    def set_bug_target_name(new_value, bound_variable):
        pass

    @accessor_for(bug_target_name)
    @call_with(bound_value="A string")
    @export_read_operation()
    @operation_parameters(bound_value=TextLine())
    @operation_for_version("1.0")
    def get_bug_target_name(bound_value):
        pass

    @accessor_for(bug_target_name)
    @call_with(bound_value="A string")
    @export_read_operation()
    @operation_parameters(bound_value=TextLine())
    @operation_for_version("2.0")
    def get_bug_target_name_20(bound_value):
        pass


@exported_as_webservice_entry(contributes_to=[IProduct])
class IHasBugs2(Interface):
    bug_count = exported(Int(title="Number of bugs"))
    not_exported = TextLine(title="Not exported")


@exported_as_webservice_entry(contributes_to=[IProduct])
class IHasBugs3(Interface):
    not_exported = TextLine(title="Not exported")

    @export_read_operation()
    def getBugsCount():
        pass


@adapter(IProduct)
@implementer(IHasBugs)
class ProductToHasBugsAdapter:
    def __init__(self, context):
        self.context = context
        self.bug_count = context._bug_count

    def getBugsCount(self):
        return self.bug_count

    def get_bug_target_name(self, bound_value):
        return self.context._bug_target_name

    def get_bug_target_name_20(self, bound_value):
        return self.context._bug_target_name + " version 2.0"

    def set_bug_target_name(self, value, bound_variable):
        self.context._bug_target_name = value


@adapter(IProject)
class ProjectToHasBugsAdapter(ProductToHasBugsAdapter):
    pass


@exported_as_webservice_entry()
class IBranch(Interface):
    name = TextLine(title="The branch name")


@implementer(IBranch)
class Branch:
    def __init__(self, name):
        self.name = name


@exported_as_webservice_entry(contributes_to=[IProduct])
class IHasBranches(Interface):
    not_exported = TextLine(title="Not exported")
    development_branch = exported(
        Reference(schema=IBranch, readonly=True),
        ("2.0", dict(exported_as="development_branch_20")),
        ("1.0", dict(exported_as="development_branch")),
    )
    branches = exported(
        CollectionField(value_type=Reference(schema=IBranch, readonly=True))
    )

    @mutator_for(development_branch)
    @export_write_operation()
    @operation_parameters(value=TextLine())
    @operation_for_version("2.0")
    def set_dev_branch(value):
        pass

    @accessor_for(branches)
    @call_with(value="A string")
    @export_read_operation()
    @operation_parameters(value=TextLine())
    def get_branches(value):
        pass


@adapter(IProduct)
@implementer(IHasBranches)
class ProductToHasBranchesAdapter:
    def __init__(self, context):
        self.context = context

    @property
    def development_branch(self):
        return self.context._dev_branch

    def set_dev_branch(self, value):
        self.context._dev_branch = value

    def get_branches(self, value):
        return self.context._branches


# One of our tests will try to unmarshall some entries, but even though we
# don't care about the unmarshalling itself, we need to register a generic
# marshaller so that the adapter lookup doesn't fail and cause an error on the
# test.
@adapter(Interface, IHTTPRequest)
class StubFieldMarshaller(SimpleFieldMarshaller):
    pass


# Classes for TestEntryMultiversion.


@exported_as_webservice_entry(as_of="2.0")
class INotInitiallyExported(Interface):
    # An entry that's not exported in the first version of the web
    # service.
    pass


@exported_as_webservice_entry(
    versioned_annotations=[("2.0", dict(exported=False))]
)
class INotPresentInLaterVersion(Interface):
    # An entry that's only exported in the first version of the web
    # service.
    pass


@exported_as_webservice_entry(
    singular_name="octopus",
    plural_name="octopi",
    versioned_annotations=[
        ("2.0", dict(singular_name="fish", plural_name="fishes"))
    ],
)
class IHasDifferentNamesInDifferentVersions(Interface):
    # An entry that has different names in different versions.
    pass


@exported_as_webservice_entry(
    singular_name="frog",
    versioned_annotations=[("2.0", dict(singular_name="toad"))],
)
class IHasDifferentSingularNamesInDifferentVersions(Interface):
    # An entry that has different names in different versions.
    pass


class TestEntryMultiversion(TestCaseWithWebServiceFixtures):
    """Test the ability to export an entry only in certain versions."""

    def test_not_initially_exported(self):
        # INotInitiallyExported is published in version 2.0 but not in 1.0.
        interfaces = generate_entry_interfaces(
            INotInitiallyExported,
            [],
            *getUtility(IWebServiceConfiguration).active_versions,
        )
        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].version, "2.0")

    def test_not_exported_in_later_version(self):
        # INotPresentInLaterVersion is published in version 1.0 but
        # not in 2.0.
        interfaces = generate_entry_interfaces(
            INotPresentInLaterVersion,
            [],
            *getUtility(IWebServiceConfiguration).active_versions,
        )
        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].version, "1.0")

    def test_different_names_in_different_versions(self):
        # IHasDifferentNamesInDifferentVersions is called
        # octopus/octopi in 1.0, and fish/fishes in 2.0.
        interfaces = generate_entry_interfaces(
            IHasDifferentNamesInDifferentVersions,
            [],
            *getUtility(IWebServiceConfiguration).active_versions,
        )
        interface_10 = interfaces[0].object
        tags_10 = interface_10.getTaggedValue(LAZR_WEBSERVICE_NAME)
        self.assertEqual("octopus", tags_10["singular"])
        self.assertEqual("octopi", tags_10["plural"])

        interface_20 = interfaces[1].object
        tags_20 = interface_20.getTaggedValue(LAZR_WEBSERVICE_NAME)
        self.assertEqual("fish", tags_20["singular"])
        self.assertEqual("fishes", tags_20["plural"])

    def test_nonexistent_annotation_fails(self):
        # You can't define an entry class that includes an unrecognized
        # annotation in its versioned_annotations.
        try:

            @exported_as_webservice_entry(
                versioned_annotations=[("2.0", dict(no_such_annotation=True))]
            )
            class IUsesNonexistentAnnotation(Interface):
                pass

            self.fail("Expected ValueError.")
        except ValueError as exception:
            self.assertEqual(
                str(exception),
                'Unrecognized annotation for version "2.0": '
                '"no_such_annotation"',
            )

    def test_changing_singular_also_changes_plural(self):
        # IHasDifferentSingularNamesInDifferentVersions defines the
        # singular name 'frog' in 1.0, and 'toad' in 2.0. This test
        # makes sure that the plural of 'toad' is not 'frogs'.
        interfaces = generate_entry_interfaces(
            IHasDifferentSingularNamesInDifferentVersions,
            [],
            *getUtility(IWebServiceConfiguration).active_versions,
        )
        interface_10 = interfaces[0].object
        tags_10 = interface_10.getTaggedValue(LAZR_WEBSERVICE_NAME)
        self.assertEqual("frog", tags_10["singular"])
        self.assertEqual("frogs", tags_10["plural"])

        interface_20 = interfaces[1].object
        tags_20 = interface_20.getTaggedValue(LAZR_WEBSERVICE_NAME)
        self.assertEqual("toad", tags_20["singular"])
        self.assertEqual("toads", tags_20["plural"])


# Classes for TestReqireExplicitVersions


@exported_as_webservice_entry()
class IEntryExportedWithoutAsOf(Interface):
    pass


@exported_as_webservice_entry(as_of="1.0")
class IEntryExportedWithAsOf(Interface):
    pass


@exported_as_webservice_entry(as_of="2.0")
class IEntryExportedAsOfLaterVersion(Interface):
    pass


@exported_as_webservice_entry(as_of="1.0")
class IFieldExportedWithoutAsOf(Interface):
    field = exported(TextLine(), exported=True)


@exported_as_webservice_entry(as_of="1.0")
class IFieldExportedToEarliestVersionUsingAsOf(Interface):
    field = exported(TextLine(), as_of="1.0")


@exported_as_webservice_entry(as_of="1.0")
class IFieldExportedToLatestVersionUsingAsOf(Interface):
    field = exported(TextLine(), as_of="2.0")


@exported_as_webservice_entry(as_of="1.0")
class IFieldDefiningAttributesBeforeAsOf(Interface):
    field = exported(TextLine(), ("1.0", dict(exported=True)), as_of="2.0")


@exported_as_webservice_entry(as_of="1.0")
class IFieldAsOfNonexistentVersion(Interface):
    field = exported(TextLine(), as_of="nosuchversion")


@exported_as_webservice_entry(as_of="1.0")
class IFieldDoubleDefinition(Interface):
    field = exported(
        TextLine(),
        ("2.0", dict(exported_as="name2")),
        exported_as="name2",
        as_of="2.0",
    )


@exported_as_webservice_entry(as_of="1.0")
class IFieldImplicitOperationDefinition(Interface):
    @call_with(value="2.0")
    @operation_for_version("2.0")
    @call_with(value="1.0")
    @export_read_operation()
    def implicitly_in_10(value):
        pass


@exported_as_webservice_entry(as_of="1.0")
class IFieldExplicitOperationDefinition(Interface):
    @call_with(value="2.0")
    @operation_for_version("2.0")
    @call_with(value="1.0")
    @export_read_operation()
    @operation_for_version("1.0")
    def explicitly_in_10(value):
        pass


@implementer(IFieldExplicitOperationDefinition)
class FieldExplicitOperationDefinition:
    pass


class TestRequireExplicitVersions(TestCaseWithWebServiceFixtures):
    """Test behavior when require_explicit_versions is True."""

    def setUp(self):
        super().setUp()
        self.utility = getUtility(IWebServiceConfiguration)
        self.utility.require_explicit_versions = True

    def test_entry_exported_with_as_of_succeeds(self):
        # An entry exported using as_of is present in the as_of_version
        # and in subsequent versions.
        interfaces = generate_entry_interfaces(
            IEntryExportedWithAsOf, [], *self.utility.active_versions
        )
        self.assertEqual(len(interfaces), 2)
        self.assertEqual(interfaces[0].version, "1.0")
        self.assertEqual(interfaces[1].version, "2.0")

    def test_entry_exported_as_of_later_version_succeeds(self):
        # An entry exported as_of a later version is not present in
        # earlier versions.
        interfaces = generate_entry_interfaces(
            IEntryExportedAsOfLaterVersion, [], *self.utility.active_versions
        )
        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].version, "2.0")

    def test_entry_exported_without_as_of_fails(self):
        exception = self.assertRaises(
            ValueError,
            generate_entry_interfaces,
            IEntryExportedWithoutAsOf,
            [],
            *self.utility.active_versions,
        )
        self.assertEqual(
            str(exception),
            'Entry "IEntryExportedWithoutAsOf": Exported in version 1.0, '
            "but not by using as_of. The service configuration requires "
            "that you use as_of.",
        )

    def test_field_exported_as_of_earlier_version_is_exported_in_subsequent_versions(  # noqa: E501
        self,
    ):  # noqa: E501
        # If you export a field as_of version 1.0, it's present in
        # 1.0's version of the entry and in all subsequent versions.
        interfaces = generate_entry_interfaces(
            IFieldExportedToEarliestVersionUsingAsOf,
            [],
            *self.utility.active_versions,
        )
        interface_10 = interfaces[0].object
        interface_20 = interfaces[1].object
        self.assertEqual(list(interface_10.names()), ["field"])
        self.assertEqual(list(interface_20.names()), ["field"])

    def test_field_exported_as_of_later_version_is_not_exported_in_earlier_versions(  # noqa: E501
        self,
    ):  # noqa: E501
        # If you export a field as_of version 2.0, it's not present in
        # 1.0's version of the entry.
        interfaces = generate_entry_interfaces(
            IFieldExportedToLatestVersionUsingAsOf,
            [],
            *self.utility.active_versions,
        )
        interface_10 = interfaces[0].object
        interface_20 = interfaces[1].object
        self.assertEqual(list(interface_10.names()), [])
        self.assertEqual(list(interface_20.names()), ["field"])

    def test_field_not_exported_using_as_of_fails(self):
        # If you export a field without specifying as_of, you get an
        # error.
        exception = self.assertRaises(
            ValueError,
            generate_entry_interfaces,
            IFieldExportedWithoutAsOf,
            [],
            *self.utility.active_versions,
        )
        self.assertEqual(
            str(exception),
            (
                'Field "field" in interface "IFieldExportedWithoutAsOf": '
                "Exported in version 1.0, but not by using as_of. "
                "The service configuration requires that you use as_of."
            ),
        )

    def test_field_cannot_be_both_exported_and_not_exported(self):
        # If you use the as_of keyword argument, you can't also set
        # the exported keyword argument to False.
        exception = self.assertRaises(
            ValueError, exported, TextLine(), as_of="1.0", exported=False
        )
        self.assertEqual(
            str(exception),
            (
                "as_of=1.0 says to export TextLine, but exported=False "
                "says not to."
            ),
        )

    def test_field_exported_as_of_nonexistent_version_fails(self):
        # You can't export a field as_of a nonexistent version.
        exception = self.assertRaises(
            ValueError,
            generate_entry_interfaces,
            IFieldAsOfNonexistentVersion,
            [],
            *self.utility.active_versions,
        )
        self.assertEqual(
            str(exception),
            (
                'Field "field" in interface "IFieldAsOfNonexistentVersion": '
                'Unrecognized version "nosuchversion".'
            ),
        )

    def test_field_exported_with_duplicate_attributes_fails(self):
        # You can't provide a dictionary of attributes for the
        # version specified in as_of.
        exception = self.assertRaises(
            ValueError,
            generate_entry_interfaces,
            IFieldDoubleDefinition,
            [],
            *self.utility.active_versions,
        )
        self.assertEqual(
            str(exception),
            (
                'Field "field" in interface "IFieldDoubleDefinition": '
                'Duplicate definitions for version "2.0".'
            ),
        )

    def test_field_with_annotations_that_precede_as_of_fails(self):
        # You can't provide a dictionary of attributes for a version
        # preceding the version specified in as_of.
        exception = self.assertRaises(
            ValueError,
            generate_entry_interfaces,
            IFieldDefiningAttributesBeforeAsOf,
            [],
            *self.utility.active_versions,
        )
        self.assertEqual(
            str(exception),
            (
                'Field "field" in interface '
                '"IFieldDefiningAttributesBeforeAsOf": Version "1.0" defined '
                'after the later version "2.0".'
            ),
        )

    def test_generate_operation_adapter_for_none_fails(self):
        # You can't pass None as the version to
        # generate_operation_adapter(). This doesn't happen in normal
        # usage because the metazcml will always pass in a real
        # version number, but we test it just to make sure it'll catch
        # the problem.
        method = [
            method
            for name, method in IFieldImplicitOperationDefinition.namesAndDescriptions()  # noqa: E501
            if name == "implicitly_in_10"
        ][0]
        exception = self.assertRaises(
            ValueError, generate_operation_adapter, method, None
        )
        self.assertEqual(
            str(exception),
            '"implicitly_in_10" is implicitly tagged for export to web '
            'service version "1.0", but the service configuration requires '
            "all version declarations to be explicit. You should add "
            '@operation_for_version("1.0") to the bottom of the '
            "annotation stack.",
        )

    def test_operation_implicitly_exported_in_earliest_version_fails(self):
        # You can't implicitly define an operation for the earliest version.
        exception = self.assertRaises(
            ValueError,
            generate_and_register_webservice_operations,
            None,
            IFieldImplicitOperationDefinition,
            [],
        )
        self.assertEqual(
            str(exception),
            (
                "IFieldImplicitOperationDefinition.implicitly_in_10: "
                'Implicitly tagged for export to web service version "1.0", '
                "but the service configuration requires all version "
                "declarations to be explicit. You should add "
                '@operation_for_version("1.0") to the bottom of the '
                "annotation stack."
            ),
        )

    def test_operation_explicitly_exported_in_earliest_version_succeeds(self):
        # You can explicitly define an operation for the earliest version.

        # Unlike the previous test, we can't just call
        # generate_and_register_webservice_operations: we need to have
        # a ZCML context.
        register_test_module("testmod", IFieldExplicitOperationDefinition)
        context = FieldExplicitOperationDefinition()
        adapter = getMultiAdapter(
            (context, self.fake_request("1.0")),
            IResourceGETOperation,
            name="explicitly_in_10",
        )
        self.assertEqual(
            adapter.__class__.__name__,
            "GET_IFieldExplicitOperationDefinition_explicitly_in_10_1_0",
        )


# Classes for TestCoherenceChecking


class INotPublished(Interface):
    pass


@exported_as_webservice_entry()
class IReferencesNotPublished(Interface):
    field = exported(Reference(schema=INotPublished))


@exported_as_webservice_entry()
class IReferencesCollectionOfNotPublished(Interface):
    field = exported(
        CollectionField(value_type=Reference(schema=INotPublished))
    )


@exported_as_webservice_entry()
class IOperationReturnsNotPublished(Interface):
    @operation_returns_entry(INotPublished)
    @export_read_operation()
    def get_impossible_object():
        pass


@exported_as_webservice_entry()
class IOperationReturnsNotPublishedCollection(Interface):
    @operation_returns_collection_of(INotPublished)
    @export_read_operation()
    def get_impossible_objects():
        pass


@exported_as_webservice_entry()
class IOperationAcceptsNotPublished(Interface):
    @operation_parameters(arg=Reference(schema=INotPublished))
    @export_write_operation()
    def use_impossible_object(arg):
        pass


@exported_as_webservice_entry()
class IOperationAcceptsCollectionOfNotPublished(Interface):
    @operation_parameters(
        arg=CollectionField(value_type=Reference(schema=INotPublished))
    )
    @export_write_operation()
    def use_impossible_objects(arg):
        pass


@exported_as_webservice_entry(as_of="2.0")
class IPublishedTooLate(Interface):
    pass


@exported_as_webservice_entry(as_of="1.0")
class IReferencesPublishedTooLate(Interface):
    field = exported(Reference(schema=IPublishedTooLate))


@exported_as_webservice_entry(as_of="1.0")
class IPublishedEarly(Interface):
    pass


@exported_as_webservice_entry(as_of="2.0")
class IPublishedLate(Interface):
    field = exported(Reference(schema=IPublishedEarly))


@exported_as_webservice_entry(
    as_of="1.0",
    versioned_annotations=[VersionedObject("2.0", dict(exported=False))],
)
class IPublishedAndThenRemoved(Interface):
    pass


@exported_as_webservice_entry(as_of="1.0")
class IReferencesPublishedAndThenRemoved(Interface):
    field = exported(Reference(schema=IPublishedAndThenRemoved))


class TestCoherenceChecking(TestCaseWithWebServiceFixtures):
    """
    Test lazr.restful's coherence checking upon web service registration.
    """

    def _test_fails_coherence_check(
        self,
        expect_failure_in_version,
        expect_failure_for_reason,
        expect_failure_due_to_interface,
        *classes
    ):
        """Verify that the given interfaces can't become a web service.

        The given set of interfaces are expected to fail the coherence
        check because they include an annotation that makes some
        version of the web service reference an entry not defined in
        that version (or at all).

        :param expect_failure_in_version: Which version of the web
           service will fail the coherence check.
        :param expect_failure_for_reason: The reason that will be given
           for failing the coherence check.
        :param expect_failure_due_to_interface: The interface that will
           cause the failure due to not being published in
           `expect_failure_in_version`.
        :param classes: The interfaces to attempt to publish as a web
            service. `expect_failure_due_to_interface` will be added to
            this list, so there's no need to specify it again.
        """
        exception = self.assertRaises(
            ValueError,
            register_test_module,
            "testmod",
            *(list(classes) + [expect_failure_due_to_interface]),
        )
        expected_message = (
            "In version %(version)s, %(reason)s, but version %(version)s "
            "of the web service does not publish %(interface)s as an entry. "
            "(It may not be published at all.)"
            % dict(
                version=expect_failure_in_version,
                reason=expect_failure_for_reason,
                interface=expect_failure_due_to_interface.__name__,
            )
        )
        self.assertEqual(str(exception), expected_message)

    def test_reference_to_unpublished_object_fails(self):
        self._test_fails_coherence_check(
            "1.0",
            ("IReferencesNotPublishedEntry_1_0.field is INotPublished"),
            INotPublished,
            IReferencesNotPublished,
        )

    def test_reference_to_object_published_later_fails(self):
        self._test_fails_coherence_check(
            "1.0",
            (
                "IReferencesPublishedTooLateEntry_1_0.field is "
                "IPublishedTooLate"
            ),
            IPublishedTooLate,
            IReferencesPublishedTooLate,
        )

    def test_reference_to_object_published_and_then_removed_fails(self):
        # This setup is acceptable in version 1.0, but in version 2.0
        # IPublishedAndThenRemoved is gone. This puts
        # IReferencesPublishedAndThenRemoved in violation of the
        # coherence check in 2.0, even though it hasn't changed since 1.0.
        self._test_fails_coherence_check(
            "2.0",
            (
                "IReferencesPublishedAndThenRemovedEntry_2_0.field is "
                "IPublishedAndThenRemoved"
            ),
            IPublishedAndThenRemoved,
            IReferencesPublishedAndThenRemoved,
        )

    def test_reference_to_object_published_earlier_succeeds(self):
        # It's okay for an object defined in 2.0 to reference an
        # object first defined in 1.0, so long as the referenced
        # object is also present in 2.0.

        # We'll call this test a success if it doesn't raise an exception.
        register_test_module("testmod", IPublishedEarly, IPublishedLate)

    # At this point we've tested all the ways entries might not be
    # published in a given version: they might never be published,
    # they might be published later, or they might be published
    # earlier and then removed.

    # Now we need to test all the places an unpublished entry might
    # show up, not counting 'as the referent of a Reference field',
    # which we've already tested.

    def test_reference_to_collection_of_unpublished_objects_fails(self):
        # An entry may define a field that's a scoped collection of
        # unpublished entries.
        self._test_fails_coherence_check(
            "1.0",
            (
                "IReferencesCollectionOfNotPublishedEntry_1_0.field is a "
                "collection of INotPublished"
            ),
            INotPublished,
            IReferencesCollectionOfNotPublished,
        )

    def test_operation_returning_unpublished_object_fails(self):
        # An operation may return an unpublished entry.
        self._test_fails_coherence_check(
            "1.0",
            ("named operation get_impossible_object returns INotPublished"),
            INotPublished,
            IOperationReturnsNotPublished,
        )

    def test_operation_returning_collection_of_unpublished_object_fails(self):
        # An operation may return a collection of unpublished entries.
        self._test_fails_coherence_check(
            "1.0",
            (
                "named operation get_impossible_objects returns a collection "
                "of INotPublished"
            ),
            INotPublished,
            IOperationReturnsNotPublishedCollection,
        )

    def test_operation_taking_unpublished_argument_fails(self):
        # An operation may take an unpublished entry as an argument.
        self._test_fails_coherence_check(
            "1.0",
            ("named operation use_impossible_object accepts INotPublished"),
            INotPublished,
            IOperationAcceptsNotPublished,
        )

    def test_operation_taking_unpublished_collection_argument_fails(self):
        # An operation may take a collection of unpublished entries as
        # an argument.
        self._test_fails_coherence_check(
            "1.0",
            (
                "named operation use_impossible_objects accepts a collection "
                "of INotPublished"
            ),
            INotPublished,
            IOperationAcceptsCollectionOfNotPublished,
        )
