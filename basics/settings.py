import configparser

class Settings:

    def __init__(self, filename="config.ini"):
        config = configparser.RawConfigParser()
        config.read(filename)
        self.candle_time = config.getfloat("application", "candle_time")
        self.ticker = config.get("exchange", "ticker")
        self.mongo_uri = config.get("mongodb", "uri")
        self.mongo_port = int(config.get("mongodb", "port"))