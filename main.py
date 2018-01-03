from colorama import init, Fore
from basics import financial

CANDLE_TIME = 60
MONGO_URI = "localhost"
MONGO_PORT = 27017
TICKER = "BTC/USD"

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
    watcher = financial.MarketWatcher(TICKER, CANDLE_TIME, MONGO_URI, MONGO_PORT)
    watcher.start()
