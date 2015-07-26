from termcolor import colored
import sys

verbose = False
tty = True


def error(msg):
    print(colored(msg, "red"))


def warn(msg):
    print(colored(msg, "yellow"))


def success(msg):
    print(colored(msg, "green"))


def info(msg):
    print(msg)
