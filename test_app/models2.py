from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table

from database import Base

# a test table to understand how exclusion of tables from autogenerate in alembic works

class TestTable(Base):
    ''' '''
    __tablename__ = 'test_table';

    test_alembic = Column(Integer);
    id = Column(Integer, primary_key=True, index=True);
