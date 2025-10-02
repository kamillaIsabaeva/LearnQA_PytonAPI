"""
Ex12: Тест запроса на метод header
Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_header
Этот метод возвращает headers с каким-то значением. Необходимо с помощью функции print() понять что за headers и с каким значением,
и зафиксировать это поведение с помощью assert
Чтобы pytest не игнорировал print() необходимо использовать ключик "-s": python -m pytest -s my_test.py
"""
import requests


def test_header():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)
    headers_dict = dict(response.headers)
    for header, value in headers_dict.items():
        print(header, value)
    assert 'x-secret-homework-header' in headers_dict, f"Заголовка нет"
    assert headers_dict[
               'x-secret-homework-header'] == 'Some secret value', f"НЕ x-secret-homework-header != Some secret value  "
    assert headers_dict['Content-Type'] == 'application/json', f"НЕ Сontent-Type != application/json  "
    assert headers_dict['Content-Length'] == '15', f"НЕ Сontent-Length != 15  "
    assert headers_dict['Connection'] == 'keep-alive', f"НЕ Connection != keep-alive  "
    assert headers_dict['Keep-Alive'] == 'timeout=10', f"НЕ Keep-Alive != timeout=10 "
    assert headers_dict['Server'] == 'Apache', f"НЕ Server != aApache  "
    assert headers_dict['Cache-Control'] == 'max-age=0', f"НЕ Cache-Control != max-age=0  "