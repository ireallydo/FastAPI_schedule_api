from fastapi import HTTPException
from db.models.SessionModel import SessionModel
from db.dto import *
from .base_dao import BaseDAO


class SessionDAO(BaseDAO[SessionModel, SessionCreateDTO, SessionPatchDTO, None]):
    pass


session_dao = SessionDAO(SessionModel)
