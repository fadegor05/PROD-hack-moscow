from enum import Enum

from fastapi import HTTPException


class MultiLangHTTPException(HTTPException):
    def __init__(self, status_code: int, detail_en: str, detail_ru: str):
        super().__init__(
            status_code=status_code, detail={"en": detail_en, "ru": detail_ru}
        )


class MultiLangHTTPExceptions(Enum):
    USER_ALREADY_EXISTS = (409, "User already exists", "Пользователь уже существует")
    USER_NOT_FOUND = (404, "User not found", "Пользователь не найден")
    EVENT_NOT_FOUND = (404, "Event not found", "Событие не найдено")
    EVENT_ALREADY_EXISTS = (409, "Event already exists", "Событие уже существует")
    BILL_NOT_FOUND = (404, "Bill not found", "Счет не найдено")
    BILL_ALREADY_EXISTS = (409, "Bill already exists", "Счет уже существует")
    ITEM_NOT_FOUND = (404, "Item not found", "Позиция не найдена")
    ITEM_ALREADY_EXISTS = (409, "Item already exists", "Позиция уже существует")
    INVALID_CREDENTIALS = (401, "Invalid credentials", "Неверные учетные данные")
    INVITE_NOT_FOUND = (404, "Invite not found", "Приглашение не найдено")
    INVALID_PERMISSIONS = (403, "Invalid permissions", "Недостаточно прав")

    def to_exception(self):
        return MultiLangHTTPException(*self.value)
