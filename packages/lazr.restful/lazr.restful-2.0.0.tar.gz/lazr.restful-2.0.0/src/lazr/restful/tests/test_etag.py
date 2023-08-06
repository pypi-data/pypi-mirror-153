# Copyright 2008 Canonical Ltd.  All rights reserved.
"""Tests for ETag generation."""

from collections import OrderedDict
from datetime import (
    date,
    datetime,
)
import os.path
import unittest

from pkg_resources import resource_filename
import pytz
from van.testing.layer import zcml_layer
from zope.component import provideUtility

from lazr.restful.interfaces import IWebServiceConfiguration
from lazr.restful.testing.helpers import TestWebServiceConfiguration
from lazr.restful.testing.webservice import create_web_service_request
from lazr.restful._resource import (
    EntryFieldResource,
    HTTPResource,
    ServiceRootResource,
    make_entry_etag_cores,
)


class FunctionalLayer:
    allow_teardown = False
    zcml = os.path.abspath(resource_filename("lazr.restful", "ftesting.zcml"))


zcml_layer(FunctionalLayer)


class TestEntryResourceETags(unittest.TestCase):
    # The EntryResource uses the field values that can be written or might
    # othwerise change as the basis for its ETags.  The make_entry_etag_cores
    # function is passed the data about the fields and returns the read and
    # write cores.

    layer = FunctionalLayer

    def test_no_field_details(self):
        # If make_entry_etag_cores is given no field details (because no
        # fields exist), the resulting cores empty strings.
        self.assertEqual(make_entry_etag_cores([]), [b"", b""])

    def test_writable_fields(self):
        # If there are writable fields, their values are incorporated into the
        # writable portion of the cores.
        field_details = [
            ("first_field", {"writable": True, "value": "first"}),
            ("second_field", {"writable": True, "value": "second"}),
        ]
        self.assertEqual(
            make_entry_etag_cores(field_details), [b"", b"first\0second"]
        )

    def test_unchanging_fields(self):
        # If there are fields that are not writable their values are still
        # reflected in the generated cores because we want and addition or
        # removal of read-only fields to trigger a new ETag.
        field_details = [
            ("first_field", {"writable": False, "value": "the value"}),
        ]
        self.assertEqual(
            make_entry_etag_cores(field_details), [b"the value", b""]
        )

    def test_combinations_of_fields(self):
        # If there are a combination of writable, changable, and unchanable
        # fields, their values are reflected in the resulting cores.
        field_details = [
            ("first_writable", {"writable": True, "value": "first-writable"}),
            (
                "second_writable",
                {"writable": True, "value": "second-writable"},
            ),
            (
                "first_non_writable",
                {"writable": False, "value": "first-not-writable"},
            ),
            (
                "second_non_writable",
                {"writable": False, "value": "second-not-writable"},
            ),
        ]
        self.assertEqual(
            make_entry_etag_cores(field_details),
            [
                b"first-not-writable\x00second-not-writable",
                b"first-writable\x00second-writable",
            ],
        )

    def test_collection_fields(self):
        # Field values that are something other than text or bytes are
        # encoded using JSON.
        field_details = [
            ("list_field", {"writable": False, "value": ["first", "second"]}),
            (
                "dict_field",
                {
                    "writable": False,
                    "value": OrderedDict(
                        (("first", "one"), ("second", "two"))
                    ),
                },
            ),
            ("date_field", {"writable": False, "value": date(2009, 7, 7)}),
            (
                "datetime_field",
                {
                    "writable": False,
                    "value": datetime(2009, 7, 7, 13, 45, 0, tzinfo=pytz.utc),
                },
            ),
        ]
        self.assertEqual(
            make_entry_etag_cores(field_details),
            [
                b'["first", "second"]\x00{"first": "one", "second": "two"}\x00'
                b'"2009-07-07"\x00"2009-07-07T13:45:00+00:00"',
                b"",
            ],
        )


class TestHTTPResourceETags(unittest.TestCase):
    def test_getETag_is_a_noop(self):
        # The HTTPResource class implements a do-nothing _getETagCores in
        # order to be conservative (because it's not aware of the nature of
        # all possible subclasses).
        self.assertEqual(HTTPResource(None, None)._getETagCores(), None)


class FauxEntryField:
    entry = None
    name = "field_name"
    field = None


