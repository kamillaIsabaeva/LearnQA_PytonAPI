# Урок 23 Параметризованный тесты
import pytest
import requests


class TestFirstApi:
    names = [
        ("Vitalii"),
        ("Arseniy"),
        ("")
    ]

    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        # GET This API call says hello by name you specify
        # # Params:
        # @ name : string - Default "someone"
        # # https://playground.learnqa.ru/api/hello
        url = "https://playground.learnqa.ru/api/hello"
        data = {'name': name}

        response = requests.get(url  # ,params=data
                                )  # делаем запрос и помещаем ответ в переменную response

        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()  # проверка, что поле найдено в словаре
        assert "answer" in response_dict, "There is not field 'answer' in the response"

        expected_response_test = f"Hello, {name}"
        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_test, "Actual text in the response is not correct"
