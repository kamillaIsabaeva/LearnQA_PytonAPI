"""
Ex18: Тесты на DELETE
У нас есть метод, который удаляет пользователя по ID - DELETE-метод https://playground.learnqa.ru/api/user/{id}
Само собой, удалить можно только того пользователя, из-под которого вы авторизованы.
Необходимо в директории tests/ создать новый файл test_user_delete.py с классом TestUserDelete.
Там написать следующие тесты.
Первый - на попытку удалить пользователя по ID 2. Его данные для авторизации:
data = {
'email': 'vinkotov@example.com',
passwod': '1234'
Убедиться, что система не даст вам удалить этого пользователя.
Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться,
 что пользователь действительно удален.
Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
"""

import requests
import pytest
import random
import string

from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserDelete(BaseCase):
    # Убедиться, что система не даст вам удалить этого пользователя.
    def test_delete_user_id_2(self):
        # login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        response2 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf-8") == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}'

        response3 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_code_status(response3, 200)
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response3, expected_fields)

        # Cоздать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться,что пользователь действительно удален.

    def test_delete_created_user_and_check_deletion(self):
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

        response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)
        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == 'User not found'

    # Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_user_other_auth(self):
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

        response5 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id_2}",
                                    headers={"x-csrf-token": token_1},
                                    cookies={"auth_sid": auth_sid_1})

        # GET
        response6 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_1}",
                                 headers={"x-csrf-token": token_1},
                                 cookies={"auth_sid": auth_sid_1})
        response7 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_1}",
                                 headers={"x-csrf-token": token_1},
                                 cookies={"auth_sid": auth_sid_1})

        #print (response5.status_code)
        #print(response5.content)
        Assertions.assert_code_status(response5, 400)
        assert response5.content.decode("utf-8") == '{"error":"This user can only delete their own account."}'
        Assertions.assert_code_status(response6, 200)
        Assertions.assert_code_status(response7, 200)