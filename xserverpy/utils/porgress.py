from config import *
import sys


class Progress():

    def __init__(self):
        self.step_counter = -1
        self.steps_done = 0

    def is_tty(self):
        return sys.stdout.isatty()

    def increment(self, title):
        self.step_counter = -1
        if self.steps_done > 0:
            if self.is_tty():
                success('\b\bDone ')
            else:
                success(' Done ')

        print("\n%s" % title)

        if self.is_tty():
            print 'Loading....  ',
        else:
            print 'Loading.',

        self.steps_done += 1

    def done(self):
        if self.is_tty() and self.steps_done > 0:
            success('\b\b Done ')
        else:
            success(' Done ')

    def step(self):
        if self.is_tty():
            self.progress()
        else:
            if self.step_counter % 4 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()

        self.step_counter += 1

    def progress(self):
        if (self.step_counter % 4) == 0:
            sys.stdout.write('\b\b\b / ')
        elif (self.step_counter % 4) == 1:
            sys.stdout.write('\b\b\b - ')
        elif (self.step_counter % 4) == 2:
            sys.stdout.write('\b\b\b \\ ')
        elif (self.step_counter % 4) == 3:
            sys.stdout.write('\b\b\b | ')

        sys.stdout.flush()
