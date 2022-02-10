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

"""aioAseko unit."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .variable import Variable

if TYPE_CHECKING:
    from .mobile import MobileAccount
    from .web import WebAccount


class Unit:
    """Aseko unit."""

    def __init__(
        self,
        account: MobileAccount | WebAccount,
        serial_number: int,
        type: str,
        name: str | None,
        notes: str | None,
        timezone: str,
        is_online: bool,
        date_last_data: str,
        has_error: bool,
    ) -> None:
        """Init Aseko unit."""
        self._account = account
        self._serial_number = serial_number
        self._type = type
        self._name = name
        self._notes = notes
        self._timezone = timezone
        self._is_online = is_online
        self._date_last_data = date_last_data
        self._has_error = has_error

    @property
    def serial_number(self) -> int:
        """Return serial number, set on init."""
        return self._serial_number

    @property
    def type(self) -> str:
        """Return type, set on init."""
        return self._type

    @property
    def name(self) -> str | None:
        """Return name, set on init."""
        return self._name

    @property
    def notes(self) -> str | None:
        """Return notes, set on init."""
        return self._notes

    @property
    def timezone(self) -> str:
        """Return timezone, set on init."""
        return self._timezone

    @property
    def is_online(self) -> bool:
        """Return is online, set on init."""
        return self._is_online

    @property
    def date_last_data(self) -> str:
        """Return date of last data, set on init."""
        return self._date_last_data

    @property
    def has_error(self) -> bool:
        """Return has error, set on init and get_state()."""
        return self._has_error

    @property
    def errors(self) -> list[UnitError]:
        """Return errors, set on get_state()."""
        return self._errors

    @property
    def variables(self) -> list[Variable]:
        """Return variables, set on get_state()."""
        return self._variables

    @property
    def has_alarm(self) -> bool:
        """Return has alarm, set on get_state()."""
        return self._has_alarm

    @property
    def water_flow(self) -> bool:
        """Return water flow, set on get_state()."""
        return self._water_flow

    async def get_state(self) -> None:
        """Get the unit state."""
        resp = await self._account._request("get", f"units/{self._serial_number}")
        data = await resp.json()
        self._errors = [
            UnitError(error["type"], error["title"], error["content"])
            for error in data["errors"]
        ]
        self._has_error = len(self._errors) >= 1
        self._variables = [
            Variable(
                variable["type"],
                variable["name"],
                variable["unit"],
                variable["icon"],
                variable["color"],
                variable["hasError"],
                variable.get("currentValue"),
                variable.get("required"),
                variable.get("alarm", {}).get("active"),
                variable.get("alarm", {}).get("minValue"),
                variable.get("alarm", {}).get("maxValue"),
            )
            for variable in data["variables"]
        ]
        self._has_alarm: bool = data["errorsAlarm"]["active"]
        self._water_flow: bool = not data.get("noWaterFlow", False)


@dataclass(frozen=True)
class UnitError:
    """Aseko unit error."""

    type: str
    title: str
    content: list[str]
