import re
import json

from pydantic import BaseModel, validator


class User(BaseModel):
    login: str
    service_number: int
    email: str
    """
    Вложенная схема валидации данных
    """
    @validator("login")
    def validate_login(cls, value):
        if not bool(re.fullmatch(r'[a-zA-Z]+[0-9?]+', value)):
            raise ValueError("Login is invalid")
        return value

    @validator("email")
    def validate_email(cls, value):
        if not bool(re.fullmatch(r'[a-zA-Z0-9.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+', value)):
            raise ValueError("Email is invalid")
        return value


def main():
    # Valid User
    valid_user = {
        'login': 'login22',
        'service_number': 2000,
        'email': 'name@domen.ru',
    }

    # Invalid User
    invalid_user = {
        'login': 'login_2',
        'service_number': 1000,
        'email': 'name_domen.ru',
    }

    try:
        valid_result = User(**valid_user)
        print(valid_result.json(indent=4))
        invalid_result = User(**invalid_user)
        print(invalid_result.json(indent=4))
    except ValueError as e:
        print(json.dumps(e.errors(), ensure_ascii=False, indent=4))


if __name__ == '__main__':
    main()
    """
    Вывод без ошибки:
    {
        "login": "login22",
        "service_number": 2000,
        "email": "name@domen.ru"
    }

    Вывод ошибки:
    [
        {
            "loc": [
                "login"
            ],
            "msg": "Login is invalid",
            "type": "value_error"
        },
        {
            "loc": [
                "email"
            ],
            "msg": "Email is invalid",
            "type": "value_error"
        }
    ]
    """
