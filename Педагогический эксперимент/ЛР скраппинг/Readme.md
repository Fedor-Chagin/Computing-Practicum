
## ЛР-2 Pillow

Программы работают по принципу двухэтапного сбора данных. Сначала скрипт проходит по страницам списка, собирает только ФИО и ссылки на профили, после чего заходит на каждый профиль, извлекает email и/или телефон (при наличии).

```py
import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = 'https://atlas.herzen.spb.ru'

# Создание сессии с заголовками как у браузера
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
})

def get_teacher_links(page_num):
    """Собирает ФИО и ссылки на профили со страницы списка"""
    url = f'https://atlas.herzen.spb.ru/teachers?page={page_num}'
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    teachers = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/teachers/' in href and href != '/teachers':
            name = link.get_text(strip=True)
            if name and len(name) > 2 and name != 'Преподаватели':
                full_url = urljoin(BASE_URL, href)
                teachers.append({'name': name, 'url': full_url})
    
    # Убираем дубликаты по URL
    unique_teachers = []
    seen_urls = set()
    for teacher in teachers:
        if teacher['url'] not in seen_urls:
            seen_urls.add(teacher['url'])
            unique_teachers.append(teacher)
    
    return unique_teachers

def parse_profile(profile_url, name):
    """Парсит страницу профиля - ищет email и телефон"""
    try:
        response = session.get(profile_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        email = ''
        phone = ''
        
        for elem in soup.find_all('h1', class_='text-m'):
            text = elem.get_text(strip=True)
            if text:
                if '@' in text:
                    email = text
                elif text.startswith('+7') or text.startswith('8'):
                    phone = text
        
        return phone, email
        
    except Exception as e:
        print(f"Ошибка при парсинге {name}: {e}")
        return '', ''

def main():
    print("Сбор данных о преподавателях...")
    
    all_teachers = []
    
    # Этап 1: Сбор ссылок (страницы 1-54)
    for page in range(1, 55):
        print(f"Обработка страницы {page}/54...")
        teachers = get_teacher_links(page)
        print(f"  Найдено {len(teachers)} преподавателей")
        all_teachers.extend(teachers)
        time.sleep(0.5)
    
    print(f"\nВсего найдено преподавателей: {len(all_teachers)}")
    
    # Этап 2: Парсинг профилей
    results = []
    for i, teacher in enumerate(all_teachers, 1):
        print(f"Обработка [{i}/{len(all_teachers)}]: {teacher['name']}")
        phone, email = parse_profile(teacher['url'], teacher['name'])
        results.append({
            'ФИО': teacher['name'],
            'Ссылка на профиль': teacher['url'],
            'Почта': email,
            'Телефон': phone
        })
        time.sleep(0.2)
    
    # Сохранение в CSV
    filename = 'list.csv'
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['ФИО', 'Ссылка на профиль', 'Почта', 'Телефон'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nСохранено {len(results)} записей в {filename}")

if __name__ == "__main__":
    main()
```
![alt text](<Снимок экрана 2026-05-30 в 03.12.16.png>)
![alt text](<Снимок экрана 2026-05-30 в 03.16.08.png>)




```py
import requests
from lxml import html
import csv
import time
from urllib.parse import urljoin

BASE_URL = 'https://atlas.herzen.spb.ru'

# Создание сессии с заголовками как у браузера
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
})

def get_teacher_links_lxml(page_num):
    """Собирает ФИО и ссылки на профили со страницы списка (lxml)"""
    url = f'https://atlas.herzen.spb.ru/teachers?page={page_num}'
    response = session.get(url)
    tree = html.fromstring(response.text)
    
    teachers = []
    
    # XPath: ищем все ссылки, содержащие '/teachers/', исключая ссылку на сам список
    for link in tree.xpath('//a[contains(@href, "/teachers/") and not(@href="/teachers")]'):
        href = link.get('href')
        name = link.text_content().strip()
        
        if name and len(name) > 2 and name != 'Преподаватели':
            full_url = urljoin(BASE_URL, href)
            teachers.append({'name': name, 'url': full_url})
    
    # Убираем дубликаты по URL
    unique_teachers = []
    seen_urls = set()
    for teacher in teachers:
        if teacher['url'] not in seen_urls:
            seen_urls.add(teacher['url'])
            unique_teachers.append(teacher)
    
    return unique_teachers

def parse_profile_lxml(profile_url, name):
    """Парсит страницу профиля - ищет email и телефон (lxml)"""
    try:
        response = session.get(profile_url, timeout=10)
        tree = html.fromstring(response.text)
        
        email = ''
        phone = ''
        
        # XPath: ищем все h1 с классом text-m
        for elem in tree.xpath('//h1[@class="text-m"]'):
            text = elem.text_content().strip()
            if text:
                if '@' in text:
                    email = text
                elif text.startswith('+7') or text.startswith('8'):
                    phone = text
        
        return phone, email
        
    except Exception as e:
        print(f"Ошибка при парсинге {name}: {e}")
        return '', ''

def main():
    print("Начинаем сбор данных о преподавателях (способ: lxml)...")
    
    all_teachers = []
    
    # Этап 1: Сбор ссылок (страницы 1-54)
    for page in range(1, 55):
        print(f"Обработка страницы {page}/54...")
        teachers = get_teacher_links_lxml(page)
        print(f"  Найдено {len(teachers)} преподавателей")
        all_teachers.extend(teachers)
        time.sleep(0.5)
    
    print(f"\nВсего найдено преподавателей: {len(all_teachers)}")
    
    # Этап 2: Парсинг профилей
    results = []
    for i, teacher in enumerate(all_teachers, 1):
        print(f"Обработка [{i}/{len(all_teachers)}]: {teacher['name']}")
        phone, email = parse_profile_lxml(teacher['url'], teacher['name'])
        results.append({
            'ФИО': teacher['name'],
            'Ссылка на профиль': teacher['url'],
            'Почта': email,
            'Телефон': phone
        })
        time.sleep(0.2)
    
    # Сохранение в CSV
    filename = 'list_lxml.csv'
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['ФИО', 'Ссылка на профиль', 'Почта', 'Телефон'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nСохранено {len(results)} записей в {filename}")

if __name__ == "__main__":
    main()
```
![alt text](<Снимок экрана 2026-05-30 в 03.42.05.png>)
![alt text](<Снимок экрана 2026-05-30 в 03.42.18.png>)

```
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 lxml
python3 main.py
```