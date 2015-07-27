# -*- coding: utf-8 -*-

from bot import Bot
from base_service import BaseService
import itertools
import sys


class Bots(BaseService):

    def endpoint(self):
        return "bots"

    def singe_item_endpoint(self, bot_id):
        return "bots/%s" % bot_id

    def item_class(self):
        return Bot

    def get_named(self, bot_name):
        bots = self.get_all()
        try:
            return list(itertools.ifilter(lambda x: x.name == bot_name, bots))[0]
        except:
            return None
