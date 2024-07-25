from os import environ
import json
from pprint import pprint
import re

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SubParams(BaseSettings):
    first_parameter: str
    second_parameter: str

    @field_validator('second_parameter')
    def validate_latin_text(cls, value):
        if not re.fullmatch(r'[a-zA-Z ]+', value):
            raise ValueError('second_parameter is invalid')
        return value

    @field_validator('first_parameter')
    def validate_cyril_text(cls, value):
        if not re.fullmatch(r'[а-яА-ЯёЁ ]+', value):
            raise ValueError('first_parameter is invalid')
        return value


class Params(BaseSettings):
    latin_text: str
    cyril_text: str
    email: str
    more_params: SubParams

    @field_validator('latin_text')
    def validate_latin_text(cls, value):
        if not re.fullmatch(r'[a-zA-Z]+', value):
            raise ValueError('latin_text is invalid')
        return value

    @field_validator('cyril_text')
    def validate_cyril_text(cls, value):
        if not re.fullmatch(r'[а-яА-ЯёЁ]+', value):
            raise ValueError('cyril_text is invalid')
        return value

    @field_validator('email')
    def validate_email(cls, value):
        if not re.fullmatch(r'[a-zA-Z0-9.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+', value):
            raise ValueError('Email is invalid')
        return value


def main():

    """
    В файле val.env содержатся следующие переменные среды:

    LATIN_TEXT=qwertyuiop
    CYRIL_TEXT=йцукенгшфывапр
    EMAIL=to.email@email.com

    В файле inval.env содержатся следующие переменные среды:
    LATIN_TEXT=qwertyuiopй
    CYRIL_TEXT=йцукенгшфывапрz
    EMAIL=to.email-email.com
    """

    environ['first_parameter'] = 'Первый параметр'
    environ['second_parameter'] = 'Second parameter'
    params = Params(_env_file='val.env', _env_file_encoding='utf-8', more_params=SubParams())
    print(params.model_dump_json(indent=4))

    try:
        params = Params(_env_file='inval.env', _env_file_encoding='utf-8', more_params=SubParams())
    except ValueError as e:
        pprint(e.errors(), indent=4)

    environ['first_parameter'] = 'Первый параметр9'
    environ['second_parameter'] = 'Second parameter9'

    try:
        params = Params(_env_file='inval.env', _env_file_encoding='utf-8', more_params=SubParams())
    except ValueError as e:
        pprint(e.errors(), indent=4)


if __name__ == '__main__':
    main()


    """
    Вывод без ошибки:

    {
        "latin_text": "qwertyuiop",
        "cyril_text": "йцукенгшфывапр",
        "email": "to.email@email.com",
        "more_params": {
            "first_parameter": "Первый параметр",
            "second_parameter": "Second parameter"
        }
    }

    Вывод ошибки в Params:
    [   {   'ctx': {'error': ValueError('latin_text is invalid')},
            'input': 'qwertyuiopй',
            'loc': ('latin_text',),
            'msg': 'Value error, latin_text is invalid',
            'type': 'value_error',
            'url': 'https://errors.pydantic.dev/2.6/v/value_error'},
        {   'ctx': {'error': ValueError('cyril_text is invalid')},
            'input': 'йцукенгшфывапрz',
            'loc': ('cyril_text',),
            'msg': 'Value error, cyril_text is invalid',
            'type': 'value_error',
            'url': 'https://errors.pydantic.dev/2.6/v/value_error'},
        {   'ctx': {'error': ValueError('Email is invalid')},
            'input': 'to.email-email.com',
            'loc': ('email',),
            'msg': 'Value error, Email is invalid',
            'type': 'value_error',
            'url': 'https://errors.pydantic.dev/2.6/v/value_error'}]

    Вывод ошибки в Subparams:

    [   {   'ctx': {'error': ValueError('first_parameter is invalid')},
            'input': 'Первый параметр9',
            'loc': ('first_parameter',),
            'msg': 'Value error, first_parameter is invalid',
            'type': 'value_error',
            'url': 'https://errors.pydantic.dev/2.6/v/value_error'},
        {   'ctx': {'error': ValueError('second_parameter is invalid')},
            'input': 'Second parameter9',
            'loc': ('second_parameter',),
            'msg': 'Value error, second_parameter is invalid',
            'type': 'value_error',
            'url': 'https://errors.pydantic.dev/2.6/v/value_error'}]
    """
