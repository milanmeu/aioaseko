# Copyright 2021, 2022 Milan Meulemans.
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

from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    """Aseko variable."""

    type: str
    name: str
    unit: str
    icon: str
    color: str
    has_error: bool
    current_value: int | None
    required_value: int | None
    has_alarm: bool | None
    min_value: int | None
    max_value: int | None
