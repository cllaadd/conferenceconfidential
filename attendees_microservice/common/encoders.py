from common.json import ModelEncoder
from attendees.models import Attendee, ConferenceVO


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
    properties = ["email", "name", "company_name", "created", "conference"]
    encoders = {"conference": ConferenceListEncoder()}
