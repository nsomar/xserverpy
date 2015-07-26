import json
import os
from xserverpy.lib.xcode_server import XcodeServer
from xserverpy.lib.user import User


class Settings():

    def __init__(self, server, user):
        self.server = server
        self.user = user

    def update(self, server, user):
        if server.host:
            self.server.host = server.host
        if server.port:
            self.server.port = server.port
        if user.user:
            self.user.user = user.user
        if user.password:
            self.user.password = user.password

    @classmethod
    def load(cls, file_name="xserverpy"):
        settings = cls.load_file(False, file_name)
        if settings:
            return settings

        settings = cls.load_file(True, file_name)
        if settings:
            return settings

        return EmptySettings()

    @classmethod
    def load_file(cls, is_global, file_name):
        path = cls.storage_path(is_global, file_name)

        if os.path.exists(path):
            return cls.parse_file(path)

        return None

    @classmethod
    def storage_path(cls, is_global, file_name="xserverpy"):
        path = "." + file_name
        if is_global:
            path = os.path.expanduser("~/" + path)
        return path

    @classmethod
    def parse_file(cls, file_path):
        with open(file_path) as opened:
            j = json.loads(opened.read())
            u = User(**j["user"])
            s = XcodeServer(**j["server"])
            return Settings(s, u)

    def store(self, is_global, file_name="xserverpy"):
        to_store = {"user": self.user.__dict__, "server": self.server.__dict__}
        path = self.storage_path(is_global, file_name)
        with open(path, 'w') as outfile:
            json.dump(to_store, outfile, indent=4, separators=(',', ': '))

    def validate(self):
        if not self.server.host:
            raise RuntimeError("Host is not a URL, please past a valid host, examples:\n" +
                               "- http://10.55.55.50\n" +
                               "- https://10.55.55.50")

        if not self.server.port:
            raise RuntimeError("Port is missing")

    def is_empty():
        return False


class EmptySettings(Settings):

    def __init__(self):
        self.user = None
        self.server = None

    def is_empty():
        return True

    def update(self, server, user):
        self.user = user
        self.server = server
