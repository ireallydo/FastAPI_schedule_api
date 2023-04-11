from functools import wraps
from db.enums import UserRolesEnum as Roles
from http import HTTPStatus
from fastapi import HTTPException
from loguru import logger


def available_roles(role, self_action=False):
    def self_actions(requesting_user, user_id):
        if str(requesting_user) != user_id:
            e = HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Forbidden')
            logger.exception(e)
            raise e

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_role = kwargs.get('self').auth_headers.role
            requesting_user = kwargs.get('self').auth_headers.user_id
            user_id = kwargs.get("user_id")
            if self_action:
                if role != Roles.ADMIN or Roles.get(user_role) != Roles.ADMIN:
                    self_actions(requesting_user, user_id)
                return_value = await func(*args, **kwargs)
            elif Roles.get(user_role) >= role:
                return_value = await func(*args, **kwargs)
            else:
                e = HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Forbidden')
                logger.exception(e)
                raise e
            return return_value
        return wrapper
    return decorator
