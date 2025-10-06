"""
Ex15: Тесты на метод user
В соответствующем классе TestUserRegister, который мы создали на уроке,
необходимо написать больше тестов на создающий пользователя POST-метод: https://playground.learnqa.ru/api/user/
Список тестов:
- Создание пользователя с некорректным email - без символа @
- Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
- Создание пользователя с очень коротким именем в один символ
- Создание пользователя с очень длинным именем - длиннее 250 символов
"""

import requests
import pytest
import random
import string
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserReqister(BaseCase):

    # из урока
    def test_create_user_with_existing_email(self):  # проверка на существующий email.
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 400, f'unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"unexpected response content {response.content}"

    #  Создание пользователя с некорректным email - без символа @
    def test_create_user_with_incorrect_email(self):  # проверка на существующий email.
        email = 'vinkotov'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f'unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"unexpected response content {response.content}"

        # Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя

    @pytest.mark.parametrize('fields_empty', [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ])
    def test_create_user_with_empty_field(self, fields_empty):  # проверка на существующий email.
        email = 'vinkotov10@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        del data[fields_empty]
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 400, f'unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {fields_empty}", f"unexpected response content {response.content}"

    # Создание пользователя с очень коротким именем в один символ
    name_one_symbol_value = 'l'

    @pytest.mark.parametrize('name_one_symbol', [
        ('username'),
        ('firstName'),
        ('lastName')
    ])
    def test_create_user_with_name_one_symbol(self, name_one_symbol):
        email = 'vinkotov11@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        data[name_one_symbol] = self.name_one_symbol_value
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 400, f'unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == f"The value of '{name_one_symbol}' field is too short", f"unexpected response content {response.content}"

    # Создание пользователя с очень длинным именем - длиннее 250 символов
    long_string = "".join(random.choices(string.ascii_letters, k=251))

    @pytest.mark.parametrize('name', [
        'username',
        'firstName',
        'lastName',
    ])
    def test_create_user_with_name_long(self, name):
        email = 'vinkotov12@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        data[name] = self.long_string
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f'unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == f"The value of '{name}' field is too long", f"unexpected response content {response.content}"
