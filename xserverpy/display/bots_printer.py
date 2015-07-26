# -*- coding: utf-8 -*-

from xserverpy.utils.config import *
from tabulate import tabulate


class BotsPrinter():

    def __init__(self, bots):
        self.bots = bots

    def print_items(self):
        # print self.bots
        printed = map(self.prepare, self.bots)
        print tabulate(printed, headers=['Bot name', 'ID', 'Number of integrations'])

    @staticmethod
    def prepare(bot):
        return [bot.name, bot.id, bot.integration_counter - 1]
