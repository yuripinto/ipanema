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
    watcher = MarketWatcher(Settings())
    watcher.start()
