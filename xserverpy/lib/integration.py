from bot import Bot
import dateutil.parser
import pytz
from tzlocal import get_localzone


class Integration():

    @staticmethod
    def from_json(json):
        date = None
        if "queuedDate" in json:
            date = dateutil.parser.parse(json["queuedDate"])

        return Integration(number=json["number"],
                           id=json["_id"],
                           result=json.get("result", "in progress"),
                           step=json["currentStep"],
                           bot=Bot.from_json(json.get("bot", None)),
                           tiny_id=json.get("tinyID", ""),
                           date=date)

    def __init__(self, **args):
        self.number = args["number"]
        self.id = args["id"]
        self.tiny_id = args["tiny_id"]
        self.result = args["result"]
        self.bot = args["bot"]
        self.date = args["date"]
        self.step = args["step"]

    def __repr__(self):
        return self.__dict__.__str__()

    def status(self):
        if self.step == "completed":
            return self.result
        else:
            return self.step

    def date_string(self):
        temp = self.date.replace(tzinfo=pytz.utc)
        local_time = temp.astimezone(get_localzone())
        return local_time.strftime('%d-%b-%Y %H:%M')

    def is_complete(self):
        return self.step == "completed"

    def is_pending(self):
        return self.step == "pending"

    def succeeded(self):
        return self.result == "succeeded"

    def completed_with_warnings(self):
        return self.result == "warnings"
