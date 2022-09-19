from sqlalchemy import Column, ForeignKey
from sqlalchemy.schema import Table

from db import Base

modules_to_typesOfClasses = Table(
    'modules_to_typesOfClasses_association', Base.metadata,
    Column('Module_id', ForeignKey('modules.id')),
    Column('TypeOfClass_id', ForeignKey('class_types.id'))
    );
