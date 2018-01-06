import ccxt


class PublicAPI(object):

    @staticmethod
    def ticker(ticker):
        bitfinex = ccxt.bitfinex()
        return bitfinex.fetch_ticker(ticker)


class TradeAPI():

    def __init__(self, public_key, private_key, verbose):
        self.client = ccxt.bitfinex({
            'apiKey': public_key,
            'secret': private_key,
            'verbose': verbose
        })

    def balance(self):
        return self.client.fetch_balance()

    def create_market_buy_order(self, ticker, amount):
        return self.client.create_market_buy_order(ticker, amount)

    def create_market_sell_order(self, ticker, amount):
        return self.client.create_market_sell_order(ticker, amount)

