from enum import Enum

from fastapi import HTTPException


class MultiLangHTTPException(HTTPException):
    def __init__(self, status_code: int, detail_en: str, detail_ru: str):
        super().__init__(status_code=status_code, detail={
            "en": detail_en,
            "ru": detail_ru
        })


class MultiLangHTTPExceptions(Enum):
    USER_ALREADY_EXISTS = (409, "User already exists", "Пользователь уже существует")
    USER_NOT_FOUND = (404, "User not found", "Пользователь не найден")

    def to_exception(self):
        return MultiLangHTTPException(*self.value)