class EntryFieldResourceTests(unittest.TestCase):
    # Tests for ETags of EntryFieldResource objects.

    # Because the ETag generation only takes into account the field value and
    # the web service revision number (and not whether the field is read-write
    # or read-only) these tests don't mention the read-write/read-only nature
    # of the field in question.

    def setUp(self):
        self.config = TestWebServiceConfiguration()
        provideUtility(self.config, IWebServiceConfiguration)
        self.resource = EntryFieldResource(FauxEntryField(), None)

    def set_field_value(self, value):
        """
        Set the value of the fake field the EntryFieldResource references.
        """
        self.resource._unmarshalled_field_cache["field_name"] = (
            ("field_name", value),
            (FauxEntryField(), value, None),
        )
        # We have to clear the etag cache for a new value to be generated.
        # XXX benji 2010-09-30 [bug=652459] Does this mean there is an error
        # condition that occurs when something other than applyChanges (which
        # invalidates the cache) modifies a field's value?
        self.resource.etags_by_media_type = {}

    def test_cores_change_with_revno(self):
        # The ETag cores should change if the revision (not the version) of
        # the web service change.
        self.set_field_value("this is the field value")

        # Find the cores generated with a given revision...
        self.config.code_revision = "42"
        first_cores = self.resource._getETagCores(self.resource.JSON_TYPE)

        # ...find the cores generated with a different revision.
        self.config.code_revision = "99"
        second_cores = self.resource._getETagCores(self.resource.JSON_TYPE)

        # The cores should be different.
        self.assertNotEqual(first_cores, second_cores)
        # In particular, the read core should be the same between the two, but
        # the write core should be different.
        self.assertEqual(first_cores[1], second_cores[1])
        self.assertNotEqual(first_cores[0], second_cores[0])

    def test_cores_change_with_value(self):
        # The ETag cores should change if the value of the field change.
        # Find the cores generated with a given value...
        self.set_field_value("first value")
        first_cores = self.resource._getETagCores(self.resource.JSON_TYPE)

        # ...find the cores generated with a different value.
        self.set_field_value("second value")
        second_cores = self.resource._getETagCores(self.resource.JSON_TYPE)

        # The cores should be different.
        self.assertNotEqual(first_cores, second_cores)
        # In particular, the read core should be different between the two,
        # but the write core should be the same.
        self.assertNotEqual(first_cores[1], second_cores[1])
        self.assertEqual(first_cores[0], second_cores[0])


class ServiceRootResourceTests(unittest.TestCase):
    # Tests for ETags of EntryFieldResource objects.

    def setUp(self):
        self.config = TestWebServiceConfiguration()
        provideUtility(self.config, IWebServiceConfiguration)
        self.resource = ServiceRootResource()

    def test_cores_change_with_revno(self):
        # The ETag core should change if the revision (not the version) of the
        # web service change.

        # Find the cores generated with a given revision...
        self.config.code_revision = "42"
        first_cores = self.resource._getETagCores(self.resource.JSON_TYPE)

        # ...find the cores generated with a different revision.
        self.config.code_revision = "99"
        second_cores = self.resource._getETagCores(self.resource.JSON_TYPE)

        # The cores should be different.
        self.assertNotEqual(first_cores, second_cores)

    def test_wadl_etags_change_with_revno(self):
        # The ETag should change if the revision (not the version) of the
        # web service changes.  (At one point this was incorrectly
        # special-cased to exclude the core, and so included no revision
        # information.)

        # Find the ETag generated with a given revision...
        self.config.code_revision = "42"
        first_etag = self.resource.getETag(self.resource.WADL_TYPE)

        # ...and find the ETag generated with a different revision.
        self.resource.etags_by_media_type = {}
        self.config.code_revision = "99"
        second_etag = self.resource.getETag(self.resource.WADL_TYPE)

        # The ETags should be different.
        self.assertNotEqual(first_etag, second_etag)


class TestableHTTPResource(HTTPResource):
    """A HTTPResource that lest us set the ETags from the outside."""

    def _parseETags(self, *args):
        return self.incoming_etags

    def getETag(self, *args):
        return self.existing_etag


class TestConditionalGet(unittest.TestCase):
    def setUp(self):
        self.config = TestWebServiceConfiguration()
        provideUtility(self.config, IWebServiceConfiguration)
        self.request = create_web_service_request("/1.0")
        self.resource = TestableHTTPResource(None, self.request)

    def test_etags_are_the_same(self):
        # If one of the ETags present in an incoming request is the same as
        # the ETag that represents the current object's state, then
        # a conditional GET should return "Not Modified" (304).
        self.resource.incoming_etags = ["1", "2", "3"]
        self.resource.existing_etag = "2"
        self.assertEqual(self.resource.handleConditionalGET(), None)
        self.assertEqual(self.request.response.getStatus(), 304)

    def test_etags_differ(self):
        # If none of the ETags present in an incoming request is the same as
        # the ETag that represents the current object's state, then a
        # conditional GET should result in a new representation of the object
        # being returned.
        self.resource.incoming_etags = ["1", "2", "3"]
        self.resource.existing_etag = "99"
        self.assertNotEqual(self.resource.handleConditionalGET(), None)


class TestConditionalWrite(unittest.TestCase):
    def setUp(self):
        self.config = TestWebServiceConfiguration()
        provideUtility(self.config, IWebServiceConfiguration)
        self.request = create_web_service_request("/1.0")
        self.resource = TestableHTTPResource(None, self.request)

    def test_etags_are_the_same(self):
        # If one of the ETags present in an incoming request is the same as
        # the ETag that represents the current object's state, then
        # the write should be applied.
        self.resource.incoming_etags = ["1", "2", "3"]
        self.resource.existing_etag = "2"
        self.assertNotEqual(self.resource.handleConditionalWrite(), None)

    def test_etags_differ(self):
        # If one of the ETags present in an incoming request is the same as
        # the ETag that represents the current object's state, then
        # the write should fail.
        self.resource.incoming_etags = ["1", "2", "3"]
        self.resource.existing_etag = "99"
        self.assertEqual(self.resource.handleConditionalWrite(), None)
        self.assertEqual(self.request.response.getStatus(), 412)
