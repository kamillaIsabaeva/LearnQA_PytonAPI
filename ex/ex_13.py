"""
Ex13: User Agent
User Agent - это один из заголовков, позволяющий серверу узнавать, с какого девайса и браузера пришел запрос.
Он формируется автоматически клиентом, например браузером.
Определив, с какого девайса или браузера пришел к нам пользователь мы сможем отдать ему только тот контент, который ему нужен.
Наш разработчик написал метод: https://playground.learnqa.ru/ajax/api/user_agent_check
Метод определяет по строке заголовка User Agent следующие параметры:
device - iOS или Android
browser - Chrome, Firefox или другой браузер
platform - мобильное приложение или веб
Если метод не может определить какой-то из параметров, он выставляет значение Unknown.
Наша задача написать параметризированный тест. Этот тест должен брать из дата-провайдера User Agent и ожидаемые значения, GET-делать запрос с этим User Agent и убеждаться, что результат работы нашего метода правильный - т.е. в ответе ожидаемое значение всех трех полей.
Список User Agent и ожидаемых значений можно найти по этой ссылке: https://gist.github.com/KotovVitaliy/138894aa5b6fa442163561b5db6e2e26
Пример того, как должен выглядеть запрос с указанным User Agent:
requests.get(
    "https://playground.learnqa.ru/ajax/api/user_agent_check",
   headers={"User-Agent": "Some value here"}
)
На самом деле метод не всегда работает правильно. Ответом к задаче должен быть список из тех User Agent, которые вернули неправильным хотя бы один параметр, с указанием того, какой именно параметр неправильный.
"""
import pytest
import requests

User_Agent_datas = [
    {
        'User_Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Expected_values': {'platform': 'Mobile',
                            'browser': 'No',
                            'device': 'Android'
                            }
    },
    {
        'User_Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
        'Expected_values': {
            'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'
        }
    },
    {
        'User_Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Expected_values':
            {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}
    },
    {
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
        'Expected_values':
            {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}
    },
    {
        'User_Agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'Expected_values': {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
    }
]


@pytest.mark.parametrize('User_Agent_data', User_Agent_datas)
def test_user_agent_check(User_Agent_data):
    incorrect_user_agents = []
    user_agent = User_Agent_data['User_Agent']
    expected = User_Agent_data['Expected_values']

    response = requests.get(
        "https://playground.learnqa.ru/ajax/api/user_agent_check",
        headers={"User-Agent": user_agent}
    )

    response_json = response.json()

    # Проверяем каждый параметр отдельно
    for expected_data in ['platform', 'browser', 'device']:
        actual_value = response_json.get(expected_data)
        expected_value = expected[expected_data]
        print (actual_value, expected_value)

        if actual_value != expected_value:
            incorrect_user_agents.append({
                'User-Agent': user_agent,
                'parameter': expected_data,
                'expected': expected_value,
                'got': actual_value
            })

    assert not incorrect_user_agents, (
        f"Для User-Agent '{user_agent}'/'{expected}' обнаружены неправильные параметры: {incorrect_user_agents}"
    )
