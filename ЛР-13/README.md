# ЛР-13

##  Конфигурация тестирования
- Инструмент: Locust 2.44.4
- Конфигурация: 10 пользователей, Ramp up: 2
- Тестируемые фреймворки: FastAPI, Flask, Tornado, Sanic

## Результаты тестирования

- ### FastAPI (порт 8000)
![alt text](<FastAPI .png>)
![alt text](<Снимок экрана 2026-06-21 в 17.31.24.png>)

- ### Flask (порт 5005)
![alt text](app_flask.png)
![alt text](<Снимок экрана 2026-06-21 в 17.37.23.png>)

- ### Tornado (порт 8888)
![alt text](Tornado.png)

- ### Sanic (порт 8001)
![alt text](Sanic.png)

## Сравнительный анализ

| Фреймворк | /high_cpu_endpoint (P95) | /high_cpu_endpoint_fixed (P95) | Общий RPS | Ошибки |
|-----------|--------------------------|-------------------------------|-----------|--------|
| **FastAPI** | 370 ms | 370 ms | 0.7 | 0% |
| **Flask** | 81 ms | 82 ms | 7.4 | 0% |
| **Tornado** | 75 ms | 78 ms | 7.5 | 0% |
| **Sanic** | 72 ms | 80 ms | 7.2 | 0% |















