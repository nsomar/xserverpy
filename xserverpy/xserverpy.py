# -*- coding: utf-8 -*-

from lib.cli import parse
from display.bots_printer import BotsPrinter
from display.integrations_printer import IntegrationsPrinter
from lib.xcode_server import XcodeServer
from lib.user import User
from lib.bots import Bots
from utils.settings import Settings
from lib.integration_watcher import IntegrationWatcher
from lib.integrations import Integrations
from utils.config import *
from utils import version
import sys
from utils import config


def start():
    reload(sys)
    sys.setdefaultencoding('utf8')
    start_with_args(None)


def start_with_args(params):
    args = parse(params)

    if args.version:
        print_version()

    # try:
    if args.bots:
        handle_bots(args)

    if args.integrations:
        handle_integrations(args)

    if args.cancel:
        handle_cancel(args)

    if args.integrate:
        handle_integrate(args)

    if args.init:
        handle_init(args)

    if args.running:
        handle_running(args)

    # except Exception as e:
    #     error(e)


def print_version():
    info(version.VERSION_STRING)
    sys.exit(0)


def handle_bots(args):
    settings = get_updated_settings(args)
    b = Bots(settings)
    printer = BotsPrinter(b.get_all())
    printer.print_items()


def handle_integrations(args):
    settings = get_updated_settings(args)

    bot_id = None
    if args.bot:
        bot_id = get_bot(settings, args).id

    integrations = Integrations(settings, bot_id=bot_id)
    IntegrationsPrinter.print_integrations(integrations.get_all())


def handle_integrate(args):
    settings = get_updated_settings(args)
    bot = get_bot(settings, args)

    config.tty = args.no_tty

    integrations_service = Integrations(settings, bot_id=bot.id)
    integration = integrations_service.integrate()

    if args.wait:
        add_watcher(integrations_service, integration, bot.name, args.interval)
    else:
        success("Integration number '%s' for bot '%s' posted successfully" %
                (integration.number, bot.name))
        info("Integration ID '%s" % integration.id)


def handle_cancel(args):
    settings = get_updated_settings(args)
    integrations_service = Integrations(settings)
    result = integrations_service.cancel_integration(args.id)

    if result:
        success("Integration with id '%s' cancelled successfully" % args.id)
    else:
        error("Failed to cancel integration with id '%s'" % args.id)


def handle_init(args):
    settings = get_settings(args)
    settings.store(not args.local)
    path = Settings.storage_path(not args.local)
    success("Settings saved successfully to '%s'" % path)


def handle_running(args):
    settings = get_updated_settings(args)
    integrations_service = Integrations(settings)
    IntegrationsPrinter.print_running(integrations_service.get_running_integration())


def add_watcher(integrations_service, integration, bot_name, interval):
    success("Integration number '%s' for bot '%s' started" %
            (integration.number, bot_name))
    info("Integration ID '%s" % integration.id)

    watcher = IntegrationWatcher(integrations_service, integration, interval)
    if watcher.watch():
        exit(0)
    else:
        exit(1)


def get_settings(args):
    u = User(user=args.user, password=args.password)
    s = XcodeServer(host=args.host, port=args.port)
    return Settings(s, u)


def get_updated_settings(args):
    settings = Settings.load()
    u = User(user=args.user, password=args.password)
    s = XcodeServer(host=args.host, port=args.port)
    settings.update(s, u)
    settings.validate()
    return settings


def get_bot(settings, args):
    bots_service = Bots(settings)

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
        return len(string) > 30
    except:
        return False
