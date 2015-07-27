import time
from xserverpy.utils.porgress import Progress
from xserverpy.utils.config import *
from xserverpy.utils import config


class IntegrationWatcher():

    def __init__(self, integrations_service, integration, interval):
        self.integration = integration
        self.integrations_service = integrations_service
        self.progress = Progress()
        self.interval = interval

    def watch(self):
        self.handle_pending()

        previous_step = None
        while not self.integration.is_complete():
            self.integration = self.integrations_service.get_item(self.integration.id)

            if self.integration.is_complete():
                    break

            if previous_step != self.integration.step:
                previous_step = self.integration.step
                self.progress.increment("- Performing step: %s" % self.integration.step)

            self.progress.step()
            time.sleep(self.interval)

        self.progress.done()
        print ("")
        return self.print_integration_result(self.integration)

    def handle_pending(self):
        if self.integration.is_pending():
            self.progress.increment("- Pending for integration")

        self.previos_bot = None
        while self.integration.is_pending():
            self.print_running()

            self.integration = self.integrations_service.get_item(self.integration.id)
            time.sleep(self.interval * 3)

    def print_running(self):
        integrations = self.integrations_service.get_running_integration()

        is_the_only_pending = len(integrations) == 0 or integrations[0].id == self.integration.id
        if is_the_only_pending:
            self.progress.step()
            return

        bot_name = integrations[0].bot.name
        if self.previos_bot == bot_name:
            pass
        else:
            self.previos_bot = bot_name
            if config.tty:
                sys.stdout.write("\r")
                sys.stdout.write("\033[K")
                sys.stdout.write("Waiting for bot '%s' to finish integrating" % bot_name)
                sys.stdout.flush()
                print("")
            else:
                self.progress.increment("Waiting for bot '%s' to finish integrating" %
                                        bot_name, prefix="")

        self.progress.step()

    def print_integration_result(self, integration):
        if integration.succeeded():
            success("Integration number '%s' for bot '%s' completed successfully" %
                    (integration.number, integration.bot.name))

            result = True
        elif integration.completed_with_warnings():
            warn("Integration number '%s' for bot '%s' completed with warnings" %
                (integration.number, integration.bot.name))
            result = True
        else:
            error("Integration number '%s' for bot '%s' failed with result '%s'" %
                  (integration.number, integration.bot.name, integration.result))
            result = False

        info("Integration ID '%s" % integration.id)
        return result
