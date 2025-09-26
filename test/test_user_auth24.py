# Позитивный тест на авторизацию + урок 26, 25, 24
# авторизуем пользователя и проверим что все прошло успешно
# POST Logs user into the system
# Params:
# @ email : string
# @ password : string
# https://playground.learnqa.ru/api/user/login
# GET Get user id you are authorizes as OR get 0 if not authorized
# https://playground.learnqa.ru/api/user/auth

import requests
import pytest


class TestUserAuth24:
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        # в ответе присутствует нужный хедер, нужный куки, id пользователя
        assert "auth_sid" in response1.cookies, "There is not auth cookies in the response"
        assert "x-csrf-token" in response1.headers, "There is not CSRF token header in the response"
        assert "user_id" in response1.json(), "There is not user id in the response"

        # запишем параметры в переменные
        self.auth_sid = response1.cookies.get("auth_sid")
        self.token = response1.headers.get("x-csrf-token")
        self.user_id_from_auth_method = response1.json()["user_id"]

    def test_user_auth24(self):

        #  передаем нужный нам токен и куки
        response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid}
                                 )
        assert "user_id" in response2.json(), "There is not user id in the 2 response "
        user_id_from_check_method = response2.json()["user_id"]
        assert self.user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user id from check method"

    # Негативный тест на авторизацию урок 25
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     headers={"x-csrf-token": self.token}
                                     )
        else:
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     cookies={"auth_sid": self.auth_sid}
                                     )
        assert "user_id" in response2.json(), "There is not user id in the second response"
        user_id_from_check_method = response2.json()["user_id"]
        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"
