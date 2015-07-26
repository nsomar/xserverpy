import unittest
import vcr
from xserverpy.lib.bots import Bots
from xserverpy.lib.xcode_server import XcodeServer
from xserverpy.lib.user import User
from xserverpy.utils.settings import Settings


class TestBots(unittest.TestCase):

    def setUp(self):
        user = User(user="aa", password="pass")
        server = XcodeServer(host="https://127.0.0.1")
        self.settings = Settings(server, user)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/bots.yaml')
    def test_can_request_bots(self):
        b = Bots(self.settings)
        assert len(b.get_all()) == 1

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/bot.yaml')
    def test_can_request_1_bot(self):
        b = Bots(self.settings)
        item = b.get_item(item_id="88c98ee21f3895749ec3888b930017be")
        self.assertEqual(item.name, "Testbots Bot")

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/bots.yaml')
    def test_can_request_bots_with_name(self):
        b = Bots(self.settings)
        bot = b.get_named("Testbots Bot")
        self.assertIsNotNone(bot)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/bots.yaml')
    def test_returns_none_if_not_found(self):
        b = Bots(self.settings)
        bot = b.get_named("sss")
        self.assertIsNone(bot)
