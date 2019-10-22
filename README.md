# uniswap-price-feed

This repository contains a standalone service for publishing Uniswap prices over Websockets.


## Rationale

This service facilitates distribution of real-time Uniswap prices to keeper bots from the `market-maker-keeper`
<https://github.com/makerdao/market-maker-keeper> repository. Prices are retrieved from chain every second.
The average of last 60 prices are reported to subscribed clients.


## Installation

This project uses *Python 3.6.6* and requires *virtualenv* to be installed.

In order to clone the project and install required third-party packages please execute:
```
git clone https://github.com/makerdao/uniswap-price-feed.git
cd uniswap-price-feed
./install.sh
```


## Running

```
usage: uniswap-price-feed [-h] [--rpc-host RPC_HOST] [--rpc-port RPC_PORT]
                          [--rpc-timeout RPC_TIMEOUT]
                          [--http-address HTTP_ADDRESS]
                          [--http-port HTTP_PORT]
                          [--base-exchange-address BASE_EXCHANGE_ADDRESS]
                          [--base-token-symbol BASE_TOKEN_SYMBOL]
                          [--base-token-address BASE_TOKEN_ADDRESS]
                          --quote-exchange-address QUOTE_EXCHANGE_ADDRESS
                          --quote-token-symbol QUOTE_TOKEN_SYMBOL
                          --quote-token-address QUOTE_TOKEN_ADDRESS
                          [--report-time REPORT_TIME]
                          [--ro-account RO_ACCOUNT]

optional arguments:
  -h, --help            show this help message and exit
  --rpc-host RPC_HOST   JSON-RPC host (default: `localhost')
  --rpc-port RPC_PORT   JSON-RPC port (default: `8545')
  --rpc-timeout RPC_TIMEOUT
                        JSON-RPC timeout (in seconds, default: 10)
  --http-address HTTP_ADDRESS
                        Address of the Uniswap Price Feed
  --http-port HTTP_PORT
                        Port of the Uniswap Price Feed
  --base-exchange-address BASE_EXCHANGE_ADDRESS
                        Address of the Uniswap Exchange
  --base-token-symbol BASE_TOKEN_SYMBOL
                        Token symbol
  --base-token-address BASE_TOKEN_ADDRESS
                        Token address
  --quote-exchange-address QUOTE_EXCHANGE_ADDRESS
                        Address of the Quote Uniswap Exchange
  --quote-token-symbol QUOTE_TOKEN_SYMBOL
                        Quote Token symbol
  --quote-token-address QUOTE_TOKEN_ADDRESS
                        Quote Token address
  --report-time REPORT_TIME
                        Time interval to report price
  --ro-account RO_ACCOUNT
                        Credentials of the read-only user (format:
                        username:password)
```

Sample of running scripts
- ETH-DAI price feed (connect to `ws://user:readonly@localhost:7777/price/ETH-DAI/socket`)
```
bin/uniswap-price-feed \
    --quote-exchange-address 0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14 \
    --quote-token-symbol DAI \
    --quote-token-address 0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359 \
    --ro-account user:readonly
```

- MKR-DAI price feed (connect to `ws://user:readonly@localhost:7778/price/MKR-DAI/socket`):
```
bin/uniswap-price-feed \
    --base-exchange-address 0x2C4Bd064b998838076fa341A83d007FC2FA50957 \
    --base-token-symbol MKR \
    --base-token-address 0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2 \
    --quote-exchange-address 0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14 \
    --quote-token-symbol DAI \
    --quote-token-address 0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359 \
    --ro-account user:readonly \
    --http-port 7778 \
    --report-time 2
```

## API

The primary and only entity this service operates on is _feed_. Each feed is effectively a stream
of timestamped records. Timestamps never go back and it is always guaranteed that
new records will be added 'after' the existing ones. This simplification makes feed streams
consumption much easier for clients.

Each record is represented throughout the service as a JSON structure with two fields: `timestamp`
and `data`. The first one is a UNIX epoch timestamp represented as a number (either integer or floating-point).
The latter can be basically anything. Sample record may look as follows:
```json
{
    "data": {
        "price": 173.03457395327663
    },
    "timestamp": 1571747588
}
```

All endpoints require and support only HTTP Basic authentication. Only one type of credentials
is supported at the moment: (`--ro-account`) gives read-only access to
the feeds.


### `ws://<service-location>/price/<feed-name>/socket`

Opens a new socket subscription to a feed. Each new subscriber will immediately receive the last record
from the feed, and will be promptly sent any new records posted by producer(s). Subscribers
can assume that timestamps of records received over the WebSocket will always increase.

This is a receive-only WebSocket. Any messages sent by consumers to the service will be ignored.

