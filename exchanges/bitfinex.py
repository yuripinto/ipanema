import ccxt


class Client(object):

    @staticmethod
    def ticker(ticker):
        bitfinex = ccxt.bitfinex()
        return bitfinex.fetch_ticker(ticker)


class TradeAPI():

    def __init__(self, public_key, private_key, verbose):
        self.client = ccxt.bitfinex2({
            'apiKey': public_key,
            'secret': private_key,
            'verbose': verbose
        })

    def balance(self):
        return self.client.fetch_balance()

