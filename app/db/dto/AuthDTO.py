from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID
from datetime import datetime

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

# class SessionCreateDTO(BaseModel):
#     user_id: UUID
#     login: str
#     expire_time: datetime
#     access_token: str
#     refresh_token: str
#
# class SessionPatchDTO(BaseModel):
#     expire_time: datetime
