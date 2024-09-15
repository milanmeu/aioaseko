# Copyright 2021, 2022, 2024 Milan Meulemans.
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

"""aioAseko consumables."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import Enum


class ConsumableType(Enum):
    """Consumable type."""

    ALGICIDE = "ALGICIDE"
    CL = "CL"
    ELECTRODE = "ELECTRODE"
    FILTER_DISINFECTION = "FILTER_DISINFECTION"
    FLOCCULANT = "FLOCCULANT"
    PH_MINUS = "PH_MINUS"
    PH_PLUS = "PH_PLUS"


@dataclass(frozen=True)
class Consumable(ABC):
    """Unit consumable generic class."""

    type: ConsumableType
    name: str


@dataclass(frozen=True)
class LiquidConsumable(Consumable):
    """Unit liquid consumable."""

    canister: Canister
    tube: Tube


@dataclass(frozen=True)
class ElectrolyzerConsumable(Consumable):
    """Unit electrolyzer consumable."""

    electrode: Electrode


@dataclass(frozen=True)
class Canister:
    """Canister data."""

    remaining: int
    has_warning: bool
    volume: int | None


@dataclass(frozen=True)
class Tube:
    """Tube data."""

    remaining: int
    has_warning: bool
    remaining_days: int


@dataclass
class Electrode:
    """Electrode data."""

    remaining: int
    week_chlorine_production: float
    has_warning: bool
