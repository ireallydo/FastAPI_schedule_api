from settings.settings import Settings
from .api_specs.user_api_spec import ApiSpec
from ..clients import http_client as client


settings = Settings()


URL = settings.HOST + ":" + settings.PORT


def create_user(session, headers={}, payload={}):
    url = URL + ApiSpec.USER
    response = client.post(session, url, payload, headers)
    return response


def get_user():
    url = URL + ApiSpec.USER
    response = client.get(session, url, payload, headers)
    return response


def patch_user():
    url = URL + ApiSpec.USER
    response = client.patch(session, url, payload, headers)
    return response


def set_user_inactive():
    url = URL + ApiSpec.USER_INACTIVE
    response = client.patch(session, url, payload, headers)
    return response
