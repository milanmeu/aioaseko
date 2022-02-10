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

"""aioAseko web API account."""
from __future__ import annotations

from dataclasses import dataclass

from aiohttp import ClientError, ClientResponse, ClientSession

from .exceptions import APIUnavailable, InvalidAuthCredentials
from .unit import Unit


class WebAccount:
    """Aseko web account."""

    def __init__(self, session: ClientSession, username: str, password: str) -> None:
        """Init Aseko account."""
        self._session = session
        self._username = username
        self._password = password

    async def _request(
        self, method: str, path: str, data: dict | None = None
    ) -> ClientResponse:
        """Make a request to the Aseko web API."""
        resp = await self._session.request(
            method, f"https://pool.aseko.com/api/{path}", data=data
        )
        if resp.status == 401:
            raise InvalidAuthCredentials
        try:
            resp.raise_for_status()
        except ClientError:
            raise APIUnavailable
        return resp

    async def login(self) -> AccountInfo:
        """Login to the Aseko web API."""
        resp = await self._request(
            "post",
            "login",
            {
                "username": self._username,
                "password": self._password,
                "agree": "on",
            },
        )
        data = await resp.json()
        return AccountInfo(data["email"], data["userId"], data.get("language"))

    async def get_units(self) -> list[Unit]:
        """Get units."""
        resp = await self._request("get", "units")
        data = await resp.json()
        return [
            Unit(
                self,
                int(item["serialNumber"]),
                item["type"],
                item.get("name"),
                item.get("notes"),
                item["timezone"],
                item["isOnline"],
                item["dateLastData"],
                item["hasError"],
            )
            for item in data["items"]
        ]


@dataclass(frozen=True)
class AccountInfo:
    """Aseko account info."""

    email: str
    user_id: str
    language: str | None
