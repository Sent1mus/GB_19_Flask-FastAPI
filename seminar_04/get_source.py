# Наработки по парсингу сайта на предмет images

from bs4 import BeautifulSoup
import requests
import base64
import time

# Использование объекта Session для обработки cookies
session = requests.Session()

# Получение HTML-кода страницы
url = 'https://www.wallpaperflare.com/'
response = session.get(url)
html_content = response.text

# Создание объекта BeautifulSoup с полученным HTML-кодом
soup = BeautifulSoup(html_content, 'html.parser')

# Поиск всех элементов <li>
li_elements = soup.find_all('li')

# Ограничиваем количество обрабатываемых элементов до 50
with open('images.txt', 'w', encoding='utf-8') as file:
    for li in li_elements[:1]:
        # Поиск элемента <figure> внутри <li>
        figure = li.find('figure')
        if figure:
            # Поиск ссылки внутри <figure>
            link = figure.find('a')
            if link:
                # Добавление к ссылке /download/2560x1440
                new_url = link['href']
                new_url += '/download/2560x1440'
                print(f"{new_url}")
                new_response = session.get(new_url)
                new_html_content = new_response.text
                new_soup = BeautifulSoup(new_html_content, 'html.parser')

                # Находим последний элемент <img> внутри <section> внутри <body><main class="resp" id="main">
                main_section = new_soup.find('body').find('main', {'class': 'resp', 'id': 'main'})
                if main_section:
                    last_img = main_section.find_all('img')[-1] # Последний элемент <img>
                    if last_img and 'src' in last_img.attrs:
                        img_src = last_img['src']
                        # Проверяем, является ли src base64
                        if img_src.startswith('data:image/'):
                            # Извлекаем и декодируем base64
                            base64_data = img_src.split(',')[1]
                            decoded_data = base64.b64decode(base64_data)
                            # Выводим декодированные данные
                            print(f"Decoded image data: {decoded_data}")
                        else:
                            print(f"Image src: {img_src}")
