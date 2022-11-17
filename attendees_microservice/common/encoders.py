from common.json import ModelEncoder
from attendees.models import Attendee, ConferenceVO, AccountVO


# class AccountVOEncoder(ModelEncoder):
#     model = AccountVO
#     properties = ["email", "first_name", "last_name", "is_active", "updated"]


class ConferenceVODetailEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name", "import_href"]


class ConferenceListEncoder(ModelEncoder):
    model = ConferenceVO
    properties = ["name"]


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = ["name"]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
    ]
    encoders = {
        "conference": ConferenceVODetailEncoder(),
    }

    def get_extra_data(self, o):
        count = AccountVO.objects.filter(email=o.email).count()
        return {"has_account": count > 0}
