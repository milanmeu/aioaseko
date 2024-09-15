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

"""aioAseko Aseko API."""

from datetime import datetime
import logging
from typing import Any, cast

from aiohttp import ClientSession
from apischema import deserialize
from gql import Client
from gql.dsl import DSLInlineFragment, DSLQuery, DSLSchema, dsl_gql, to_camel_case
from gql.transport.aiohttp import AIOHTTPTransport, log as gql_log
from gql.transport.exceptions import TransportQueryError
from yarl import URL

from .exceptions import AsekoAPIError, AsekoInvalidCredentials, AsekoNotLoggedIn
from .unit import Unit, UnitNeverConnected
from .user import User

AUTH_URL = "https://auth.aseko.acs.aseko.cloud/auth"
GRAPHQL_URL = "https://graphql.acs.prod.aseko.cloud/graphql"

gql_log.setLevel(logging.ERROR)


class Aseko:
    """Aseko API."""

    def __init__(self, email: str, password: str) -> None:
        """Initialize the Aseko API."""
        self._email = email
        self._password = password
        self._token: str | None = None
        self._refresh_token: str | None = None
        self._cached_schema: DSLSchema | None = None

    async def login(self) -> User:
        """Login to the Aseko API."""
        async with ClientSession() as session:
            resp = await session.post(
                AUTH_URL + "/login",
                json={
                    "email": self._email,
                    "password": self._password,
                    "cloud": "01HXS50KTV7NRSVNHD617J4CKB",
                },
            )
        if resp.status == 401:
            raise AsekoInvalidCredentials
        try:
            resp.raise_for_status()
        except Exception as e:
            raise AsekoAPIError from e
        data = await resp.json()
        self._token = data["token"]
        self._refresh_token = resp.cookies["refreshToken"].value
        return User(
            data["user"]["id"],
            datetime.fromisoformat(data["user"]["createdAt"]),
            datetime.fromisoformat(data["user"]["updatedAt"]),
            data["user"]["name"],
            data["user"]["surname"],
            data["user"]["lang"],
            data["user"]["isActive"],
        )

    async def _token_refresh(self) -> None:
        """Refresh the token."""
        assert self._refresh_token is not None
        async with ClientSession() as session:
            session.cookie_jar.update_cookies(
                {"refreshToken": self._refresh_token}, URL(AUTH_URL)
            )
            resp = await session.post(AUTH_URL + "/refresh-token")
        try:
            resp.raise_for_status()
        except Exception as e:
            raise AsekoAPIError from e
        data = await resp.json()
        self._token = data["token"]

    def _client(self) -> Client:
        """Return the Aseko GraphQL client."""
        if self._token is None:
            raise AsekoNotLoggedIn
        transport = AIOHTTPTransport(
            url=GRAPHQL_URL, headers={"Authorization": f"Bearer {self._token}"}
        )
        return Client(transport=transport, fetch_schema_from_transport=True)

    async def _schema(self) -> DSLSchema:
        """Return the Aseko GraphQL schema."""
        if self._cached_schema is None:
            async with self._client() as session:
                self._cached_schema = DSLSchema(session.client.schema)
        return self._cached_schema

    async def _query(self, query: DSLQuery, retry: bool = True) -> dict[str, Any]:
        """Query the Aseko GraphQL API."""
        async with self._client() as session:
            document = dsl_gql(query)
            try:
                result = await session.execute(document)
            except TransportQueryError as e:
                if not retry:
                    raise AsekoAPIError from e
                await self._token_refresh()
                result = await self._query(query, False)
            return cast(dict[str, Any], result)

    async def get_all_units(self) -> list[Unit | UnitNeverConnected]:
        """Get all units, including never connected units."""

        def unit_deserializer(data: dict) -> Unit | UnitNeverConnected:
            """Deserialize a unit."""
            if "brandName" in data:
                return deserialize(Unit, data, aliaser=to_camel_case)
            return deserialize(UnitNeverConnected, data, aliaser=to_camel_case)

        ds = await self._schema()
        query = DSLQuery(
            ds.Query.units.select(
                ds.UnitList.units.select(
                    DSLInlineFragment()
                    .on(ds.Unit)
                    .select(
                        ds.Unit.serialNumber,
                        ds.Unit.name,
                        ds.Unit.note,
                        ds.Unit.online,
                        ds.Unit.hasWarning,
                        ds.Unit.timeZone,
                        ds.Unit.position,
                        ds.Unit.brandName.select(
                            ds.UnitBrandName.primary,
                            ds.UnitBrandName.secondary,
                        ),
                        ds.Unit.consumables.select(
                            DSLInlineFragment()
                            .on(ds.LiquidConsumable)
                            .select(
                                ds.LiquidConsumable.type,
                                ds.LiquidConsumable.name,
                                ds.LiquidConsumable.canister.select(
                                    ds.Canister.remaining,
                                    ds.Canister.hasWarning,
                                    ds.Canister.volume,
                                ),
                                ds.LiquidConsumable.tube.select(
                                    ds.Tube.remaining,
                                    ds.Tube.hasWarning,
                                    ds.Tube.remainingDays,
                                ),
                            ),
                            DSLInlineFragment()
                            .on(ds.ElectrolyzerConsumable)
                            .select(
                                ds.ElectrolyzerConsumable.type,
                                ds.ElectrolyzerConsumable.name,
                                ds.ElectrolyzerConsumable.electrode.select(
                                    ds.Electrode.remaining,
                                    ds.Electrode.weekChlorineProduction,
                                    ds.Electrode.hasWarning,
                                ),
                            ),
                        ),
                        ds.Unit.statusValues.select(
                            ds.StatusValues.primary.select(
                                ds.StatusValue.type,
                                ds.StatusValue.center.select(
                                    DSLInlineFragment()
                                    .on(ds.StringValue)
                                    .select(
                                        ds.StringValue.value,
                                    ),
                                    DSLInlineFragment()
                                    .on(ds.UpcomingFiltrationPeriodValue)
                                    .select(
                                        ds.UpcomingFiltrationPeriodValue.configuration.select(
                                            ds.FiltrationInterval.period,
                                            ds.FiltrationInterval.name,
                                        ),
                                        ds.UpcomingFiltrationPeriodValue.isNext,
                                    ),
                                ),
                            ),
                            ds.StatusValues.secondary.select(
                                ds.StatusValue.type,
                                ds.StatusValue.center.select(
                                    DSLInlineFragment()
                                    .on(ds.StringValue)
                                    .select(
                                        ds.StringValue.value,
                                    ),
                                    DSLInlineFragment()
                                    .on(ds.UpcomingFiltrationPeriodValue)
                                    .select(
                                        ds.UpcomingFiltrationPeriodValue.configuration.select(
                                            ds.FiltrationInterval.period,
                                            ds.FiltrationInterval.name,
                                        ),
                                        ds.UpcomingFiltrationPeriodValue.isNext,
                                    ),
                                ),
                            ),
                        ),
                    ),
                    DSLInlineFragment()
                    .on(ds.UnitNeverConnected)
                    .select(
                        ds.UnitNeverConnected.serialNumber,
                        ds.UnitNeverConnected.name,
                        ds.UnitNeverConnected.note,
                        ds.UnitNeverConnected.position,
                        ds.UnitNeverConnected.online,
                    ),
                ),
            )
        )
        result = await self._query(query)
        return deserialize(
            list[Unit | UnitNeverConnected],
            result["units"]["units"],
            aliaser=to_camel_case,
            conversion=unit_deserializer,
        )

    async def get_units(self) -> list[Unit]:
        """Get active units."""
        units = await self.get_all_units()
        return [unit for unit in units if isinstance(unit, Unit)]
