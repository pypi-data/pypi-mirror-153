#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_value.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-01 10:07:23 +0200
# Project: vutils-validator: Data validation utilities
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.validator.value` module."""

from vutils.testing.testcase import TestCase

from vutils.validator.value import Location, ValueHolder


class LocationTestCase(TestCase):
    """Test case for `Location`."""

    __slots__ = ()

    def test_constructor_default(self):
        """
        Test initialization.

        Test `Location` object initialization with default values.
        """
        location = Location()

        self.assertIsNone(location.path)
        self.assertEqual(location.line, -1)
        self.assertEqual(location.column, -1)

    def test_constructor_custom(self):
        """
        Test initialization.

        Test `Location` object initialization with custom values.
        """
        path, line, column = "./foo.py", 42, 7
        location = Location(path, line, column)

        self.assertEqual(location.path, path)
        self.assertEqual(location.line, line)
        self.assertEqual(location.column, column)

    def test_to_str_conversion(self):
        """Test `Location.__str__`."""
        testset = [
            ((), ""),
            (("./foo.bar", -1, -1), "./foo.bar"),
            ((None, 42, -1), "42"),
            ((None, -1, 42), "?:42"),
            ((None, 42, 7), "42:7"),
            (("./foo", 42, -1), "./foo:42"),
            (("./foo", -1, 42), "./foo:?:42"),
            (("./foo", 42, 7), "./foo:42:7"),
        ]

        for item in testset:
            self.assertEqual(str(Location(*item[0])), item[1])


class ValueHolderTestCase(TestCase):
    """Test case for `ValueHolder`."""

    __slots__ = ()

    def test_constructor_default(self):
        """
        Test initialization.

        Test `ValueHolder` object initialization with default values.
        """
        value = "quux"
        holder = ValueHolder(value)

        self.assertEqual(holder.value, value)
        self.assertEqual(holder.name, "The value")
        self.assertIsInstance(holder.location, Location)

    def test_constructor_custom(self):
        """
        Test initialization.

        Test `ValueHolder` object initialization with custom values.
        """
        value, name, location = "baz", "foo", Location()
        holder = ValueHolder(value, name, location)

        self.assertEqual(holder.value, value)
        self.assertEqual(holder.name, name)
        self.assertIs(holder.location, location)

    def test_value_extraction(self):
        """Test `ValueHolder.__str__`."""
        value = "foobar"
        holder = ValueHolder(value)

        self.assertEqual(str(holder), value)
        self.assertEqual(str(holder), holder.value)

    def test_detail(self):
        """Test `ValueHolder.detail`."""
        testset = [
            (("baz",), "is bad", "The value is bad"),
            (("baz", "foo"), "is bad", "foo is bad"),
            (
                ("baz", "foo", Location(None, 42, 7)),
                "is bad",
                "42:7: foo is bad",
            ),
        ]

        for item in testset:
            self.assertEqual(ValueHolder(*item[0]).detail(item[1]), item[2])
