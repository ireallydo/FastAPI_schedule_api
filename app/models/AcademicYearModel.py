from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from db import Base

class AcademicYearModel(Base):
    __tablename__ = 'years';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, primary_key=True, index=True);
    # students - years - many-to-one

    students = relationship('StudentModel', back_populates='year');
