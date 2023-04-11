from pydantic import BaseModel as BaseSchema
from sqlalchemy import select, update, delete
from typing import Generic, TypeVar, Type, List, Union, NoReturn
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import BaseModel
from db.dto import *
from db.database import SessionLocal, engine
from sqlalchemy.exc import DBAPIError
from http import HTTPStatus
from fastapi import HTTPException
from loguru import logger


DBModelType = TypeVar("DBModelType", bound=BaseModel)
CreateDTOType = TypeVar("CreateDTOType", bound=BaseSchema)
UpdateDTOType = TypeVar("UpdateDTOType", bound=BaseSchema)
DeleteDTOType = TypeVar("DeleteDTOType", bound=BaseSchema)


class BaseDAO(Generic[DBModelType, CreateDTOType, UpdateDTOType, DeleteDTOType]):
    def __init__(self, model: Type[DBModelType], session_generator: Type[AsyncSession] = SessionLocal):
        self._model = model
        self._session_generator = session_generator

    async def create(self, input_data: CreateDTOType) -> Union[List[DBModelType], DBModelType]:
        logger.info(f"{self._model.__name__} DAO: Create db entry")
        logger.trace(
            f"{self._model.__name__} DAO: Data passed for creation: {input_data}")
        if isinstance(input_data, list):
            resp = []
            for d in input_data:
                if not isinstance(d, dict):
                    d = d.dict()
                new_line = self._model(**d)
                async with self._session_generator() as session:
                    session.add(new_line)
                    await session.commit()
                    await session.refresh(new_line)
                resp.append(new_line)
            logger.debug(f"{self._model.__name__} DAO: Created entries in database: {[r.dict() for r in resp]}")
            return resp
        elif isinstance(input_data, dict):
            new_line = self._model(**input_data)
        else:
            new_line = self._model(**input_data.dict())
        async with self._session_generator() as session:
            session.add(new_line)
            await session.commit()
            await session.refresh(new_line)
        logger.debug(f"{self._model.__name__} DAO: Created entry in database: {new_line.dict()}")
        return new_line

    async def get_by(self, **kwargs) -> DBModelType:
        logger.info(f"{self._model.__name__} DAO: Get db entry by parameters")
        logger.trace(
            f"{self._model.__name__} DAO: Data passed to filter: params: {kwargs}")
        async with self._session_generator() as session:
            try:
                resp = await session.execute(select(self._model).filter_by(**kwargs))
                resp = resp.scalar()
                logger.debug(f"{self._model.__name__} DAO: received a response from the database")
                return resp
            except DBAPIError:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail=f"Wrong data provided.",
                                    headers={"WWW-Authenticate": "Bearer"})

    async def get_all_by(self, skip: int = 0, limit: int = None, **kwargs) -> List[DBModelType]:
        logger.info(f"{self._model.__name__} DAO: Get all db entries by parameters")
        logger.trace(
            f"{self._model.__name__} DAO: Data passed to filter: skip: {skip}, limit: {limit}, params: {kwargs}")
        async with self._session_generator() as session:
            try:
                result = await session.execute(select(self._model).filter_by(**kwargs).offset(skip).limit(limit))
                resp = [raw[0] for raw in result]
                logger.debug(f"{self._model.__name__} DAO: received a response from the database")
                return resp
            except DBAPIError:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail=f"Wrong data provided.",
                                    headers={"WWW-Authenticate": "Bearer"})

    async def get_by_id(self, item_id) -> DBModelType:
        logger.info(f"{self._model.__name__} DAO: Get db entry by id: {item_id}")
        async with self._session_generator() as session:
            try:
                resp = await session.get(self._model, item_id)
                logger.debug(f"{self._model.__name__} DAO: received a response from the database")
                return resp
            except DBAPIError:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail=f"Wrong data provided.",
                                    headers={"WWW-Authenticate": "Bearer"})

    async def patch(self, patch_data, item_id) -> DBModelType:
        logger.info(f"{self._model.__name__} DAO: Update db entry")
        logger.trace(
            f"{self._model.__name__} DAO: Data passed for update: item_id: {item_id}, patch_data: {patch_data}")
        async with self._session_generator() as session:
            await session.execute(update(self._model).
                                  where(self._model.id == item_id).
                                  values(patch_data.dict(exclude_unset=True)))
            await session.commit()
            resp = await session.get(self._model, item_id)
            logger.debug(f"{self._model.__name__} DAO: Received updated entry from the database")
            return resp

    async def delete(self, item_id) -> NoReturn:
        async with self._session_generator() as session:
            await session.execute(delete(self._model).
                                  where(self._model.id == item_id))
            await session.commit()

    async def delete_by(self, **kwargs) -> NoReturn:
        async with self._session_generator() as session:
            await session.execute(delete(self._model).
                                  filter_by(**kwargs))
            await session.commit()
