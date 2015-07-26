from xserverpy.utils.config import *
from tabulate import tabulate


class IntegrationsPrinter():

    @classmethod
    def print_integrations(cls, integrations):
        printed = map(cls.prepare, integrations)

        if len(integrations) == 0:
            info("Selected bot has 0 integrations")
            return

        info("\nListing all integrations for bot '%s'" % integrations[0].bot.name)
        print tabulate(printed, headers=['Bot', 'Number', 'ID', 'Step', 'Result', 'Date'])

    @classmethod
    def print_running(cls, integrations):
        if integrations is None:
            return

        info("%d Integrations running currently" % len(integrations))

        if len(integrations) == 0:
            return

        print("")
        printed = map(cls.prepare, integrations)
        print tabulate(printed, headers=['Bot', 'Number', 'ID', 'Step', 'Result', 'Date'])

    @classmethod
    def prepare(cls, integration):
        return [integration.bot.name, integration.number, integration.tiny_id,
                integration.step, integration.result,
                integration.date_string()]
