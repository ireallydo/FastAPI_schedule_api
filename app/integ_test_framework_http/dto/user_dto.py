from typing import List, Union, Dict, Optional
from pydantic import BaseModel

from uuid import UUID

class UserBase(BaseModel):
    class Config:
        orm_mode = True

# requests

class CreateUserRequest(UserBase):
    login: Optional[str]
    password: Optional[str]
    email: Optional[str]

# responses

class CreateUserResponse(UserBase):
    id: Optional[Union[UUID, str]]
    login: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
