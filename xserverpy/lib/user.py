import requests


class User():

    def __init__(self, user=None, password=None):
        self.user = user
        self.password = password

    def basic_auth(self):
        if self.user and self.password:
            return requests.auth.HTTPBasicAuth(self.user,
                                               self.password)
        else:
            return None
