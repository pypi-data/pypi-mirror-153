# Copyright 2010 Canonical Ltd.  All rights reserved.

"""Test for lazr.restful.utils."""

import random
import testtools
import unittest

from zope.publisher.browser import TestRequest
from zope.security.management import (
    endInteraction,
    newInteraction,
    queryInteraction,
)

from lazr.restful.utils import (
    extract_write_portion,
    get_current_browser_request,
    is_total_size_link_active,
    parse_accept_style_header,
    sorted_named_things,
    VersionedDict,
)


class TestUtils(unittest.TestCase):
    def test_two_part_extract_write_portion(self):
        # ETags are sometimes two-part.  A hyphen seperates the parts if so.
        self.assertEqual("write", extract_write_portion("read-write"))

    def test_one_part_extract_write_portion(self):
        # ETags are sometimes one-part.  If so, writes are predicated on the
        # whole ETag.
        self.assertEqual("etag", extract_write_portion("etag"))

    def test_get_current_browser_request_no_interaction(self):
        # When there's no interaction setup, get_current_browser_request()
        # returns None.
        self.assertEqual(None, queryInteraction())
        self.assertEqual(None, get_current_browser_request())

    def test_get_current_browser_request(self):
        # When there is an interaction, it returns the interaction's request.
        request = TestRequest()
        newInteraction(request)
        self.assertEqual(request, get_current_browser_request())
        endInteraction()

    def test_is_total_size_link_active(self):
        # Parts of the code want to know if the sizes of collections should be
        # reported in an attribute or via a link back to the service.  The
        # is_total_size_link_active function takes the version of the API in
        # question and a web service configuration object and returns a
        # boolean that is true if a link should be used, false otherwise.

        # Here's the fake web service config we'll be using.
        class FakeConfig:
            active_versions = ["1.0", "2.0", "3.0"]
            first_version_with_total_size_link = "2.0"

        # First, if the version is lower than the threshold for using links,
        # the result is false (i.e., links should not be used).
        self.assertEqual(is_total_size_link_active("1.0", FakeConfig), False)

        # However, if the requested version is equal to, or higher than the
        # threshold, the result is true (i.e., links should be used).
        self.assertEqual(is_total_size_link_active("2.0", FakeConfig), True)
        self.assertEqual(is_total_size_link_active("3.0", FakeConfig), True)

    def test_name_sorter(self):
        # The WADL generation often sorts classes or functions by name; the
        # sorted_named_things helper... helps.

        # First we need some named things to sort.
        class Thing:
            pass

        def make_named_thing():
            thing = Thing()
            thing.__name__ = random.choice("abcdefghijk")
            return thing

        # The function sorts on the object's __name__ attribute, which
        # functions and classes have, see:
        assert hasattr(Thing, "__name__")
        assert hasattr(make_named_thing, "__name__")

        # Now we can make a bunch of things with randomly ordered names and
        # show that sorting them does order them by name.
        things = sorted_named_things(make_named_thing() for i in range(10))
        names = [thing.__name__ for thing in things]
        self.assertEqual(names, sorted(names))

    # For the sake of convenience, test_get_current_web_service_request()
    # and tag_request_with_version_name() are tested in test_webservice.py.


