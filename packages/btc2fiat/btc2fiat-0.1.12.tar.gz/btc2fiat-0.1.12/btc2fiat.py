#!/usr/bin/env python

import abc
import sys
import traceback

from requests import Request, Session

class Exchange(abc.ABC):
    @abc.abstractmethod
    def get_url(self, fiat_symbol):
        pass

    def build_request(self, fiat_symbol):
        return Request('GET', self.get_url(fiat_symbol))

    @abc.abstractmethod
    def get_value(self, response, fiat_symbol):
        pass

class Binance(Exchange):
    def get_url(self, fiat_symbol):
        shitcoin_symbol = (fiat_symbol + 'T') if fiat_symbol == 'USD' else fiat_symbol
        return f'https://api.binance.com/api/v3/avgPrice?symbol=BTC{shitcoin_symbol}'

    def get_value(self, response, fiat_symbol):
        return float(response.json()['price'])

class Coinbase(Exchange):
    def get_url(self, fiat_symbol):
        return f"https://api.coinbase.com/v2/prices/spot?currency={fiat_symbol}"

    def get_value(self, response, fiat_symbol):
        return float(response.json()['data']['amount'])

class Kraken(Exchange):
    def get_url(self, fiat_symbol):
        return f'https://api.kraken.com/0/public/Ticker?pair=XBT{fiat_symbol}'

    def get_value(self, response, fiat_symbol):
        return float(response.json()['result'][f'XXBTZ{fiat_symbol}']['c'][0])

EXCHANGES = {'binance': Binance, 'coinbase': Coinbase, 'kraken': Kraken}

def get_value(exchange=None, fiat_symbol=None):
    if exchange is None:
        exchange = 'kraken'
    if fiat_symbol is None:
        fiat_symbol = 'USD'

    exchange = EXCHANGES[exchange]()
    session = Session()
    request = exchange.build_request(fiat_symbol)
    prepared_request = session.prepare_request(request)
    response = session.send(prepared_request)

    return exchange.get_value(response, fiat_symbol)

if __name__ == '__main__':
    exchange = 'kraken'
    fiat_symbol = 'USD'

    USAGE = f"Usage: {sys.argv[0]} [binance|coinbase|kraken] [usd|eur]"

    if len(sys.argv) >= 2:
        exchange = sys.argv[1].lower()
    if len(sys.argv) >= 3:
        fiat_symbol = sys.argv[2].upper()
    if len(sys.argv) > 3:
        print(USAGE)
        sys.exit(1)

    print(get_value(exchange, fiat_symbol))
