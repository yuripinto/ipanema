import time
from threading import Thread
from colorama import init, Back
from exchanges import bitfinex

CANDLE_TIME = 5


class MarketWatcher(Thread):

    def __init__(self, ticker):
        Thread.__init__(self)
        self.ticker = ticker

    def run(self):
        self.watch()

    def watch(self):
        while (True):
            response = bitfinex.Client.ticker(self.ticker)
            print(response['last_price'])
            time.sleep(CANDLE_TIME)

    def updateDatabase(self):
        # todo - Add sqlite scripts
        pass


if __name__ == '__main__':
    init(autoreset=True)
    watcher = MarketWatcher("btcusd")
    watcher.start()

