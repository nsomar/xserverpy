from termcolor import colored
import sys

verbose = False
tty = True


def colored_if_needed(msg, color):
    if tty:
        return colored(msg, color)
    else:
        return msg


def error(msg):
    print(colored_if_needed(msg, "red"))


def warn(msg):
    print(colored_if_needed(msg, "yellow"))


def success(msg):
    print(colored_if_needed(msg, "green"))


def info(msg):
    print(msg)
