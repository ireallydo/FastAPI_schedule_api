from db.models.TeacherModel import TeacherModel
from db.dto import *
from .base_dao import BaseDAO
from loguru import logger


class TeacherDAO(BaseDAO[TeacherModel, TeacherCreateDTO, None, None]):

    async def create_modules(self, user_id, modules):
        logger.info("TeacherDAO: Create db entry")
        logger.trace(f"TeacherDAO: Data passed for creation: modules: {modules}")
        async with self._session_generator() as session:
            teacher = await session.get(self._model, user_id)
            for module in modules:
                teacher.modules.append(module)
                await session.commit()
            resp = await session.get(self._model, user_id)
            return resp.modules

    async def delete_teacher_module(self, user_id, module):
        logger.info("TeacherDAO: Query db to de-associate teacher from module")
        logger.trace(f"TeacherDAO: Data passed for de-association: teacher_id: {user_id}, module_id: {module.id}")
        async with self._session_generator() as session:
            teacher = await session.get(self._model, user_id)
            for mod in teacher.modules:
                if mod.id == module.id:
                    obj = mod
            teacher = await session.get(self._model, user_id)
            teacher.modules.remove(obj)
            await session.commit()


teacher_dao = TeacherDAO(TeacherModel)
