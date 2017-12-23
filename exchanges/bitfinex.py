import requests

ENDPOINT = "https://api.bitfinex.com/v1/"
TIMEOUT = 5


class Client(object):

    @staticmethod
    def get(url):
        return requests.get(url, timeout=TIMEOUT).json()

    @staticmethod
    def ticker(symbol):
        # https://api.bitfinex.com/v1/pubticker/<symbol>
        return Client.get(ENDPOINT + "pubticker/" + symbol)

    @staticmethod
    def symbols():
        # https://api.bitfinex.com/v1/symbols
        return Client.get(ENDPOINT + "symbols")

    @staticmethod
    def orderbook(symbol):
        # https://api.bitfinex.com/v1/book/<symbol>
        return Client.get(ENDPOINT + "book/" + symbol)
