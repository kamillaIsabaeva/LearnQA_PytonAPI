# Ex4: GET-запрос

# В проекте создать скрипт, который отправляет GET-запрос по адресу: https://playground.learnqa.ru/api/get_text
# Затем с помощью функции print вывести содержимое текста в ответе на запрос.
# Когда скрипт будет готов - давайте его закоммитим в наш репозиторий.
# Результатом должна быть ссылка на коммит.


import requests  # импорт библиотеки

response = requests.get(
    "https://playground.learnqa.ru/api/get_text")  # вызов функции типом get
print(response.text)
