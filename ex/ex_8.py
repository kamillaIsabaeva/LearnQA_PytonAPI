"""
Ex8: Токены
Иногда API-метод выполняет такую долгую задачу, что за один HTTP-запрос от него нельзя сразу получить готовый ответ.
Это может быть подсчет каких-то сложных вычислений или необходимость собрать информацию по разным источникам.
В этом случае на первый запрос API начинает выполнения задачи, а на последующие ЛИБО говорит, что задача еще не готова,
ЛИБО выдает результат. Сегодня я предлагаю протестировать такой метод.
Сам API-метод находится по следующему URL: https://playground.learnqa.ru/ajax/api/longtime_job
Если мы вызываем его БЕЗ GET-параметра token, метод заводит новую задачу, а в ответ выдает нам JSON со следующими полями:
* seconds - количество секунд, через сколько задача будет выполнена
* token - тот самый токен, по которому можно получить результат выполнения нашей задачи
Если же вызвать метод, УКАЗАВ GET-параметром token, то мы получим следующий JSON:
* error - будет только в случае, если передать token, для которого не создавалась задача. В этом случае в ответе будет следующая надпись - No job linked to this token
* status - если задача еще не готова, будет надпись Job is NOT ready, если же готова - будет надпись Job is ready
* result - будет только в случае, если задача готова, это поле будет содержать результат
Наша задача - написать скрипт, который делал бы следующее:
1) создавал задачу
2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
"""
import requests
import json
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)
obj = json.loads(response.text)
token_params = obj['token']
if (token_params != ''):
    print("Задача создана ", obj)
    response2 = requests.get(url, params={"token": token_params})
    obj2 = json.loads(response2.text)
    if 'error' not in obj2:
        status_params = obj2['status']
        time_params = obj['seconds']
        if (status_params == 'Job is NOT ready'):
            print('Ждем завершение задачи, время ожидания ', time_params)
            time.sleep(time_params)
            response3 = requests.get(url,
                                     params={"token": token_params})
            obj3 = json.loads(response3.text)
            status_result = obj3['status']
            result_result = obj3['result']
            if (status_result == 'Job is ready' and obj3['result']):
                print('Ура задача готова', status_result, result_result)
            else:
                print('Что то пошло не так ')
        else:
            print({'No job linked to this token'})
    else:
        print('Token не существует error', obj2['error'])
else:
    print('Token не создан')
