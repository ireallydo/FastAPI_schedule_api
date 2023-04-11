from typing import NoReturn, Union
from http import HTTPStatus
from datetime import datetime
from fastapi import HTTPException
from services.student_service import student_service, StudentService
from services.teacher_service import teacher_service, TeacherService
from db.models import UserModel
from db.dto import CheckUserDTO, UserCreateDTO, UserRegisterDTO,\
    UserPatchDTO, UserChangePasswordDTO, UserBlockedDTO, UserDeleteDTO
from db.dao import user_dao, UserDAO, student_dao, StudentDAO, teacher_dao, TeacherDAO
from utils.utils import hash_password
from loguru import logger


class UserService:
    def __init__(self, user_dao: UserDAO, student_service: StudentService, teacher_service: TeacherService):
        self._user_dao = user_dao
        self._student_service = student_service
        self._teacher_service = teacher_service

    async def create(self, item: UserRegisterDTO) -> UserModel:
        logger.info(f"UserService: Create user")
        logger.trace(f"UserService: Create user with passed data {item}")
        # check is user with provided login and/or email already exists
        login_ex = await self._user_dao.get_by(login=item.login)
        email_ex = await self._user_dao.get_by(email=item.email)
        if login_ex or email_ex is not None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="Cannot use this login or email.")
        item.birth_date = datetime.strptime(item.birth_date, '%d-%m-%Y')
        item.password = hash_password(item.password)
        if item.role == 'student':
            service = self._student_service
        elif item.role == 'teacher':
            service = self._teacher_service
        elif item.role == 'admin':
            create_obj = UserCreateDTO(**item.dict())
            return await self._user_dao.create(create_obj)
        else:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Provided user role is not acceptable.")

        user = await service.get_by(
            first_name=item.first_name,
            second_name=item.second_name,
            last_name=item.last_name,
            birth_date=item.birth_date
        )
        if user is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="User cannot be registered. Please contact your administrator.")
        elif user.registered_user and user.is_active:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="User is already registered. Please contact administration.")
        elif not user.is_active:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="User was registered and deleted.\
                                 Please contact administration to restore user.")
        else:
            try:
                assert (item.registration_token == user.registration_token)
                item.id = user.id
                create_obj = UserCreateDTO(**item.dict())
                resp = await self._user_dao.create(create_obj)
                await service.set_registered(user.id, True)
                return resp
            except AssertionError:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail="Registration token for provided user is incorrect")

    async def get_profile(self, user_id: str) -> UserModel:
        logger.info("UserService: Get user profile")
        logger.trace(f"UserService: Get user by id: {user_id}")
        response = await self._user_dao.get_by_id(user_id)
        if response is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"User with provided id does not exist.")
        return response

    async def patch(self, user_id: str, patch_data: Union[UserPatchDTO, UserBlockedDTO]) -> UserModel:
        logger.info("UserService: Update user profile")
        logger.trace(f"UserService: Update user: {user_id} with following data: {patch_data}")
        resp = await self._user_dao.patch(patch_data, user_id)
        return resp

    async def change_password(self, user_id: str, patch_data: UserChangePasswordDTO) -> NoReturn:
        logger.info("UserService: Change user password")
        logger.trace(f"UserService: Change password for user with id: {user_id}")
        patch_data.password = hash_password(patch_data.password)
        await self._user_dao.patch(patch_data, user_id)

    async def delete_user(self, user_id: str) -> NoReturn:
        logger.info("UserService: Delete user")
        logger.trace(f"UserService: Set is_active field to False for user with id {user_id}")
        user = await self._user_dao.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="No user found with provided id.")
        elif not user.is_active:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="User is already deleted.")
        else:
            patch_data = UserDeleteDTO(is_active=False)
            await self._user_dao.patch(patch_data, user_id)

    async def restore_user(self, user_id: str) -> NoReturn:
        logger.info("UserService: Restore user")
        logger.trace(f"UserService: Set is_active field to True for user with id {user_id}")
        user = await self._user_dao.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="No user found with provided id.")
        elif user.is_active:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="User is active and cannot be restored.")
        else:
            patch_data = UserDeleteDTO(is_active=True)
            await self._user_dao.patch(patch_data, user_id)

    @staticmethod
    async def get_by_login(login):
        user = await user_dao.get_by(login=login)
        return user


user_service = UserService(user_dao, student_service, teacher_service)
