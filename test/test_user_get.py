"""
Ex16: Запрос данных другого пользователя
На занятиях в классе TestUserGet мы писали тест на запрос, показывающий данные пользователя. Мы покрыли тестами два кейса:
- неавторизованный запрос на данные - там мы получили только username
- авторизованный запрос - мы были авторизованы пользователем с ID 2 и делали запрос для получения данных того же пользователя,
в этом случае мы получали все поля
В этой задаче нужно написать тест, который авторизовывается одним пользователем, но получает данные другого (т.е. с другим ID).
И убедиться, что в этом случае запрос также получает только username, так как мы не должны видеть остальные данные чужого пользователя.
"""
import requests
import pytest
import random
import string

from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):  # неавторизованный пользователь
        response = requests.get("https://playground.learnqa.ru/api/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'password': '1234',
            'email': 'vinkotov@example.com'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_other_user_auth(self):
        data = {
            'password': '1234',
            'email': 'vinkotov@example.com'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = ((self.get_json_value(response1, "user_id")) + 1)

        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        if (response2.status_code == 200):
            Assertions.assert_json_has_key(response2, "username")
            Assertions.assert_json_has_not_key(response2, "email")
            Assertions.assert_json_has_not_key(response2, "firstName")
            Assertions.assert_json_has_not_key(response2, "lastName")
        else:
            print('User not found with user_id =',{user_id_from_auth_method})



