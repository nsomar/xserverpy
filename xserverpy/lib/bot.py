class Bot():

    @staticmethod
    def from_json(json):
        if json:
            return Bot(name=json.get("name", ""),
                       id=json["_id"],
                       integration_counter=json.get("integration_counter", ""))
        else:
            return EmptyBot()

    def __init__(self, **args):
        self.name = args["name"]
        self.id = args["id"]
        self.integration_counter = args["integration_counter"]

    def __repr__(self):
        return self.__dict__.__str__()


class EmptyBot():

    def __init__(self, **args):
        self.name = " - "
        self.id = " - "
        self.integration_counter = " - "
