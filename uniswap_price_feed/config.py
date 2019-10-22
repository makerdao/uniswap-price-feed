# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2019 grandizzy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional


class Config:
    def __init__(self, base_symbol: str, quote_symbol: str, report_time: int, ro_account: Optional[str], rw_account: Optional[str]):
        assert(isinstance(quote_symbol, str))
        assert(isinstance(base_symbol, str))
        assert(isinstance(report_time, int))
        assert(isinstance(ro_account, str) or ro_account is None)
        assert(isinstance(rw_account, str) or rw_account is None)

        self.base_symbol = base_symbol
        self.quote_symbol = quote_symbol
        self.ro_account = ro_account
        self.rw_account = rw_account
        self.report_time = report_time
