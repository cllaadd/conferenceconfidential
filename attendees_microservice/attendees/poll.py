import json
import requests

from .models import ConferenceVO, AccountVO


def get_conferences():
    url = "http://monolith:8000/api/conferences/"
    response = requests.get(url)
    content = json.loads(response.content)
    for conference in content["conferences"]:
        ConferenceVO.objects.update_or_create(
            import_href=conference["href"],
            defaults={"name": conference["name"]},
        )


# def get_accounts():
#     url = "http://monolith:8000/api/accounts/"
#     response = requests.get(url)
#     content = json.loads(response.content)
#     for conference in content["conferences"]:
#         AccountVO.objects.update_or_create(**content)
