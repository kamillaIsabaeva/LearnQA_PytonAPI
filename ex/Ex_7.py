"""
Ex7: Запросы и методы
Сегодня задача должна быть попроще. У нас есть вот такой URL: https://playground.learnqa.ru/ajax/api/compare_query_type
Запрашивать его можно четырьмя разными HTTP-методами: POST, GET, PUT, DELETE
При этом в запросе должен быть параметр method. Он должен содержать указание метода, с помощью которого вы делаете запрос. Например, если вы делаете GET-запрос,
параметр method должен равняться строке ‘GET’. Если POST-запросом - то параметр method должен равняться ‘POST’. И так далее.
Надо написать скрипт, который делает следующее:
1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.
Не забывайте, что для GET-запроса данные надо передавать через params=
А для всех остальных через data=
Итогом должна быть ссылка на коммит со скриптом и ответы на все 4 вопроса.
"""
import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
methods = ['POST', 'GET', 'PUT', 'DELETE']
for method in methods:
    response_1 = requests.request(method, url)
    print(f"1) http-запрос любого типа без параметра {method} вывод: {response_1.text}")
# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response_2_1 = requests.head(url)
print("2) Делает http-запрос не из списка HEAD:", response_2_1.text)
response_2_2 = requests.patch(url)
print("2) Делает http-запрос не из списка PATCH:", response_2_2.text)

# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
for method in methods:
    if method == 'GET':
        response_3 = requests.get(url, params={"method": method})
    else:
        response_3 = requests.request(method, url, data={"method": method})
    print(f"3) Делает запрос с правильным значением {method} : {response_3.text}")

    # 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.

for method_request in methods:
    for method_params in methods:
        if method_request == 'GET':
            response_4 = requests.request(method_request, url, params={"method": method_params})
        else:
            response_4 = requests.request(method_request, url, data={"method": method_params})
        print(f"4) Реквест метод {method_request}, Передаваемый параметр {method_params},ответ {response_4.text}")
        if (method_request != method_params) and response_4.text == '{"success":"!"}':
            print(
                f" Тип запроса не совпадает со значением параметра Реквест метод {method_request}, Передаваемый параметр {method_params},ответ {response_4.text}")
        elif (method_request == method_params) and response_4.text != '{"success":"!"}':
            print(
                f"Типы совпадают, но сервер считает, что это не так Реквест метод {method_request}, Передаваемый параметр {method_params},ответ {response_4.text}")