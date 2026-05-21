import requests
from bs4 import BeautifulSoup

# URL страницы
url = 'https://habr.com/ru/companies/gnivc/news/1037538/'

# Заголовки User-Agent, чтобы имитировать запрос от браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # Отправляем GET-запрос
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Парсим HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. Извлекаем название статьи (из тега <title>)
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
        # Обрезаем " — Хабр" или подобное в конце, если есть
        if ' — ' in title:
            title = title.split(' — ')[0]
    else:
        title = "Название не найдено"

    # 2. Извлекаем автора (РАБОТАЮЩИЙ способ из вашего первого кода)
    author_tag = soup.find('a', attrs={'data-test-id': 'authorLink'})
    if not author_tag:
        # Альтернативный поиск по классу
        author_tag = soup.find('span', class_='tm-user-info__user')
    author = author_tag.text.strip() if author_tag else "Автор не найден"

    # 3. Извлекаем дату публикации (из атрибута datetime тега <time>)
    date_tag = soup.find('time')
    if date_tag and date_tag.get('datetime'):
        date = date_tag.get('datetime')
        # Приводим к формату ГГГГ-ММ-ДД
        date = date.split('T')[0] if 'T' in date else date
    else:
        date = "Дата не найдена"

    # Выводим результаты
    print(f"Название статьи: {title}")
    print(f"Автор: {author}")
    print(f"Дата публикации: {date}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")