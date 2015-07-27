# -*- coding: utf-8 -*-
import re

PORT = 443


class XcodeServer(object):

    def __init__(self, host=None, port=PORT):
        self.host = host
        self.port = port

        self.validate()

    def validate(self):
        if not self.host:
            return

        if not self.url_validate():
            raise RuntimeError("Host is not a URL, please past a valid host, examples:\n" +
                               "- http://10.55.55.50\n" +
                               "- https://10.55.55.50")

        if "/xcode/api" not in self.host:
            self.host = self.host + "/xcode/api"

    def url_validate(self):
        regex = re.compile( r'^(?:http|ftp)s?://'
                            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                            r'localhost|' #localhost...
                            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                            r'(?::\d+)?' # optional port
                            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return regex.match(self.host)
