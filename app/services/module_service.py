from sorcery import dict_of
from typing import NoReturn
from http import HTTPStatus
from fastapi import HTTPException
from db.models import ModuleModel
from db.dto import ModuleCreateDTO, ModuleTeachersDTO
from db.dao import module_dao, ModuleDAO
from loguru import logger


class ModuleService:

    def __init__(self, module_dao: ModuleDAO):
        self._module_dao = module_dao

    async def create_module(self, item: ModuleCreateDTO) -> ModuleModel:
        """creates a module if module with same name, class_type and year does not exist"""
        logger.info("ModuleService: Create module")
        logger.trace(f"ModuleService: Create module with passed data {item}")
        logger.info("ModuleService: Check if module with same parameters exists.")
        in_db = await self._module_dao.get_by(module_name=item.module_name,
                                              class_type=item.class_type,
                                              academic_year=item.academic_year)
        if in_db:
            logger.info(f"ModuleService: Got existing module from db: {in_db}")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="Module with provided parameters already exists.",
                                headers={"WWW-Authenticate": "Bearer"})
        response = await self._module_dao.create(item)
        return response

    async def get_all_modules(self, *args) -> list:
        logger.info("ModuleService: Get all modules")
        resp = await self._module_dao.get_all_by(*args)
        response = [module for module in resp]
        return response

    async def get_by_id(self, module_id: str) -> ModuleModel:
        logger.info(f"ModuleService: Get module by id: {module_id}")
        # here's get)by instead of get_by_id, because modules have a triple primary key
        response = await self._module_dao.get_by(id=module_id)
        if response is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Module with provided id does not exist.",
                                headers={"WWW-Authenticate": "Bearer"})
        return response

    async def get_teachers(self, module_id: str) -> ModuleTeachersDTO:
        module = await self.get_by_id(module_id)
        teachers = module.teachers
        response = ModuleTeachersDTO(id=module_id,
                                     teachers=teachers)
        return response

    async def delete(self, module_id: int) -> NoReturn:
        """deletes module from the database"""
        logger.info("ModuleService: Delete module")
        await self._module_dao.delete(module_id)


module_service = ModuleService(module_dao)


# def get_by_name(db, module_name, skip, limit):
#     return module_dao.get_all_by_name(db, module_name, skip, limit)
# def get_by_name_and_type(db, module_name, class_type):
#     input_data = dict_of(module_name, class_type)
#     return module_dao.get_by(db, input_data)
#
# def patch(db, search_data, patch_data):
#     module = module_dao.get_by(db, search_data)
#     module_dao.patch(db, patch_data, module.id)
#     return module_dao.get_by_id(db, module.id)
