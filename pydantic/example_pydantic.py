import json
from pprint import pprint
import re

from pydantic import BaseModel, field_validator


class User(BaseModel):
    login: str
    service_number: int
    email: str

    @field_validator('login')
    def validate_login(cls, value):
        if not re.fullmatch(r'[a-zA-Z]+[0-9?]+', value):
            raise ValueError('Login is invalid')
        return value

    @field_validator('email')
    def validate_email(cls, value):
        if not re.fullmatch(r'[a-zA-Z0-9.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+', value):
            raise ValueError('Email is invalid')
        return value


class Boss(BaseModel):
    user: User
    office: str

    @field_validator('office')
    def validate_office(cls, value):
        if not re.fullmatch(r'^[А-Я]{1}[а-я]{4,}[а-я ]{6,}', value):
            raise ValueError('Office is invalid')
        return value


def main():
    # Valid Boss
    valid_boss = {
        'user':
            {
                'login': 'login22',
                'service_number': 2000,
                'email': 'name@domen.ru',
            },
        'office': 'Отдел кадров',
    }

    # Invalid Boss
    invalid_boss = {
        'user':
            {
                'login': 'login_2',
                'service_number': 2000,
                'email': 'name_domen.ru',
            },
        'office': 'Отдел',
    }

    try:
        valid_boss_result = Boss(**valid_boss)
        print(valid_boss_result.model_dump_json(indent=4))

        invalid_boss_result = Boss(**invalid_boss)
    except ValueError as e:
        pprint(e.errors(), indent=4)


if __name__ == '__main__':
    main()

    """
    Вывод без ошибки:
    {
        "user": {
            "login": "login22",
            "service_number": 2000,
            "email": "name@domen.ru"
        },
        "office": "Отдел кадров"
    }

    Вывод ошибки:
[   {   'ctx': {'error': ValueError('Login is invalid')},
        'input': 'login_2',
        'loc': ('user', 'login'),
        'msg': 'Value error, Login is invalid',
        'type': 'value_error',
        'url': 'https://errors.pydantic.dev/2.6/v/value_error'},
    {   'ctx': {'error': ValueError('Email is invalid')},
        'input': 'name_domen.ru',
        'loc': ('user', 'email'),
        'msg': 'Value error, Email is invalid',
        'type': 'value_error',
        'url': 'https://errors.pydantic.dev/2.6/v/value_error'},
    {   'ctx': {'error': ValueError('Office is invalid')},
        'input': 'Отдел',
        'loc': ('office',),
        'msg': 'Value error, Office is invalid',
        'type': 'value_error',
        'url': 'https://errors.pydantic.dev/2.6/v/value_error'}]
    """
