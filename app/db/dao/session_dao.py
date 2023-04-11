from db.models.SessionModel import SessionModel
from db.dto import SessionCreateDTO, SessionPatchDTO
from .base_dao import BaseDAO


class SessionDAO(BaseDAO[SessionModel, SessionCreateDTO, SessionPatchDTO, None]):
    pass


session_dao = SessionDAO(SessionModel)
