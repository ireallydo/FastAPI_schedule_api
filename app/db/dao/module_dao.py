from db.models.ModuleModel import ModuleModel
from db.dto import ModuleCreateDTO
from .base_dao import BaseDAO


class ModuleDAO(BaseDAO[ModuleModel, ModuleCreateDTO, None, None]):
    pass


module_dao = ModuleDAO(ModuleModel)
