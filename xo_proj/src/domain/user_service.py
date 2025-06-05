# user_service.py
from uuid import uuid4
from domain.model import User
from datasource.repository import UserRepository


class UserService:

    @staticmethod
    def register(login: str, password: str) -> bool:
        user_check = UserRepository.get_user(login)
        if user_check:
            print("UserService User already exists:", user_check)
            return False

        UserRepository.add_user(str(uuid4()), login, password)
        print("UserService User registered:", UserRepository.get_user(login))
        return True

    @staticmethod
    def authenticate(login: str, password: str) -> User | None:
        print("UserService authenticate:", login, password)
        user = UserRepository.get_user(login)
        if user and user.password == password:
            print("UserService User authenticated correct:", user)
            return user
        print("UserService User authenticated incorrect:", user)
        return None

    @staticmethod
    def get_by_uid(user_uuid: str) -> User | None:
        user = UserRepository.get_user_by_uid(user_uuid)
        print("UserService get_by_uid:", user)
        return user
