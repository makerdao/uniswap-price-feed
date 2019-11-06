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

import argparse
import logging
import sys
import tornado
from uniswap_price_feed.feed import FeedSocketHandler
from uniswap_price_feed.config import Config
from web3 import Web3, HTTPProvider

from pyexchange.uniswap import Uniswap
from pymaker import Address

class UniswapPriceFeed:
    """Uniswap Price Feed server."""

    logger = logging.getLogger()

    def __init__(self, args: list, **kwargs):
        parser = argparse.ArgumentParser(prog='uniswap-price-feed')

        parser.add_argument("--rpc-host", type=str, default="localhost",
                            help="JSON-RPC host (default: `localhost')")

        parser.add_argument("--rpc-port", type=int, default=8545,
                            help="JSON-RPC port (default: `8545')")

        parser.add_argument("--rpc-timeout", type=int, default=10,
                            help="JSON-RPC timeout (in seconds, default: 10)")

        parser.add_argument("--http-address", type=str, default='',
                            help="Address of the Uniswap Price Feed")

        parser.add_argument("--http-port", type=int, default=7777,
                            help="Port of the Uniswap Price Feed")

        parser.add_argument("--base-exchange-address", type=str, default=None,
                            help="Address of the Uniswap Exchange")

        parser.add_argument("--base-token-symbol", type=str, default='ETH',
                            help="Token symbol")

        parser.add_argument("--base-token-address", type=str, default='',
                            help="Token address")

        parser.add_argument("--quote-exchange-address", type=str, default='',
                            help="Address of the Quote Uniswap Exchange", required=True)

        parser.add_argument("--quote-token-symbol", type=str, default='',
                        help="Quote Token symbol", required=True)

        parser.add_argument("--quote-token-address", type=str, default='',
                        help="Quote Token address", required=True)

        parser.add_argument("--report-time", type=int, default=10,
                            help="Time interval to report price")

        parser.add_argument("--ro-account", type=str,
                            help="Credentials of the read-only user (format: username:password)")

        parser.add_argument("--rw-account", type=str,
                            help="Credentials of the read-write user (format: username:password)")

        self.arguments = parser.parse_args(args)

        if self.arguments.rpc_host.startswith("https"):
            endpoint_uri = f"{self.arguments.rpc_host}"
        else:
            endpoint_uri = f"http://{self.arguments.rpc_host}:{self.arguments.rpc_port}"

        self.web3 = kwargs['web3'] if 'web3' in kwargs else Web3(HTTPProvider(endpoint_uri=endpoint_uri,
                                                                              request_kwargs={"timeout": self.arguments.rpc_timeout}))

        self.web3.eth.defaultAccount = "0x0000000000000000000000000000000000000000"

        if self.arguments.base_exchange_address is not None:
            self.base_uniswap = Uniswap(self.web3, Address(self.arguments.base_token_address), Address(self.arguments.base_exchange_address))
        else:
            self.base_uniswap = None

        self.quote_uniswap = Uniswap(self.web3, Address(self.arguments.quote_token_address), Address(self.arguments.quote_exchange_address))

        self.config = Config(
            base_symbol=self.arguments.base_token_symbol,
            quote_symbol=self.arguments.quote_token_symbol,
            report_time=self.arguments.report_time,
            ro_account=self.arguments.ro_account,
            rw_account=self.arguments.rw_account)

        application = tornado.web.Application([
            (f"/price/{self.arguments.base_token_symbol}-{self.arguments.quote_token_symbol}/socket", FeedSocketHandler,
                dict(base_uniswap=self.base_uniswap,
                     quote_uniswap=self.quote_uniswap,
                     config=self.config))
        ])
        application.listen(port=self.arguments.http_port,address=self.arguments.http_address)
        tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.INFO)
    UniswapPriceFeed(sys.argv[1:]).main()
