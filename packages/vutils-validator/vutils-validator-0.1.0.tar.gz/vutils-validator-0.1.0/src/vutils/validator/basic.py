#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/validator/basic.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-05-29 21:59:20 +0200
# Project: vutils-validator: Data validation utilities
#
# SPDX-License-Identifier: MIT
#
"""Basic validation."""

import re
from typing import TYPE_CHECKING

from vutils.validator.errors import ValidationError

if TYPE_CHECKING:
    from vutils.validator.value import ValueHolder

EMAIL_RE = r"^\S+@\S+\.[A-Za-z]+$"


def verify_not_empty(value: "ValueHolder | str") -> None:
    """
    Verify that value is not empty.

    :param value: The value to be verified
    :raises ValidationError: when verification fails
    """
    if len(str(value)) == 0:
        raise ValidationError("must not be empty!", value)


def verify_matches(
    value: "ValueHolder | str", regex: str, detail: str = ""
) -> None:
    """
    Verify that value matches the regular expression.

    :param value: The value to be verified
    :param regex: The regular expression
    :param detail: The error detail (default is ``must match `{regex}`!``)
    :raises ValidationError: when verification fails
    """
    if not re.match(regex, str(value)):
        raise ValidationError(detail or f"must match `{regex}`!", value)


def verify_email(value: "ValueHolder | str") -> None:
    """
    Verify that value is an email address.

    :param value: The value to be verified
    :raises ValidationError: when verification fails
    """
    verify_matches(value, EMAIL_RE, "must be an email address!")
