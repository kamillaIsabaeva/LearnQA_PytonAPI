from numpy import error_message
from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value,
                                  error_message):  # значение внутри json доступно по определенному имени и равно ожидаемому значению
        try:
            reponse_as_disct = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json Format. Response text is '{response.text}'"

            assert name is response_as_dict, f"Response JSON doesn't have key '{name}"
            assert response_as_disc[name] == expected_value, error_message
