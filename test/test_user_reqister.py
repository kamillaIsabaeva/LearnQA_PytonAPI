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

import pytest
import random
import string
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("User Registration")

class TestUserReqister(BaseCase):
    # из урока
    @allure.description("This tets successfully created user ")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        assert response.status_code == 200, f'unexpected status code {response.status_code}'
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This tets  created user with existing email ")
    def test_create_user_with_existing_email(self):  # проверка на существующий email.
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"unexpected response content {response.content}"

    #  Создание пользователя с некорректным email - без символа @
    def test_create_user_with_incorrect_email(self):  # проверка на существующий email.
        email = 'vinkotov'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

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
        data = self.prepare_registration_data()
        del data[fields_empty]
        response = MyRequests.post("/user/", data=data)
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
        data = self.prepare_registration_data()

        data[name_one_symbol] = self.name_one_symbol_value
        response = MyRequests.post("/user/", data=data)
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
        data = self.prepare_registration_data()
        data[name] = self.long_string
        response = MyRequests.post("/user/", data=data)

        assert response.status_code == 400, f'unexpected status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == f"The value of '{name}' field is too long", f"unexpected response content {response.content}"
