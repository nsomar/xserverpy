from termcolor import colored
import os


global verbose
verbose = False
SAVED_DESCRIPTORS = None


def error(msg):
    print(colored(msg, "red"))


def warn(msg):
    print(colored(msg, "yellow"))


def success(msg):
    print(colored(msg, "green"))


def info(msg):
    print(msg)
