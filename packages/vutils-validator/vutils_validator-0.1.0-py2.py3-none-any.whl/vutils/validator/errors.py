#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/validator/errors.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-05-29 21:45:41 +0200
# Project: vutils-validator: Data validation utilities
#
# SPDX-License-Identifier: MIT
#
"""Validation errors."""

from vutils.validator.value import ValueHolder


class ValidationError(Exception):
    """Used to report failed checks."""

    __slots__ = ("message", "value")

    def __init__(self, message: str, value: "ValueHolder | str") -> None:
        """
        Initialize the error object.

        :param message: The error message
        :param value: The value
        """
        Exception.__init__(self)
        self.message = message
        self.value = (
            value if isinstance(value, ValueHolder) else ValueHolder(value)
        )

    def __repr__(self) -> str:
        """
        Get the error representation.

        :return: the error representation
        """
        return self.value.detail(self.message)

    def __str__(self) -> str:
        """
        Get the error representation (`str` alias).

        :return: the error representation
        """
        return repr(self)