class TestVersionedDict(testtools.TestCase):
    def setUp(self):
        super().setUp()
        self.dict = VersionedDict()

    def test_rename_version_works(self):
        # rename_version works when the given version exists.
        self.dict.push("original")
        self.dict.rename_version("original", "renamed")
        self.assertEqual(self.dict.dict_names, ["renamed"])

    def test_rename_version_fails_given_nonexistent_version(self):
        # rename_version gives KeyError when the given version does
        # not exist.
        self.dict.push("original")
        self.assertRaises(
            KeyError, self.dict.rename_version, "not present", "renamed"
        )

    def test_dict_for_name_finds_dict_with_given_name(self):
        # dict_for_name finds a dict with the given name in the stack.
        self.dict.push("name1")
        self.dict["key"] = "value1"
        self.assertEqual(self.dict.dict_for_name("name1"), dict(key="value1"))

    def test_dict_for_name_finds_first_dict(self):
        # If there's more than one dict with a given name,
        # dict_for_name() finds the first one.
        self.dict.push("name1")
        self.dict["key"] = "value1"
        self.dict.push("name2")
        self.dict.push("name1")
        self.dict["key"] = "value2"
        self.assertEqual(self.dict.dict_for_name("name1"), dict(key="value1"))

    def test_dict_for_name_returns_None_if_no_such_name(self):
        # If there's no dict with the given name, dict_for_name
        # returns None.
        self.assertEqual(None, self.dict.dict_for_name("name1"))

    def test_dict_for_name_returns_default_if_no_such_name(self):
        # If there's no dict with the given name, and a default value
        # is provided, dict_for_name returns the default.
        obj = object()
        self.assertEqual(obj, self.dict.dict_for_name("name1", obj))

    def test_normalize_for_versions_fills_in_blanks(self):
        # `normalize_for_versions` makes sure a VersionedDict has
        # an entry for every one of the given versions.
        self.dict.push("name2")
        self.dict["key"] = "value"
        self.dict.normalize_for_versions(["name1", "name2", "name3"])
        self.assertEqual(
            self.dict.stack,
            [
                ("name1", dict()),
                ("name2", dict(key="value")),
                ("name3", dict(key="value")),
            ],
        )

    def test_normalize_for_versions_uses_default_dict(self):
        self.dict.push("name2")
        self.dict["key"] = "value"
        self.dict.normalize_for_versions(
            ["name1", "name2"], dict(default=True)
        )
        self.assertEqual(
            self.dict.stack,
            [("name1", dict(default=True)), ("name2", dict(key="value"))],
        )

    def test_normalize_for_versions_rejects_nonexistant_versions(self):
        self.dict.push("nosuchversion")
        exception = self.assertRaises(
            ValueError, self.dict.normalize_for_versions, ["name1"]
        )
        self.assertEqual(
            str(exception), 'Unrecognized version "nosuchversion".'
        )

    def test_normalize_for_versions_rejects_duplicate_versions(self):
        self.dict.push("name1")
        self.dict.push("name1")
        exception = self.assertRaises(
            ValueError, self.dict.normalize_for_versions, ["name1", "name2"]
        )
        self.assertEqual(
            str(exception), 'Duplicate definitions for version "name1".'
        )

    def test_normalize_for_versions_rejects_misordered_versions(self):
        self.dict.push("name2")
        self.dict.push("name1")
        exception = self.assertRaises(
            ValueError, self.dict.normalize_for_versions, ["name1", "name2"]
        )
        self.assertEqual(
            str(exception),
            'Version "name1" defined after the later version "name2".',
        )

    def test_error_prefix_prepended_to_exception(self):
        self.dict.push("nosuchversion")
        exception = self.assertRaises(
            ValueError,
            self.dict.normalize_for_versions,
            ["name1"],
            error_prefix="Error test: ",
        )
        self.assertEqual(
            str(exception), 'Error test: Unrecognized version "nosuchversion".'
        )


class TestParseAcceptStyleHeader(unittest.TestCase):
    def test_single_value(self):
        self.assertEqual(parse_accept_style_header("foo"), ["foo"])

    def test_multiple_unodered_values(self):
        self.assertEqual(parse_accept_style_header("foo, bar"), ["foo", "bar"])

        self.assertEqual(
            parse_accept_style_header("foo, bar,baz"), ["foo", "bar", "baz"]
        )

    def test_highest_quality_parameter_wins(self):
        self.assertEqual(
            parse_accept_style_header("foo;q=0.001, bar;q=0.05, baz;q=0.1"),
            ["baz", "bar", "foo"],
        )

    def test_quality_zero_is_omitted(self):
        self.assertEqual(
            parse_accept_style_header("foo;q=0, bar;q=0.5"), ["bar"]
        )

    def test_duplicate_values_are_collapsed(self):
        self.assertEqual(
            parse_accept_style_header("foo;q=0.1, foo;q=0.5, bar;q=0.3"),
            ["foo", "bar"],
        )

    def test_no_quality_parameter_is_implicit_one_point_zero(self):
        self.assertEqual(
            parse_accept_style_header("foo;q=0.5, bar"), ["bar", "foo"]
        )

    def test_standalone_parameter_is_untouched(self):
        self.assertEqual(parse_accept_style_header("foo;a=0.5"), ["foo;a=0.5"])

    def test_quality_parameter_is_removed_next_parameter_is_untouched(self):
        self.assertEqual(
            parse_accept_style_header("foo;a=bar;q=0.5"), ["foo;a=bar"]
        )

    def test_quality_parameter_is_removed_earlier_parameter_is_untouched(self):
        self.assertEqual(
            parse_accept_style_header("foo;q=0.5;a=bar"), ["foo;a=bar"]
        )

    def test_quality_parameter_is_removed_surrounding_parameters_are_untouched(
        self,
    ):
        self.assertEqual(
            parse_accept_style_header("foo;a=bar;q=0.5;b=baz"),
            ["foo;a=bar;b=baz"],
        )
