# Copyright 2021, Milan Meulemans.
#
# This file is part of aioaseko.
#
# aioaseko is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# aioaseko is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with aioaseko.  If not, see <https://www.gnu.org/licenses/>.

"""aioAseko variable."""
from __future__ import annotations


class Variable:
    """Aseko variable."""

    def __init__(
        self,
        type: str,
        name: str,
        unit: str,
        icon: str,
        color: str,
        has_error: bool,
        current_value: int | None,
        required_value: int | None,
        alarm: bool | None,
        min_value: int | None,
        max_value: int | None,
    ) -> None:
        """Init Aseko variable."""
        self._type = type
        self._name = name
        self._unit = unit
        self._icon = icon
        self._color = color
        self._has_error = has_error
        self._current_value = current_value
        self._required_value = required_value
        self._has_alarm = alarm
        self._min_value = min_value
        self._max_value = max_value

    @property
    def type(self) -> str:
        """Return type."""
        return self._type

    @property
    def name(self) -> str:
        """Return name."""
        return self._name

    @property
    def unit(self) -> str:
        """Return unit."""
        return self._unit

    @property
    def icon(self) -> str:
        """Return icon."""
        return self._icon

    @property
    def color(self) -> str:
        """Return color."""
        return self._color

    @property
    def has_error(self) -> bool:
        """Return has error."""
        return self._has_error

    @property
    def current_value(self) -> int | None:
        """Return current_value."""
        return self._current_value

    @property
    def required_value(self) -> int | None:
        """Return required."""
        return self._required_value

    @property
    def has_alarm(self) -> bool | None:
        """Return has alarm."""
        return self._has_alarm

    @property
    def min_value(self) -> int | None:
        """Return min value."""
        return self._min_value

    @property
    def max_value(self) -> int | None:
        """Return max value."""
        return self._max_value
