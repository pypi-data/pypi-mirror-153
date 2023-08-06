#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_version.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-05-03 21:26:33 +0200
# Project: vutils-validator: Data validation utilities
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.validator.version` module."""

from vutils.testing.testcase import TestCase

from vutils.validator.version import __version__


class VersionTestCase(TestCase):
    """Test case for version."""

    __slots__ = ()

    def test_version(self):
        """Test if version is defined properly."""
        self.assertIsInstance(__version__, str)
