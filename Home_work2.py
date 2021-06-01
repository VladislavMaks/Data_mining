# Необходимо обойти все записи в блоге и извлеч из них информацию следующих полей:
# url страницы материала
# Заголовок материала
# Первое изображение материала (Ссылка)
# Дата публикации (в формате datetime)
# имя автора материала
# ссылка на страницу автора материала
# комментарии в виде (автор комментария и текст комментария)
# Структуру сохраняем в MongoDB

import requests
from bs4 import BeautifulSoup
import datetime
import pymongo

url = 'https://gb.ru/posts/kak-najti-rabotu-v-mobilnoj-razrabotke-i-ne-boyatsya-scrum'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
comments_link = soup.find('comments').attrs.get("commentable-id")


def parse_post():
    tittle = soup.find('h1', class_='blogpost-title')
    image_href = soup.find('img').get('src')
    post_date = soup.find('time', class_='text-md text-muted m-r-md').get('datetime')[:10]
    post_date = datetime.datetime.strptime(post_date, '%Y-%m-%d').date()
    author_name = soup.find('div', class_='text-lg text-dark')
    author_link = soup.find('div', class_='col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v').find('a').get('href')
    result = (f'URL:{url}\nЗаголовок: {tittle.text}\nПервое изображение материала: {image_href}\n'
              f'Дата публикации: {post_date}\nИмя автора: {author_name.text}\n'
              f'Ссылка на автора: {author_link}')
    return result


def get_comments():
    api_path = f"https://gb.ru/api/v2/comments?commentable_type=Post&commentable_id={comments_link}&order=desc"
    response = requests.get(api_path)
    soup = BeautifulSoup(response.text, 'lxml')
    comments = soup.find_all('p')
    a = []
    for comment in comments[1:]:
        a.append(comment.text)
    return a


print(parse_post())
print(get_comments())
