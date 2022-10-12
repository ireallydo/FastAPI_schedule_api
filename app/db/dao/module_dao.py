from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models import ModuleModel
from db.enums import WeekdaysEnum
from db.dto import *


def fill_table(db: Session, input_data:  ModuleCreateDTO):
    new_line = ModuleModel(**input_data.dict())
    db.add(new_line)
    db.commit()
    db.refresh(new_line)
    print(new_line)
    return new_line

def get_all(db: Session, skip, limit):
    response =  db.query(ModuleModel).offset(skip).limit(limit).all()
    print(response)
    return response

def get_by_name(db: Session, module_name, skip, limit):
    response = db.query(ModuleModel).filter(ModuleModel.module_name==module_name).offset(skip).limit(limit).all()
    return response

def patch(db: Session, input_data: ModulePatchDTO):

    post_name = input_data.new_module_name
    post_class_type = input_data.new_class_type
    post_year = input_data.new_academic_year

    module = get_module_full(db, input_data)

    db.query(ModuleModel).filter(ModuleModel.id==module.id).update([(ModuleModel.module_name, post_name),
    (ModuleModel.class_type, post_class_type),
    (ModuleModel.academic_year, post_year)],
    update_args={'preserve_parameter_order': True})
    response = db.query(ModuleModel).filter(ModuleModel.id==module.id).one()
    db.commit()
    return response

def delete(db: Session, input_data: ModuleDeleteDTO):
    module = get_module_full(db, input_data)
    db.query(ModuleModel).filter(ModuleModel.id==module.id).delete()
    db.commit()

def get_module_full(db, input_data):
    search_name = input_data.module_name
    search_class_type = input_data.class_type
    search_year = input_data.academic_year

    module = db.query(ModuleModel).filter(ModuleModel.module_name==search_name, ModuleModel.class_type==search_class_type, ModuleModel.academic_year==search_year).first()

    return module
