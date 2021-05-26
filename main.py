# определяем список хабов, которые нам интересны
DESIRED_HUBS = ['дизайн', 'фото', 'web', 'python', 'devops-инженеры', 'threat', 'javascript']

import requests
from bs4 import BeautifulSoup
from pprint import pprint
if __name__ is 'main':
    # получаем страницу с самыми свежими постами
    ret = requests.get('https://habr.com/ru/all/')
    soup = BeautifulSoup(ret.text, 'html.parser')

    # извлекаем посты
    posts = soup.find_all('article', class_='post')
    for post in posts:
        post_id = post.parent.attrs.get('id')
        # если идентификатор не найден, это что-то странное, пропускаем
        # ну или если это не пост, а что-то иное
        if not post_id or post_id == 'effect':
            continue
        post_id = post_id.split('_')[-1]
        # print('Post:', post_id)

        # извлекаем хабы поста
        hubs = post.find_all('a', class_='hub-link')
        dict = {}
        for hub in hubs:
            hub_lower = hub.text.lower()
            # ищем вхождение желаемого хаба
            if any([hub_lower in desired for desired in DESIRED_HUBS]):
                title_element = post.find('a', class_='post__title_link')
                dict[post_id] = ("Найдено в Hub's", title_element.text, title_element.attrs.get('href'))
        # извлекаем наименование поста
        hubs = post.find_all('a', class_='post__title_link')
        for hub in hubs:
            hub_lowers = hub.text.lower()
            hub_lowers = hub_lowers.split()
            for hub_lower in hub_lowers:
                # ищем вхождение желаемого хаба
                if hub_lower in DESIRED_HUBS:
                    title_element = post.find('a', class_='post__title_link')
                    dict[post_id] = ('Найдено в Title', title_element.text, title_element.attrs.get('href'))
        # извлекаем preview поста
        hubs = post.find_all('div', class_='post__text-html')
        for hub in hubs:
            hub_lowers = hub.text.lower()
            hub_lowers = hub_lowers.split()
            for hub_lower in hub_lowers:
                # ищем вхождение желаемого хаба
                if hub_lower in DESIRED_HUBS:
                    title_element = post.find('a', class_='post__title_link')
                    dict[post_id] = ('Найдено в Preview', title_element.text, title_element.attrs.get('href'))
        pprint(dict)