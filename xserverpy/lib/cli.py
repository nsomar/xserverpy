# -*- coding: utf-8 -*-
import argparse
import sys

def parse(args=None):
    parser = argparse.ArgumentParser(
            description='Command line interface for Xcode server.')
    sub_parsers = parser.add_subparsers(title="Commands", dest="sub")

    parser.add_argument('--version', help="Display version", action="count")

    add_bot_parser(sub_parsers)
    add_integrate_parser(sub_parsers)
    add_init_flags(sub_parsers)

    if has_pre_parse(parser):
        return pre_parse()

    parsed_args = parser.parse_args(args)

    parsed_args.bots = parsed_args.sub == "bots"
    parsed_args.integrations = parsed_args.sub == "list"
    parsed_args.integrate = parsed_args.sub == "new"
    parsed_args.cancel = parsed_args.sub == "cancel"
    parsed_args.init = parsed_args.sub == "init"
    parsed_args.running = parsed_args.sub == "running"

    return parsed_args


def has_pre_parse(parser):
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    return sys.argv[1] == "--version"


def pre_parse():
    is_version = sys.argv[1] == "--version"

    if is_version:
        parsed_args = argparse.Namespace()
        parsed_args.version = True
        return parsed_args

    return None


def add_bot_parser(sub_parsers):
    help = "List Xcode server bots"
    parser = sub_parsers.add_parser("bots",
                                    help=help,
                                    description=help)
    add_common_flags(parser)


def add_integrate_parser(sub_parsers):
    help = "Handle Xcode server integrations"
    integration_parser = sub_parsers.add_parser("integrations",
                                                help=help,
                                                description=help)

    integration_sub_parsers = integration_parser.add_subparsers(title="Commands", dest="sub")
    add_new_integration_parser(integration_sub_parsers)
    add_list_integrations_parser(integration_sub_parsers)
    add_cancel_integration_parser(integration_sub_parsers)
    add_running_integrations_parser(integration_sub_parsers)


def add_new_integration_parser(integration_sub_parsers):
    help = "Integrate an Xcode bot"
    new_subparser = integration_sub_parsers.add_parser("new",
                                                       help=help,
                                                       description=help)

    add_common_flags(new_subparser)
    new_subparser.add_argument('--bot', help="Bot to integrate",
                               action="store", required=True)
    new_subparser.add_argument('--interval',
                               help="Interval to poll the server for updates, default .5s",
                               action="store", type=int, default=.5)
    new_subparser.add_argument('--wait', help="Print integration steps progress",
                               action="store_true", default=False)
    new_subparser.add_argument('--no-tty', help="Force non tty progress reporting",
                               action="store_false", default=sys.stdout.isatty())


def add_list_integrations_parser(integration_sub_parsers):
    help = "List Xcode server integrations"
    list_parser = integration_sub_parsers.add_parser("list",
                                                     help=help,
                                                     description=help)
    add_common_flags(list_parser)
    list_parser.add_argument('--bot', help="Bot to list integrations for",
                             action="store", default=None)


def add_cancel_integration_parser(integration_sub_parsers):
    help = "Cancel a previos integration"
    cancel_subparser = integration_sub_parsers.add_parser("cancel",
                                                          help=help,
                                                          description=help)

    add_common_flags(cancel_subparser)
    cancel_subparser.add_argument('--id', help="Integration ID to cancel",
                                  action="store", required=True)


def add_running_integrations_parser(integration_sub_parsers):
    help = "List running integrations"
    list_parser = integration_sub_parsers.add_parser("running",
                                                     help=help,
                                                     description=help)
    add_common_flags(list_parser)


def add_common_flags(parser):
    parser.add_argument('--host', help="Xcode server host",
                        action="store", default=None)
    parser.add_argument('--port', help="Xcode server host port, default 443",
                        action="store", default=443)
    parser.add_argument('--user', help="Username to use for authentication",
                        action="store", default=None)
    parser.add_argument('--password', help="Password to use for authentication",
                        action="store", default=None)


def add_init_flags(parser):
    help = "Setup user environment to be used with consequent commands"
    parser = parser.add_parser("init",
                               help=help,
                               description=help)

    parser.add_argument('--host', help="Xcode server host",
                        action="store", required=True)
    parser.add_argument('--port', help="Xcode server host port, default 443",
                        action="store", default=443)
    parser.add_argument('--user', help="Username to use for authentication",
                        action="store", default=None)
    parser.add_argument('--password', help="Password to use for authentication",
                        action="store", default=None)
    parser.add_argument('--local', help="Store configuration file in the local directory",
                        action="store_true", default=False)
