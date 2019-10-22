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

import base64

from uniswap_price_feed.config import Config


class AuthenticationMixin(object):
    def _send_auth_challenge(self) -> bool:
        self.set_status(401)
        self.set_header('WWW-Authenticate', 'Basic realm="Protected area"')
        self.finish()

        return False

    def _authenticate_user(self, write: bool):
        assert(isinstance(write, bool))
        assert(isinstance(self.config, Config))

        auth_header = self.request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            return self._send_auth_challenge()

        auth_data = auth_header.split(None, 1)[-1]
        auth_data = base64.b64decode(auth_data).decode('ascii')

        allowed_auth_data = [self.config.rw_account] if write else [self.config.ro_account, self.config.rw_account]

        if auth_data in allowed_auth_data:
            return True
        else:
            return self._send_auth_challenge()


def auth_required(write: bool):
    def auth_decorator(func):
        def inner(self, *args, **kw):
            if self._authenticate_user(write):
                return func(self, *args, **kw)
        return inner

    return auth_decorator