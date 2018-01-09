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

    def create_limit_buy_order(self, ticker, amount, limit):
        return self.client.create_limit_buy_order(ticker, amount, limit)

    def create_limit_sell_order(self, ticker, amount, limit):
        return self.client.create_limit_buy_order(ticker, amount, limit)

