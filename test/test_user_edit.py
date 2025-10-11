"""
Ex17: Негативные тесты на PUT
На занятиях мы написали только позитивный тест на PUT-метод редактирования пользователя.
Давайте напишем несколько негативных:
- Попытаемся изменить данные пользователя, будучи неавторизованными
- Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
- Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
- Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
"""

import requests
import pytest
import random
import string

from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # login
        login_data = {'email': email,
                      'password': password}
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Edit
        new_name = "Changed Name"
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_user_not_auth(self):
        # GET
        response1 = requests.get(f"https://playground.learnqa.ru/api/user/2")
        before_username = self.get_json_value(response1, "username")

        new_name = "Changed Name"
        response = requests.put(f"https://playground.learnqa.ru/api/user/2", data={"firstName": new_name})
        Assertions.assert_code_status(response, 400)

        response2 = requests.get(f"https://playground.learnqa.ru/api/user/2")
        current_username = self.get_json_value(response2, "username")

        assert before_username == current_username, "first name changed not_auth "
        print(f"test_edit_user_not_auth: {current_username}, {before_username}")

    # Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_edit_user_other_auth(self):
        # Register user_1
        user_1_register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=user_1_register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email_1 = user_1_register_data['email']
        first_name_1 = user_1_register_data['firstName']
        password_1 = user_1_register_data['password']
        user_id_1 = self.get_json_value(response1, "id")

        # Register user_2
        user_2_register_data = self.prepare_registration_data()
        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=user_2_register_data)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email_2 = user_2_register_data['email']
        first_name_2 = user_2_register_data['firstName']
        password_2 = user_2_register_data['password']
        user_id_2 = self.get_json_value(response2, "id")

        # login user_1
        login_data = {'email': email_1,
                      'password': password_1}
        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid_1 = self.get_cookie(response3, "auth_sid")
        token_1 = self.get_header(response3, "x-csrf-token")

        # GET
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_1}",
                                 headers={"x-csrf-token": token_1},
                                 cookies={"auth_sid": auth_sid_1})
        before_name_first_name_1 = self.get_json_value(response4, "firstName")

        # Edit
        new_name = "Changed Name"
        response5 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id_2}",
                                 headers={"x-csrf-token": token_1},
                                 cookies={"auth_sid": auth_sid_1},
                                 data={"firstName": new_name}
                                 )
        # GET
        response6 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_1}",
                                 headers={"x-csrf-token": token_1},
                                 cookies={"auth_sid": auth_sid_1})
        current_name_first_name_1 = self.get_json_value(response6, "firstName")

        print(f"test_edit_user_other_auth: {current_name_first_name_1}, {before_name_first_name_1}")
        Assertions.assert_code_status(response5, 400)
        assert response5.content.decode("utf-8") == '{"error":"This user can only edit their own data."}'
        assert current_name_first_name_1 == before_name_first_name_1, "name other user changed "

    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_user_email_without_at_symbol(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # login
        login_data = {'email': email,
                      'password': password}
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # GET
        response3 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        before_email = self.get_json_value(response3, "email")

        # Edit
        new_email = "voctorovmail.ru"
        response4 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": new_email}
                                 )

        Assertions.assert_code_status(response4, 400)
        assert response4.content.decode(
            "utf-8") == '{"error":"Invalid email format"}'

        # GET
        response5 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        current_email = self.get_json_value(response5, "email")
        assert current_email == before_email, "Email changed "
        print(f"test_edit_user_email_without_at_symbol: {current_email}, {before_email}")

    # Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_user_name_one_symbol(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # login
        login_data = {'email': email,
                      'password': password}
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # GET
        response3 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        before_firstName = self.get_json_value(response3, "firstName")

        # Edit
        new_name = "o"
        response4 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response4, 400)
        assert response4.content.decode("utf-8") == '{"error":"The value for field `firstName` is too short"}'

        # GET
        response5 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})
        current_firstName = self.get_json_value(response5, "firstName")
        assert current_firstName == before_firstName, "firstName changed"
        print(f"test_edit_user_name_one_symbol: {current_firstName}, {before_firstName}")
