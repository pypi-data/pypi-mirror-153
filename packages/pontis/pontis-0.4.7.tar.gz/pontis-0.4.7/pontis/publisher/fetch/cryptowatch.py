import datetime
import os
import re
from pontis.core.utils import currency_pair_to_key

import requests
from pontis.core.entry import construct_entry


def fetch_binance(assets):
    PUBLISHER_PREFIX = os.environ.get("PUBLISHER_PREFIX")
    publisher = PUBLISHER_PREFIX + "-cryptowatch-coinbase-pro"

    response = requests.get("https://api.cryptowat.ch/markets/coinbase-pro", timeout=20)

    entries = []

    for asset in assets:
        if asset["type"] != "SPOT":
            print(f"Skipping Cryptowatch for non-spot asset {asset}")
            continue

        pair = asset["pair"]
        result = [e for e in response.json()["result"] if e["pair"] == "".join(pair)]
        if len(result) == 0:
            print(f"No entry found for {key} from Cryptowatch")
            continue

        assert (
            len(result) == 1
        ), f"Found more than one matching entries for Cryptowatch response and price pair {pair}"

        result = response.json()

        timestamp = int(result["timestamp"])
        price = float(result["last"])
        price_int = int(price * (10 ** asset["decimals"]))
        key = currency_pair_to_key(*pair)

        print(f"Fetched price {price} for {'/'.join(pair)} from Bitstamp")

        entries.append(
            construct_entry(
                key=key,
                value=price_int,
                timestamp=timestamp,
                publisher=publisher,
            )
        )

    return entries
