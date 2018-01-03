import requests
import ccxt


ENDPOINT = "https://api.bitfinex.com/v1/"
TIMEOUT = 5


class Client(object):

    @staticmethod
    def ticker(ticker):
        bitfinex = ccxt.bitfinex()
        return bitfinex.fetch_ticker(ticker)
