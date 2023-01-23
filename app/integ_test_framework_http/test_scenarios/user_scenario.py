import requests

from settings.settings import Settings
from ..test_cases_positive import user_cases


settings = Settings()

#decide what to do with ids, tokens etc variables
#headers to consts

with requests.Session() as session:
    create_user = user_cases.create_user(session)
    print(create_user)
