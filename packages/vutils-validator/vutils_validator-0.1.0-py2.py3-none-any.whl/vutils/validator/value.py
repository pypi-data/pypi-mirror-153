#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/validator/value.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-05-31 11:51:57 +0200
# Project: vutils-validator: Data validation utilities
#
# SPDX-License-Identifier: MIT
#
"""Value holder."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pathlib


class Location:
    """Hold value/token location."""

    __slots__ = ("path", "line", "column")

    def __init__(
        self,
        path: "str | pathlib.Path | None" = None,
        line: int = -1,
        column: int = -1,
    ) -> None:
        """
        Initialize the location.

        :param path: The path to the file of the value/token origin
        :param line: The line number of the value/token origin
        :param column: The column number of the value/token origin
        """
        self.path = path
        self.line = line
        self.column = column

    def __str__(self) -> str:
        """
        Give the string representation of the value/token location.

        :return: the value/token location as a `str` object

        Location is of the form ``{path}:{line}:{column}``, where ``path``,
        ``line``, and ``column`` are omitted together with redundant ``:`` if
        they are `None`, negative, and negative, respectively. If ``line`` is
        negative and ``column`` is not, the result is ``{path}:?:{column}``.
        """
        location: str = ""
        if self.path is not None:
            location += f"{self.path}"
        if self.line >= 0:
            if location:
                location += ":"
            location += f"{self.line}"
        if self.column >= 0:
            if location:
                location += ":"
            if self.line < 0:
                location += "?:"
            location += f"{self.column}"
        return location


class ValueHolder:
    """Hold value with its context."""

    __slots__ = ("value", "name", "location")

    def __init__(
        self,
        value: str,
        name: str = "The value",
        location: "Location | None" = None,
    ) -> None:
        """
        Initialize the value holder.

        :param value: The value
        :param name: The name of the value
        :param location: The location of the value origin
        """
        self.value = value
        self.name = name
        self.location = location or Location()

    def __str__(self) -> str:
        """
        Get the stored value.

        :return: the stored value
        """
        return self.value

    def detail(self, message: str) -> str:
        """
        Add detail information about the value to the message.

        :param message: The message
        :return: detail information about the value

        Add the value location if present and the value name to *message* so
        the final form is ``{location}: {name} {message}``.
        """
        location: str = str(self.location)

        detail: str = f"{self.name} {message}"
        if location:
            detail = f"{location}: {detail}"
        return detail
