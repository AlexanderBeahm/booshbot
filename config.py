import os
import io
from configenum import ConfigEnum
import enum
class Config:
    def __init__(self):
        self.dictionary = self.__load__()

    def __load__(self):
        dictionary = {}
        with open('bot.config') as f:
            for config_line in f:
                split_entry = config_line.split("=")
                if len(split_entry) != 2:
                    raise Exception()
                dictionary[split_entry[0]] = split_entry[1]
        return dictionary

    def get_token(self):
        return self.dictionary[ConfigEnum.BOT_CLIENT.name]