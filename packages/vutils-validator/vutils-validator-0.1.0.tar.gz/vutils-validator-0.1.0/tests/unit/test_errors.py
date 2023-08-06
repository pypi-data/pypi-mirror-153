#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_errors.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-01 16:28:57 +0200
# Project: vutils-validator: Data validation utilities
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.validator.errors` module."""

from vutils.testing.testcase import TestCase

from vutils.validator.errors import ValidationError
from vutils.validator.value import Location, ValueHolder


class ValidationErrorTestCase(TestCase):
    """Test case for `ValidationError`."""

    __slots__ = ()

    def test_validation_error(self):
        """Test `ValidationError`."""
        self.do_test("must be 123", "321", "The value must be 123")
        self.do_test(
            "must be 123",
            ValueHolder("321", "foo", Location("./bar.py", 1, 2)),
            "./bar.py:1:2: foo must be 123",
        )

    def do_test(self, message, value, result):
        """
        Do the `ValidationError` test.

        :param message: The message
        :param value: The value
        :param result: The expected result
        """
        with self.assertRaises(ValidationError) as context_manager:
            raise ValidationError(message, value)
        exception = context_manager.exception

        self.assertEqual(repr(exception), result)
        self.assertEqual(str(exception), repr(exception))
