import urlparse
import requests
import json


class BaseService():

    def __init__(self, settings):
        self.server = settings.server
        urlparts = urlparse.urlparse(self.server.host)
        self.user = settings.user
        self.url = "%s://%s:%s/xcode/api/" % (urlparts.scheme, urlparts.netloc, settings.server.port)

    def get_all(self):
        result = self.perform_request(self.endpoint(), "get")
        return self.parse_response(result[0])

    def post(self):
        result = self.perform_request(self.endpoint(), "post")
        return self.item_class().from_json(json.loads(result[0]))

    def get_item(self, item_id=None):
        if not item_id:
            raise RuntimeError("item_id is reuired")

        result = self.perform_request(self.singe_item_endpoint(item_id), "get")
        if not result: return None

        return self.item_class().from_json(json.loads(result[0]))

    def perform_request(self, path_url, http_method):
        try:
            requests.packages.urllib3.disable_warnings()
            method = getattr(requests, http_method, None)
            r = method(
                    url=self.url + path_url,
                    auth=self.basic_auth(),
                    verify=False
                )

            if r.status_code in (200, 201, 204):
                return r.content, r.status_code
            if r.status_code == 409:
                raise RuntimeError("Conflict happened, please retry later")
            if r.status_code in (401, 403):
                if self.basic_auth():
                    raise RuntimeError("User name or password provided are not correct")
                else:
                    raise RuntimeError("Xcode server requires user and password, "
                                       "use --user USER and --pass PASSWORD")
        except Exception as e:
            raise e

        raise RuntimeError("Unknown error occurred")

    def basic_auth(self):
        return self.user.basic_auth()

    def parse_response(self, response):
        parsed = json.loads(response)
        results = parsed["results"]
        items = map(lambda x: self.item_class().from_json(x), results)
        return items

    # Subclass
    def endpoint(self):
        raise RuntimeError("Must be implemented")

    def singe_item_endpoint(self, item_id):
        raise RuntimeError("Must be implemented")

    def item_class(self):
        raise RuntimeError("Must be implemented")
