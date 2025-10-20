# Позитивный тест на авторизацию + урок 26, 25, 24
# авторизуем пользователя и проверим что все прошло успешно
# POST Logs user into the system
# Params:
# @ email : string
# @ password : string
# https://playground.learnqa.ru/api/user/login
# GET Get user id you are authorizes as OR get 0 if not authorized
# https://playground.learnqa.ru/api/user/auth

import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

from lib.my_requests import MyRequests
import allure
@allure.label("owner", "Kamilla")
@allure.epic("Authorization cases")
@allure.id("1")
class TestUserAuth24(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")
        # в ответе присутствует нужный хедер, нужный куки, id пользователя

    @allure.description("This tets successfully user by email and password")
    @allure.story("positive")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_auth24(self):

        #  передаем нужный нам токен и куки
        response2 = MyRequests.get("/user/auth",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid}
                                   )
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.description("This test checks authorization status without sending auth cookie or token ")
    @allure.story("negative")
    @allure.severity(allure.severity_level.CRITICAL)
    # Негативный тест на авторизацию урок 25
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            response2 = MyRequests.get("/user/auth",
                                       headers={"x-csrf-token": self.token}
                                       )
        else:
            response2 = MyRequests.get("/user/auth",
                                       cookies={"auth_sid": self.auth_sid}
                                       )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
