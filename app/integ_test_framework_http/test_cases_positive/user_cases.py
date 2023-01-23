from settings.settings import Settings
from ..routers import user_router
from ..payloads import user_payload as payloads
from ..assertion.check_status import check_for_code_201, check_for_code_200
from ..dto import CreateUserResponse


def create_user(session):
    payload =  payloads.create_user()
    create_user_response = user_router.create_user(session, payload=payload)
    # ASSERTION
    response = check_for_code_201('CREATE USER', create_user_response, response_model=CreateUserResponse)
    response_dict = {'status_code': create_user_response.status_code, 'body': response}
    return response_dict

def get_user():
    pass

def patch_user():
    pass

def set_user_inactive():
    pass
