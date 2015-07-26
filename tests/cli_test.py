import unittest
import vcr
from xserverpy.lib.cli import parse
from xserverpy.xserverpy import start_with_args
from cStringIO import StringIO
import sys


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


class CliTests(unittest.TestCase):

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/bdd_integrations.yaml')
    def test_can_list_integrations(self):
        args = ["integrations", "list",
                "--host", "https://127.0.0.1",
                "--bot", 'Testbots Bot',
                "--user", 'Omar Abdelhafith',
                "--pass", "omaromar123"]

        sys.argv = args
        out = ""
        with Capturing() as output:
            start_with_args(args)
            out = output

        self.assertIn("Listing all integrations for bot 'Testbots Bot'", out)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/bdd_new_integration.yaml')
    def test_can_create_integration(self):
        args = ["integrations", "new",
                "--host", "https://127.0.0.1",
                "--bot", 'Testbots Bot',
                "--user", 'Omar Abdelhafith',
                "--pass", "omaromar123"]

        sys.argv = args
        out = ""
        with Capturing() as output:
            start_with_args(args)
            out = output

        self.assertIn("Integration number '142' for bot 'Testbots Bot' posted successfully", out)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/bdd_bots.yaml')
    def test_can_list_bots(self):
        args = ["bots",
                "--host", "https://127.0.0.1",
                "--user", 'Omar Abdelhafith',
                "--pass", "omaromar123"]

        sys.argv = args
        out = ""
        with Capturing() as output:
            start_with_args(args)
            out = output

        self.assertIn("Testbots Bot  88c98ee21f3895749ec3888b930017be" +
                      "                       139", out)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integration_running.yaml')
    def test_can_list_running_integrations(self):
        args = ["integrations", "running",
                "--host", "https://127.0.0.1",
                "--user", 'Omar Abdelhafith',
                "--pass", "omaromar123"]

        sys.argv = args
        out = ""
        with Capturing() as output:
            start_with_args(args)
            out = output

        self.assertIn("1 Integrations running currently", out)
