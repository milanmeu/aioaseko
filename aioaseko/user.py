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

"""Aseko API user."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    """Aseko API User."""

    user_id: str
    created_at: datetime
    updated_at: datetime
    name: str
    surname: str
    language: str
    is_active: bool
