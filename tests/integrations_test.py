import unittest
import vcr
from xserverpy.lib.integrations import Integrations
from xserverpy.lib.xcode_server import XcodeServer
from xserverpy.lib.user import User
from xserverpy.utils.settings import Settings


class TestIntegrations(unittest.TestCase):

    def setUp(self):
        user = User(user="aa", password="pass")
        server = XcodeServer(host="https://127.0.0.1")
        self.settings = Settings(server, user)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integrations.yaml')
    def test_can_request_integrations(self):
        b = Integrations(self.settings, "88c98ee21f3895749ec3888b930017be")
        assert len(b.get_all()) == 4

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integration.yaml')
    def test_can_request_1_integration(self):
        b = Integrations(self.settings, "88c98ee21f3895749ec3888b930017be")
        self.assertEqual(b.get_item(item_id="88c98ee21f3895749ec3888b93009ea3").result,
                         "succeeded")

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integration_new.yaml')
    def test_can_request_new_integration(self):
        b = Integrations(self.settings, "88c98ee21f3895749ec3888b930017be")
        self.assertIsNotNone(b.integrate())

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integration_cancel.yaml')
    def test_can_cancel_integration(self):
        i = Integrations(self.settings, "88c98ee21f3895749ec3888b930017be")
        integration = i.integrate()
        self.assertIsNotNone(integration)
        result = i.cancel_integration(integration.id)
        self.assertTrue(result)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integration_running.yaml')
    def test_can_request_running_integration(self):
        b = Integrations(self.settings)
        running = b.get_running_integration()
        self.assertIsNotNone(running)
        self.assertEqual(running[0].bot.name, "Testbots Bot")
