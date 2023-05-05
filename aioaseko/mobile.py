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

"""aioAseko mobile API account."""
from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp import ClientError

from .exceptions import APIUnavailable, InvalidAuthCredentials
from .unit import Unit

from jwt import decode, get_unverified_header
from time import time


if TYPE_CHECKING:
    from aiohttp import ClientResponse, ClientSession


class MobileAccount:
    """Aseko account."""

    TOKEN_EXPIRATION_BUFFER = 60

    def __init__(
        self,
        session: ClientSession,
        username: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
        access_token_expiration: int | None = None,
        refresh_token: str | None = None,
    ) -> None:
        """Init Aseko account."""
        self._session = session
        self._username = username
        self._password = password
        self._access_token = access_token
        self._access_token_expiration = access_token_expiration
        self._refresh_token = refresh_token

    @property
    def refresh_token(self) -> str | None:
        """Return refresh token."""
        return self._refresh_token

    @property
    def access_token_expiration(self) -> int | None:
        """Return access token expiration."""
        return self._access_token_expiration

    async def _request(
        self, method: str, path: str, data: dict | None = None
    ) -> ClientResponse:
        """Make a request to the Aseko mobile API."""
        resp = await self._session.request(
            method,
            f"https://pool.aseko.com/api/v1/{path}",
            data=data,
            headers=None
            if self._access_token is None
            else {"access-token": await self.access_token()},
        )
        if resp.status == 401:
            raise InvalidAuthCredentials
        try:
            resp.raise_for_status()
        except ClientError:
            raise APIUnavailable
        return resp

    async def login(self) -> None:
        """Login to Aseko Pool Live with username and password."""
        resp = await self._request(
            "post",
            "login",
            {
                "username": self._username,
                "password": self._password,
                "firebaseId": "",
            },
        )
        data = await resp.json()
        self.retrieve_tokens(data)

    async def access_token(self) -> str | None:
        """Return access token."""
        now = time()
        if (self.access_token_expiration <= now + self.TOKEN_EXPIRATION_BUFFER):
            self._access_token = None
            try:
                await self.refresh()
            except InvalidAuthCredentials:
                await self.login()
        return self._access_token

    async def refresh(self) -> None:
        """Refresh access token for Aseko Pool Live with refresh token."""
        resp = await self._request(
            "post",
            "refresh",
            {
                "refreshToken": self._refresh_token,
                "firebaseId": "",
            },
        )
        data = await resp.json()
        self.retrieve_tokens(data)

    async def logout(self) -> None:
        """Logout Aseko Pool Live account."""
        await self._request("post", "logout")
        self._access_token = None
        self._access_token_expiration = None
        self._refresh_token = None

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

    def retrieve_tokens(self, data: dict) -> None:
        algorithm = get_unverified_header(data["accessToken"]).get('alg')
        token = decode(
            jwt=data["accessToken"],
            key="",
            algorithms=algorithm,
            options={
                "verify_signature": False
            },
        )
        self._access_token = data["accessToken"]
        self._access_token_expiration = token["exp"]
        self._refresh_token = data["refreshToken"]
