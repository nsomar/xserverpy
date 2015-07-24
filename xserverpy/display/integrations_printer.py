from xserverpy.utils.config import *
from tabulate import tabulate


class IntegrationsPrinter():

    def __init__(self, integrations):
        self.integrations = integrations

    def print_items(self):
        # print self.bots
        printed = map(self.prepare, self.integrations)
        print tabulate(printed, headers=['Number', 'ID', 'Step', 'Result', 'Date'])

    @staticmethod
    def prepare(integration):
        return [integration.number, integration.tiny_id,
                integration.step, integration.result,
                integration.date_string()]
