#!/bin/bash

bin/uniswap-price-feed \
    --quote-exchange-address 0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14 \
    --quote-token-symbol DAI \
    --quote-token-address 0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359 \
    --ro-account user:readonly \
    --rw-account user:readwrite \
    $@ 2> >(tee -a /home/george/grandizzy/uniswap-price-feed/uniswap.log >&2)