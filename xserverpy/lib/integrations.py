from integration import Integration
from base_service import BaseService
from xserverpy.utils.config import *
from xserverpy.utils import config
import json


class Integrations(BaseService):

    def __init__(self, settings, bot_id=None):
        self.bot_id = bot_id
        BaseService.__init__(self, settings)

    def integrate(self):
        return self.post()

    def endpoint(self):
        if self.bot_id:
            return "bots/%s/integrations" % self.bot_id
        else:
            return "integrations"

    def singe_item_endpoint(self, integration_id):
        return "integrations/%s" % integration_id

    def cancel_integration(self, item_id):
        url = self.singe_item_endpoint(item_id) + "/cancel"
        return self.perform_request(url, "post")

    def item_class(self):
        return Integration

    def get_running_integration(self):
        content, _ = self.perform_request("integrations/running", "get")
        parsed = self.parse_response(content)
        parsed = map(lambda x: self.get_item(x.id), parsed)
        return parsed
