import unittest
import os
from xserverpy.utils.settings import Settings, EmptySettings
import glob
import shutil
from mock import MagicMock


class SettingsTests(unittest.TestCase):

    def setUp(self):
        self.f = ".xserverpy.test"
        try:
            os.remove(".test_xserverpy")
        except: pass

        try:
            os.remove(os.path.expanduser("~/.test_xserverpy"))
        except: pass

    def test_can_save_to_local_file(self):

        server = MagicMock()
        server.__dict__ = {"host": "123123", "port": "8080"}

        user = MagicMock()
        user.__dict__ = {"user": "testuser", "password": "password"}

        self.assertEqual(os.path.exists(".test_xserverpy"), False)
        settings = Settings(server, user)
        settings.store(False, "test_xserverpy")
        self.assertEqual(os.path.exists(".test_xserverpy"), True)

    def test_can_save_to_global_file(self):

        server = MagicMock()
        server.__dict__ = {"host": "123123", "port": "8080"}

        user = MagicMock()
        user.__dict__ = {"user": "testuser", "password": "password"}

        path = os.path.expanduser("~/.test_xserverpy")
        self.assertEqual(os.path.exists(path), False)
        settings = Settings(server, user)
        settings.store(True, "test_xserverpy")
        self.assertEqual(os.path.exists(path), True)

    def test_can_load_from_global_file(self):
        self.dummy_store(True)
        path = os.path.expanduser("~/.test_xserverpy")
        self.assertEqual(os.path.exists(path), True)
        self.assertEqual(os.path.exists(".test_xserverpy"), False)

        settings = Settings.load("test_xserverpy")
        self.assertEqual(settings.server.host, "http://1.2.2.2/xcode/api")
        self.assertEqual(settings.server.port, "8080")
        self.assertEqual(settings.user.user, "testuser")
        self.assertEqual(settings.user.password, "password")

    def test_can_load_from_local_file(self):
        self.dummy_store(False)
        path = os.path.expanduser("~/.test_xserverpy")
        self.assertEqual(os.path.exists(path), False)
        self.assertEqual(os.path.exists(".test_xserverpy"), True)

        settings = Settings.load("test_xserverpy")
        self.assertEqual(settings.server.host, "http://1.2.2.2/xcode/api")
        self.assertEqual(settings.server.port, "8080")
        self.assertEqual(settings.user.user, "testuser")
        self.assertEqual(settings.user.password, "password")

    def test_returns_none_if_no_file(self):
        path = os.path.expanduser("~/.test_xserverpy")
        self.assertEqual(os.path.exists(path), False)
        self.assertEqual(os.path.exists(".test_xserverpy"), False)

        settings = Settings.load("test_xserverpy")
        self.assertIsInstance(settings, EmptySettings)

    def test_can_updated_an_empty_with_user_and_server(self):
        settings = EmptySettings()
        self.assertIsNone(settings.server)
        self.assertIsNone(settings.user)
        settings.update(MagicMock(), MagicMock())
        self.assertIsNotNone(settings.server)
        self.assertIsNotNone(settings.user)

    def test_validates_correctly(self):
        server = MagicMock()
        server.__dict__ = {"host": None, "port": "80820"}

        user = MagicMock()
        user.__dict__ = {"user": "testuser2", "password": "2222"}
        settings = Settings(server, user)

        with self.assertRaises(RuntimeError):
            settings.validate()

        server = MagicMock()
        server.__dict__ = {"host": "http://1.2.2.2/xcode/api", "port": None}
        settings.server = server
        with self.assertRaises(RuntimeError):
            settings.validate()

    def test_can_updated_a_non_empty_with_user_and_server(self):
        self.dummy_store(False)
        path = os.path.expanduser("~/.test_xserverpy")
        self.assertEqual(os.path.exists(path), False)
        self.assertEqual(os.path.exists(".test_xserverpy"), True)

        settings = Settings.load("test_xserverpy")
        self.assertEqual(settings.server.host, "http://1.2.2.2/xcode/api")
        self.assertEqual(settings.server.port, "8080")
        self.assertEqual(settings.user.user, "testuser")
        self.assertEqual(settings.user.password, "password")

        server = MagicMock()
        server.__dict__ = {"host": "http://1.2.2.4/xcode/api", "port": "80820"}

        user = MagicMock()
        user.__dict__ = {"user": "testuser2", "password": "2222"}
        settings.update(server, user)
        self.assertEqual(settings.server.host, "http://1.2.2.4/xcode/api")
        self.assertEqual(settings.server.port, "80820")
        self.assertEqual(settings.user.user, "testuser2")
        self.assertEqual(settings.user.password, "2222")

        # If value is none, dont overwrite it
        server = MagicMock()
        server.__dict__ = {"host": None, "port": None}

        user = MagicMock()
        user.__dict__ = {"user": "testuser2", "password": "2222"}
        settings.update(server, user)
        self.assertEqual(settings.server.host, "http://1.2.2.4/xcode/api")
        self.assertEqual(settings.server.port, "80820")
        self.assertEqual(settings.user.user, "testuser2")
        self.assertEqual(settings.user.password, "2222")

    def dummy_store(self, is_global):
        server = MagicMock()
        server.__dict__ = {"host": "http://1.2.2.2/xcode/api", "port": "8080"}

        user = MagicMock()
        user.__dict__ = {"user": "testuser", "password": "password"}
        settings = Settings(server, user)
        settings.store(is_global, "test_xserverpy")
