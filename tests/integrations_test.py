import unittest
import vcr
from xserverpy.lib.integrations import Integrations
from xserverpy.lib.xcode_server import XcodeServer


class TestIntegrations(unittest.TestCase):

    def setUp(self):
        self.server = XcodeServer(host="https://127.0.0.1", user="aa", password="pass")

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integrations.yaml')
    def test_can_request_integrations(self):
        b = Integrations(self.server, "88c98ee21f3895749ec3888b930017be")
        assert len(b.get_all()) == 4

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integration.yaml')
    def test_can_request_1_integration(self):
        b = Integrations(self.server, "88c98ee21f3895749ec3888b930017be")
        self.assertEqual(b.get_item(item_id="88c98ee21f3895749ec3888b93009ea3").result,
                         "succeeded")

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/integration_new.yaml')
    def test_can_request_new_integration(self):
        b = Integrations(self.server, "88c98ee21f3895749ec3888b930017be")
        self.assertIsNotNone(b.integrate())
