"""
Ex11: Тест запроса на метод cookie
Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_cookie
Этот метод возвращает какую-то cookie с каким-то значением. Необходимо с помощью функции print() понять что за cookie и с каким значением,
и зафиксировать это поведение с помощью assert
Чтобы pytest не игнорировал print() необходимо использовать ключик "-s": python -m pytest -s my_test.py
"""

import requests


def test_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"

    response = requests.get(url)
    value_cookie = dict(response.cookies)
    print(value_cookie)
    assert value_cookie['HomeWork'] == 'hw_value', f"неверные куки"
    print(value_cookie['HomeWork'])