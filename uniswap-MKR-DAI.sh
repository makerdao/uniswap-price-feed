#!/bin/bash

bin/uniswap-price-feed \
    --base-exchange-address 0x2C4Bd064b998838076fa341A83d007FC2FA50957 \
    --base-token-symbol MKR \
    --base-token-address 0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2 \
    --quote-exchange-address 0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14 \
    --quote-token-symbol DAI \
    --quote-token-address 0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359 \
    --ro-account user:readonly \
    --rw-account user:readwrite \
    --http-port 7778 \
    --report-time 2
