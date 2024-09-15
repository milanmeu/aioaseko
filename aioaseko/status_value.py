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

"""aioAseko status value."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .filtration import FiltrationInterval


class StatusValueType(Enum):
    """Status value type."""

    AIR_TEMPERATURE = "AIR_TEMPERATURE"
    CL_FREE = "CL_FREE"
    DOSE = "DOSE"
    ELECTROLYZER = "ELECTROLYZER"
    FILTER_FLOW = "FILTER_FLOW"
    FILTRATION_PUMP_SPEED = "FILTRATION_PUMP_SPEED"
    HEATING = "HEATING"
    LIGHTS_STATE = "LIGHTS_STATE"
    MODE = "MODE"
    PH = "PH"
    POOL_FLOW = "POOL_FLOW"
    PUMP_SPEED = "PUMP_SPEED"
    REDOX = "REDOX"
    REDOX_PRO = "REDOX_PRO"
    SALINITY = "SALINITY"
    SOLAR = "SOLAR"
    SOLAR_TEMPERATURE = "SOLAR_TEMPERATURE"
    SOLAR_TIMER = "SOLAR_TIMER"
    UPCOMING_FILTRATION_PERIOD = "UPCOMING_FILTRATION_PERIOD"
    WATER_FLOW_TO_PROBES = "WATER_FLOW_TO_PROBES"
    WATER_LEVEL = "WATER_LEVEL"
    WATER_TEMPERATURE = "WATER_TEMPERATURE"


@dataclass(frozen=True)
class StatusValues:
    """Status values."""

    primary: list[StatusValue]
    secondary: list[StatusValue]


@dataclass(frozen=True)
class StatusValue:
    """Status value."""

    type: StatusValueType
    center: StringValue | UpcomingFiltrationPeriodValue


@dataclass(frozen=True)
class StringValue:
    """String value."""

    value: str


@dataclass(frozen=True)
class UpcomingFiltrationPeriodValue:
    """Upcoming filtration period value."""

    configuration: FiltrationInterval
    is_next: bool
