from config import *
import sys
import config


class Progress():

    def __init__(self):
        self.steps_done = 0

    def increment(self, title=None, prefix="\n"):
        self.print_done_if_needed()
        self.step_counter = 0

        if title:
            print("%s%s" % (prefix, title))

        self.steps_done += 1

    def print_done_if_needed(self):
        if self.steps_done > 0 and self.step_counter > 0:
            if config.tty:
                success('\b\bDone ')
            else:
                success(' Done ')

    def done(self):
        if config.tty and self.steps_done > 0:
            success('\b\bDone ')
        else:
            success(' Done ')

    def step(self):
        if self.step_counter == 0 and not config.tty:
            print 'Loading.',

        if config.tty:
            self.progress()
        else:
            sys.stdout.write('.')
            sys.stdout.flush()

        self.step_counter += 1

    def progress(self):
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write('Loading.... ')

        if (self.step_counter % 4) == 0:
            sys.stdout.write('/ ')
        elif (self.step_counter % 4) == 1:
            sys.stdout.write('- ')
        elif (self.step_counter % 4) == 2:
            sys.stdout.write('\\ ')
        elif (self.step_counter % 4) == 3:
            sys.stdout.write('| ')

        sys.stdout.flush()
