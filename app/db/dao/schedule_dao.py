from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from fastapi import Depends, FastAPI, HTTPException

from db.models import ScheduleModel
from db.dto import ScheduleCreateManuallyDTO

# def get_db():
#     db = SessionLocal();
#     try:
#         yield db;
#     finally:
#         db.close();
#
# db: Session = Depends(get_db)

def fill_manually(input_data: ScheduleCreateManuallyDTO):

    new_line = ScheduleCreateManuallyDTO(**input_data.dict())

    db.add(new_line)
    db.commit()
    db.refresh(new_line)

    return new_line

def check_exists(db, input_data: ScheduleCreateManuallyDTO):

        return db.query(ScheduleModel).filter(ScheduleModel.group==input_data.group,
                                            ScheduleModel.semester==input_data.semester,
                                            ScheduleModel.weekday==input_data.weekday,
                                            ScheduleModel.lesson_number==input_data.lesson_number).all()
