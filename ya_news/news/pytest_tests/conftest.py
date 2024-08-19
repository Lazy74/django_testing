from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.conf import settings

from news.models import Comment, News

COMMENT_TEXTS = (
    'Текст',
    'Еще текст',
)

FORM_DATA = {'text': COMMENT_TEXTS[1]}


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
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXTS[0],
    )


@pytest.fixture
def news_list():
    today = datetime.today()
    all_news = [
        News(
            title=f'Заголовок новости {index}',
            text=f'Текст {index}',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comments_list(author, news):
    now = datetime.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Коментарий {index}',
        )
        comment.created = now - timedelta(days=index)
