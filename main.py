import time
from threading import Thread
from colorama import init, Fore
from exchanges import bitfinex
from pymongo import MongoClient
from time import gmtime, strftime
import numpy
import talib


CANDLE_TIME = 5
MONGO_URI = "localhost"
MONGO_PORT = 27017
TICKER = "btcusd"


class MarketWatcher(Thread):

    def __init__(self, ticker):
        Thread.__init__(self)
        self.ticker = ticker
        self.log("Connecting to MongoDB")
        self.client = MongoClient(MONGO_URI, MONGO_PORT)
        self.log("Preparing data")
        self.client.ipanema.history.drop()
        self.history = self.client.ipanema.history
        self.log("MarketWatcher started")
        self.log("Candle time: " + str(CANDLE_TIME) + "(s)")
        self.rsi = None

    def run(self):
        self.watch()

    def watch(self):
        while (True):
            try:
                response = bitfinex.Client.ticker(self.ticker)
                self.last = response['last_price']
                self.updateDatabase()
                rsi = self.getRSI()
                rsi_trend = "loading"
                if rsi > 0:
                    if rsi <= 30:
                        rsi_trend = "buy"
                    elif rsi >= 70:
                        rsi_trend = "sell"
                    else:
                        rsi_trend = "no trend"
                self.log("(" + self.ticker + ") " + self.getLast() + " (rsi) " + str(rsi) + " (rsi_trend) " + rsi_trend)
                time.sleep(CANDLE_TIME)
            except Exception as e:
                self.log("Failed to load ticker data: " + str(e))

    def getLast(self):
        return self.last

    def getRSI(self):
        history = []
        for row in self.client.ipanema.history.find().limit(50):
            history.append(float(row['last_price']))
        history = numpy.asanyarray(history)
        output = talib.RSI(history)
        self.rsi = output[-1]
        return self.rsi

    def updateDatabase(self):
        ticker = {
            "last_price": self.last,
            "ticker": self.ticker
        }
        return self.history.insert_one(ticker).inserted_id

    def log(self, output):
        time = "(" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ")"
        print(time + " " + output)


if __name__ == '__main__':
    logo = """ ______                                                          
/\__  _\                                                         
\/_/\ \/   _____      __      ___      __    ___ ___      __     
   \ \ \  /\ '__`\  /'__`\  /' _ `\  /'__`\/' __` __`\  /'__`\   
    \_\ \_\ \ \L\ \/\ \L\.\_/\ \/\ \/\  __//\ \/\ \/\ \/\ \L\.\_ 
    /\_____\ \ ,__/\ \__/.\_\ \_\ \_\ \____\ \_\ \_\ \_\ \__/.\_\
    
    \/_____/\ \ \/  \/__/\/_/\/_/\/_/\/____/\/_/\/_/\/_/\/__/\/_/
             \ \_\                                               
              \/_/                                               """
    init(autoreset=True)
    print(Fore.GREEN + logo)
    watcher = MarketWatcher(TICKER)
    watcher.start()
