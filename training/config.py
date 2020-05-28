from configparser import SafeConfigParser

class Config:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Config.__instance == None:
            Config()
        return Config.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Config.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.parser = SafeConfigParser()
            self.parser.read('config.ini')
            Config.__instance = self
        
    def get(self, key):
        return self.parser.get("DEFAULT", key)