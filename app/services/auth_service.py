from fastapi import HTTPException
from http import HTTPStatus
from db.models import SessionModel, UserModel
from db.dto import LoginRespDTO, SessionCreateDTO
from utils import utils
from services.user_service import user_service
from db.dao import session_dao, SessionDAO
from loguru import logger


class AuthService:

    def __init__(self, session_dao: SessionDAO):
        self._session_dao = session_dao

    async def __create_session(self, user: UserModel) -> SessionModel:
        logger.info("AuthService: Create session")
        logger.trace(f"AuthService: Create session with user: {user.id}")
        access_token, access_expire_time = utils.create_access_token(user.login)
        refresh_token, refresh_expire_time = utils.create_refresh_token(user.login)
        session_obj = SessionCreateDTO(
            user_id=user.id,
            login=user.login,
            role=user.role,
            access_token=access_token,
            refresh_token=refresh_token,
            access_expire_time=access_expire_time,
            refresh_expire_time=refresh_expire_time,
            blocked=user.blocked,
            is_active=user.is_active
        )
        session = await self._session_dao.create(session_obj)
        return session

    async def login_user(self, form_data) -> LoginRespDTO:
        logger.info(f"AuthService: Login user")
        logger.trace(f"AuthService: Login user: {form_data.username}")
        user = await user_service.get_by_login(form_data.username)
        if user is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Incorrect login or password')
        elif user.blocked:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='User is blocked. Please contact administration.')
        elif not user.is_active:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='User was deleted. Please contact administration.')
        if not utils.verify_password(form_data.password, user.password):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Incorrect login or password')
        session = await self.__create_session(user)
        resp = LoginRespDTO(access_token=session.access_token,
                            refresh_token=session.refresh_token,
                            user_id=user.id,
                            login=user.login,
                            role=user.role)
        return resp


auth_service = AuthService(session_dao)
