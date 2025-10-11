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
<<<<<<< HEAD
from datetime import datetime


class TestUserReqister(BaseCase):
    # из урока
    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 200, f'unexpected status code {response.status_code}'
        Assertions.assert_json_has_key(response, "id")

=======


class TestUserReqister(BaseCase):

    # из урока
>>>>>>> b4393f39ffde8f501679e8386baccb7e493718c9
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
<<<<<<< HEAD
        Assertions.assert_code_satus(response, 400)
=======
        assert response.status_code == 400, f'unexpected status code {response.status_code}'
>>>>>>> b4393f39ffde8f501679e8386baccb7e493718c9
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
<<<<<<< HEAD

=======
        email = 'vinkotov10@example.com'
>>>>>>> b4393f39ffde8f501679e8386baccb7e493718c9
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
<<<<<<< HEAD
            'email': self.email
=======
            'email': email
>>>>>>> b4393f39ffde8f501679e8386baccb7e493718c9
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
<<<<<<< HEAD

=======
        email = 'vinkotov11@example.com'
>>>>>>> b4393f39ffde8f501679e8386baccb7e493718c9
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
<<<<<<< HEAD
            'email': self.email
=======
            'email': email
>>>>>>> b4393f39ffde8f501679e8386baccb7e493718c9
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
<<<<<<< HEAD

=======
        email = 'vinkotov12@example.com'
>>>>>>> b4393f39ffde8f501679e8386baccb7e493718c9
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
<<<<<<< HEAD
            'email': self.email
=======
            'email': email
>>>>>>> b4393f39ffde8f501679e8386baccb7e493718c9
        }
        data[name] = self.long_string
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f'unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == f"The value of '{name}' field is too long", f"unexpected response content {response.content}"
