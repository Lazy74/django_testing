from datetime import datetime, timedelta
from time import sleep

import pytest
from django.test.client import Client
from django.conf import settings

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='User')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def comment_text():
    return (
        'Текст',
        'Еще текст',
    )


@pytest.fixture
def comment(author, news, comment_text):
    return Comment.objects.create(
        news=news,
        author=author,
        text=comment_text[0],
    )


@pytest.fixture
def comment_pk(comment):
    return comment.pk,


@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text[1]}


@pytest.fixture
def news_list():
    news = []
    today = datetime.today()
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news_piece = News.objects.create(
            title=f'Заголовок новости {index}',
            text=f'Текст {index}',
            date=today - timedelta(days=index),
        )
        news.append(news_piece)
    return news


@pytest.fixture
def comments_list(author, news):
    now = datetime.now()
    comments = []
    for index in range(2):
        sleep(0.1)
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Коментарий {index}',
            created=now + timedelta(minutes=index)
        )
        comments.append(comment)
    return comments
