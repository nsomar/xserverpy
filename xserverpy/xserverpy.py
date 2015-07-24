# -*- coding: utf-8 -*-
from lib.cli import parse
from display.bots_printer import BotsPrinter
from display.integrations_printer import IntegrationsPrinter
from lib.xcode_server import XcodeServer
from lib.bots import Bots
from lib.integration_watcher import IntegrationWatcher
from lib.integrations import Integrations
from utils.config import *
from utils import version
import sys


def start():
    args = parse()

    if args.version:
        print_version()

    if args.bots:
        handle_bots(args)

    if args.integrations:
        handle_integrations(args)

    if args.integrate:
        handle_integrate(args)


def print_version():
    info(version.VERSION_STRING)
    sys.exit(0)


def handle_bots(args):
    try:
        s = XcodeServer(host=args.host, port=args.port, user=args.user, password=args.password)
        b = Bots(s)
        printer = BotsPrinter(b.get_all())
        printer.print_items()
    except Exception as e:
        error(e)


def handle_integrations(args):
    try:
        server = XcodeServer(host=args.host, port=args.port, user=args.user, password=args.password)
        bot = get_bot(server, args)

        integrations = Integrations(server, bot_id=bot.id)
        printer = IntegrationsPrinter(integrations.get_all())
        info("\nListing all integrations for bot '%s'" % bot.name)
        printer.print_items()
    except Exception as e:
        error(e)


def handle_integrate(args):
    try:
        server = XcodeServer(host=args.host, port=args.port, user=args.user, password=args.password)
        bot = get_bot(server, args)
        integrations_service = Integrations(server, bot_id=bot.id)
        integration = integrations_service.integrate()

        if args.watch:
            add_watcher(integrations_service, integration, bot.name)
        else:
            success("Integration number '%s' for bot '%s' posted successfully" %
                    (integration.number, bot.name))
            info("Integration ID '%s" % integration.id)

    except Exception as e:
        error(e)


def add_watcher(integrations_service, integration, bot_name):
    success("Integration number '%s' for bot '%s' started" %
            (integration.number, bot_name))
    info("Integration ID '%s" % integration.id)

    watcher = IntegrationWatcher(integrations_service, integration)
    watcher.watch()
    success("Integration number '%s' for bot '%s' posted successfully" %
            (integration.number, bot_name))
    info("Integration ID '%s" % integration.id)


def get_bot(server, args):
    bots_service = Bots(server)

    method_name = ["get_named", "get_item"][is_id(args.bot)]
    method = getattr(bots_service, method_name, None)
    bot = method(args.bot)

    if not bot:
        name_or_id = ["with name", "with id"][is_id(args.bot)]
        raise RuntimeError("Bot %s '%s' cannot be found" % (name_or_id, args.bot))

    return bot


def is_id(string):
    try:
        int(string, 16)
        return True
    except:
        return False
