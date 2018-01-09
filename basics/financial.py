import time
from threading import Thread
from exchanges import api
import pymongo
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
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, self.mongo_port, serverSelectionTimeoutMS = 5)
            self.client.ipanema.history.drop()
            self.history = self.client.ipanema.history
        except:
            self.log("Failed to setup MongoDB. Please set connection on config.ini and start service.")
            exit()
        # Starting watcher
        self.log("MarketWatcher started")
        self.log("Candle time: " + str(self.candle_time / 60) + "(m)")
        self.rsi = None
        # Loading trade api
        self.trade_api = api.TradeAPI(settings.public_key, settings.private_key, settings.verbose)

    def run(self):
        self.watch()

    def watch(self):
        while (True):
            try:
                # Getting ticket data
                response = api.PublicAPI.ticker(self.ticker)
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
        balance = self.trade_api.balance()
        if trend != "no_trend":
            last = self.get_last()
            #todo adjust this hardcoded params
            money = 0
            coins = 0
            try:
                money = balance["total"]["USD"]
            except Exception as err:
                self.log("Not found money info. Setting to 0")
            try:
                coins = balance["total"]["BTC"]
            except Exception as err:
                self.log("Not found coins info. Setting to 0")
            if trend == "buy":
                if money < 100:
                    self.log("Insufficient money to buy")
                else:
                    # Calculate coins amount to buy
                    self.log("Sending a buy order")
                    amount = money / last
                    self.trade_api.create_limit_buy_order(self.ticker, amount, self.get_last())
            elif trend == "sell":
                if (coins * last) < 100:
                    self.log("Insufficient coins to sell")
                else:
                    # Sell all coins
                    self.log("Sending a sell order")
                    self.trade_api.create_limit_sell_order(self.ticker, coins, self.get_last())

    def get_last(self):
        return self.last

    def get_RSI(self):
        history = []
        try:
            for row in self.client.ipanema.history.find().sort('_id', pymongo.DESCENDING).limit(15):
                history.insert(0, float(row['last_price']))
        except Exception as err:
            print(err)
        history = numpy.asanyarray(history)
        output = talib.RSI(history, timeperiod=14)
        self.rsi = output[-1]
        return self.rsi

    def update_database(self):
        data = {
            "last_price": self.last,
            "ticker": self.ticker,
            "time": time.time()
        }
        self.history.insert_one(data)

    def log(self, output):
        time = "(" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ")"
        print(time + " " + output)

