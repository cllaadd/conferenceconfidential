from common.json import ModelEncoder
from .models import Presentation


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title", "status"]

    def get_extra_data(self, o):
        return {"status": o.status.name}


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]
