from colorama import init, Fore
from basics.financial import MarketWatcher
from basics.settings import Settings


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
    settings = Settings()
    watcher = MarketWatcher(settings.ticker, settings.candle_time, settings.mongo_uri, settings.mongo_port)
    watcher.start()
