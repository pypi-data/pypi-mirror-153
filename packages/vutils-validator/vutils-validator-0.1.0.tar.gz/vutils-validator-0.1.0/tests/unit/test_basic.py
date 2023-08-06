#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_basic.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-01 18:00:18 +0200
# Project: vutils-validator: Data validation utilities
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.validator.basic` module."""

from vutils.testing.testcase import TestCase

from vutils.validator.basic import (
    verify_email,
    verify_matches,
    verify_not_empty,
)
from vutils.validator.errors import ValidationError
from vutils.validator.value import ValueHolder


class BasicValidationTestCase(TestCase):
    """Test case for basic validation."""

    __slots__ = ()

    def test_verify_not_empty(self):
        """Test `verify_not_empty`."""
        self.do_test(verify_not_empty, ("",), "The value must not be empty!")
        self.do_test(
            verify_not_empty,
            (ValueHolder("", "foobar"),),
            "foobar must not be empty!",
        )
        self.do_test(verify_not_empty, ("foo",), None)

    def test_verify_matches(self):
        """Test `verify_matches`."""
        regex = r"^[_A-Za-z][_0-9A-Za-z]*$"

        self.do_test(
            verify_matches, ("-", regex), f"The value must match `{regex}`!"
        )
        self.do_test(
            verify_matches,
            ("-", regex, "must be an identifier!"),
            "The value must be an identifier!",
        )
        self.do_test(
            verify_matches,
            (ValueHolder("-", "foobar"), regex, "must be an identifier!"),
            "foobar must be an identifier!",
        )
        self.do_test(verify_matches, ("_foo", regex), None)

    def test_verify_email(self):
        """Test `verify_email`."""
        self.do_test(
            verify_email, ("foo@bar",), "The value must be an email address!"
        )
        self.do_test(
            verify_email,
            (ValueHolder("foo@bar", "foobar"),),
            "foobar must be an email address!",
        )
        self.do_test(verify_email, ("foo@bar.baz",), None)

    def do_test(self, func, args, result):
        """
        Do the test of basic validation.

        :param func: The validation function
        :param args: The validation function arguments
        :param result: The expected result

        Expected result set to `None` signals that the validation function
        should not raise an exception. Otherwise the validation function should
        raise `ValidationError` and its representation should match the
        expected result.
        """
        if result is None:
            func(*args)
            return
        with self.assertRaises(ValidationError) as context_manager:
            func(*args)
        self.assertEqual(f"{context_manager.exception}", result)
