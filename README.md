## Тестовое задание

Тестовое задание выполнил Федоров Роман rfedorov@linkentools.com 

## Важно
Перед тем как взять задание в работу, оцените его по времени и сообщите нам.
Не нужно зарываться в него на неделю чтобы "вышлифовывать" всё до блеска, но все
заявленные требования должны быть выполнены. Также нам важно соблюдение PEP8.
После реализации нужно прокомментировать предложенное решение, выбранные
механизмы хранения и обработки данных, оценить плюсы и минусы.
Решение должно работать на больших объемах данных.
Исходный код проекта нужно разместить на github или bitbucket.
В исходных текстах и имени проекта не должно быть упоминания компании ***.
Предполагаем, что в системе одна валюта - USD.

## Задание
Необходимо разработать веб-приложение простой платежной системы (для упрощения,
все переводы и зачисления без комиссии).
Требования:
1. Каждый клиент в системе имеет один "кошелек", содержащий денежные средства.
2. Сохраняется информация о кошельке и остатке средств на нем.
3. Клиенты могут делать друг другу денежные переводы.
4. Сохраняется информация о всех операциях на кошельке клиента.
5. Проект представляет из себя HTTP API, содержащее основные операции по "кошелькам".
6. HTTP API должен представлять следующие интерфейсы:
* создание клиента с кошельком.
* зачисление денежных средств на кошелек клиента
* перевод денежных средств с одного кошелька на другой.

## Основные файлы

[`billing/models.py`](billing/models.py) - User and Payment models

[`billing/user.py`](billing/user.py) - user API

[`billing/payment.py`](billing/payment.py) - payment API

[`billing_tests/test_user.py`](billing_tests/test_user.py) - user tests

[`billing_tests/test_payment.py`](billing_tests/test_payment.py) - payment tests

## Проверка конкурентной записи

[![проверка конкурентной записи](https://img.youtube.com/vi/963Zp8ocT1U/0.jpg)](https://www.youtube.com/watch?v=963Zp8ocT1U)

## Installation

```bash
docker-compose up -d
docker-compose run --rm web pytest
```

Проверьте, что сайт заработал http://0.0.0.0:8000/docs#/

## Development

```bash
pipenv --python 3.7
pipenv shell
pip install poetry
poetry install
docker-compose up
```
