import requests
from bs4 import BeautifulSoup

# 1. Отправляем GET-запрос к сайту
url = "https://quotes.toscrape.com/"
try:
    response = requests.get(url)
    response.raise_for_status()  # Проверяем, успешен ли запрос

    # 2. Парсим HTML-содержимое страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3. Находим первую цитату на странице
    # Каждая цитата находится в div с классом 'quote'
    first_quote_div = soup.find('div', class_='quote')

    if first_quote_div:
        # Извлекаем текст цитаты из span с классом 'text'
        quote_text = first_quote_div.find('span', class_='text').text
        # Извлекаем имя автора из small с классом 'author'
        author_name = first_quote_div.find('small', class_='author').text

        # 4. Выводим результат в нужном формате
        print(f"Цитата: {quote_text}")
        print(f"Автор: {author_name}")
    else:
        print("Не удалось найти цитату на странице.")

except requests.exceptions.RequestException as e:
    print(f"Произошла ошибка при запросе к сайту: {e}")