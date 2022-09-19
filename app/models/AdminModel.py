from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base

class AdminModel(Base):
    __tablename__ = 'admins';

    id = Column(Integer, primary_key=True, index=True);
    name = Column(String(255), unique=True, index=True);
    # users - administration - one-to-one (unique)

    username = relationship('UserModel', back_populates='admin', uselist=False);
