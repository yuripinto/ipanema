import time
from threading import Thread
from exchanges import bitfinex
from pymongo import MongoClient
from time import gmtime, strftime
import numpy
import talib


class MarketWatcher(Thread):

    def __init__(self, settings):
        Thread.__init__(self)
        # Getting params
        self.ticker = settings.ticker
        self.candle_time = settings.candle_time
        self.mongo_uri = settings.mongo_uri
        self.mongo_port = settings.mongo_port
        # Connecting to database
        self.log("Connecting to MongoDB")
        self.client = MongoClient(self.mongo_uri, self.mongo_port)
        self.log("Preparing data")
        self.client.ipanema.history.drop()
        self.history = self.client.ipanema.history
        # Starting watcher
        self.log("MarketWatcher started")
        self.log("Candle time: " + str(self.candle_time) + "(s)")
        self.rsi = None
        #Loading trade api
        self.trade_api = bitfinex.TradeAPI(settings.public_key, settings.private_key, settings.verbose)

    def run(self):
        self.watch()

    def watch(self):
        while (True):
            try:
                # Getting ticket data
                response = bitfinex.Client.ticker(self.ticker)
                self.last = response['last']
                self.update_database()
                # Running strategy
                rsi = self.get_RSI()
                # Logging
                rsi_trend = "loading"
                if rsi > 0:
                    if rsi <= 30:
                        rsi_trend = "buy"
                    elif rsi >= 70:
                        rsi_trend = "sell"
                    else:
                        rsi_trend = "no_trend"
                self.log("(" + self.ticker + ") " + str(self.get_last()) + " (rsi) " + str(rsi) + " (rsi_trend) " + rsi_trend)
                # Trade
                self.trade(rsi_trend)
            except Exception as e:
                self.log("Failed to load ticker data: " + str(e))
            time.sleep(self.candle_time)

    def trade(self, trend):
        if trend != "no_trend":
            balance = self.trade_api.balance()
            if trend == "buy":
                pass
            elif trend == "sell":
                pass

    def get_last(self):
        return self.last

    def get_RSI(self):
        history = []
        for row in self.client.ipanema.history.find().limit(50):
            history.append(float(row['last_price']))
        history = numpy.asanyarray(history)
        output = talib.RSI(history, timeperiod=14)
        self.rsi = output[-1]
        return self.rsi

    def update_database(self):
        data = {
            "last_price": self.last,
            "ticker": self.ticker
        }
        self.history.insert_one(data)

    def log(self, output):
        time = "(" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ")"
        print(time + " " + output)

