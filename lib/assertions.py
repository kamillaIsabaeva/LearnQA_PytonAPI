from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value,
                                  error_message):  # значение внутри json доступно по определенному имени и равно ожидаемому значению
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response,
                            name):  # проверяет, что JSON содержит указанное поле
        try:

            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response,
                             names: list):  # проверяет, что JSON  содержит все указанные поля
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"
        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_code_status(response: Response,
                           expected_status_code):  # проверяет статус код
        assert response.status_code == expected_status_code, f"Unexpected status code! Expected: {expected_status_code}. Actual:{response.status_code}"

    @staticmethod
    def assert_json_has_not_key(response: Response,
                                name):  # проверяет, что JSON не содержит указанное поле
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"
        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}'. But it's present"
