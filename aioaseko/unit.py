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

"""aioAseko unit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from .consumable import ElectrolyzerConsumable, LiquidConsumable
from .status_value import StatusValues, StatusValueType, StringValue

T = TypeVar("T", int, float, str, bool)


@dataclass(frozen=True)
class UnitNeverConnected:
    """Aseko Unit that has never connected."""

    serial_number: str
    name: str | None
    note: str | None
    position: int
    online: bool


@dataclass(frozen=True)
class Unit:
    """Aseko Unit that has connected."""

    serial_number: str
    name: str | None
    note: str | None
    online: bool
    has_warning: bool
    time_zone: str
    position: int
    brand_name: UnitBrandName | None
    consumables: list[LiquidConsumable | ElectrolyzerConsumable]
    status_values: StatusValues

    @property
    def air_temperature(self) -> float | None:
        """Return the air temperature."""
        return self._converted_status_value(StatusValueType.AIR_TEMPERATURE, float)

    @property
    def cl_free(self) -> float | None:
        """Return the free chlorine."""
        return self._converted_status_value(StatusValueType.CL_FREE, float)

    @property
    def dose(self) -> int | None:
        """Return the dose."""
        return self._converted_status_value(StatusValueType.DOSE, int)

    @property
    def electrolyzer(self) -> int | None:
        """Return the electrolyzer."""
        return self._converted_status_value(StatusValueType.ELECTROLYZER, int)

    @property
    def heating(self) -> bool | None:
        """Return the heating status."""
        return self._converted_status_value(StatusValueType.HEATING, bool)

    @property
    def ph(self) -> float | None:
        """Return the pH value."""
        return self._converted_status_value(StatusValueType.PH, float)

    @property
    def redox(self) -> int | None:
        """Return the redox value."""
        return self._converted_status_value(StatusValueType.REDOX, int)

    @property
    def salinity(self) -> float | None:
        """Return the salinity."""
        return self._converted_status_value(StatusValueType.SALINITY, float)

    @property
    def water_flow_to_probes(self) -> bool | None:
        """Return the water flow to probes."""
        return self._converted_status_value(StatusValueType.WATER_FLOW_TO_PROBES, bool)

    @property
    def water_temperature(self) -> float | None:
        """Return the water temperature."""
        return self._converted_status_value(StatusValueType.WATER_TEMPERATURE, float)

    def _status_value_string_value(
        self, status_value_type: StatusValueType
    ) -> str | None:
        """Return the status value of the given type, only for string values."""
        for status_value in self.status_values.primary:
            if status_value.type == status_value_type:
                if isinstance(status_value.center, StringValue):
                    return status_value.center.value
                raise ValueError(f"Value of {status_value_type} is not a string.")
        for status_value in self.status_values.secondary:
            if status_value.type == status_value_type:
                if isinstance(status_value.center, StringValue):
                    return status_value.center.value
                raise ValueError(f"Value of {status_value_type} is not a string.")
        return None

    def _converted_status_value(
        self, status_value_type: StatusValueType, return_type: type[T]
    ) -> T | None:
        """Return the status value of the given status type, converted to the given type.

        Only for status value types with string value.
        """
        value = self._status_value_string_value(status_value_type)
        if value is None or value == "---":
            return None
        if return_type is bool:
            if value in ("YES", "ON"):
                return return_type(True)
            if value in ("NO", "OFF"):
                return return_type(False)
            raise ValueError(f"Value of {status_value_type} is not a boolean.")
        return return_type(value)


@dataclass(frozen=True)
class UnitBrandName:
    """Brand name of the unit."""

    primary: str
    secondary: str
