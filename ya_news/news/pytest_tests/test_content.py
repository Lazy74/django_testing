"""
В файле test_content.py:
    — Количество новостей на главной странице — не более 10.
    — Новости отсортированы от самой свежей к самой старой.
      Свежие новости в начале списка.
    — Комментарии на странице отдельной новости отсортированы
      в хронологическом порядке: старые в начале списка, новые — в конце.
    — Анонимному пользователю недоступна форма для отправки комментария
      на странице отдельной новости, а авторизованному доступна.
"""

import pytest

from django.urls import reverse

from news.pytest_tests.conftest import NEWS_COUNT_ON_HOME_PAGE

URL = reverse('news:home')


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_count(client):
    response = client.get(URL)
    assert response.context['object_list'].count() <= NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_order(client):
    response = client.get(URL)
    news_dates = [news.date for news in response.context['object_list']]
    ordered_dates = sorted(news_dates, reverse=True)
    assert news_dates == ordered_dates


@pytest.mark.usefixtures('comments_list')
def test_comments_order(client, news_pk):
    response = client.get(reverse('news:detail', args=news_pk))
    all_comments = response.context['news'].comment_set.all()
    assert list(all_comments) == list(all_comments.order_by('created'))


@pytest.mark.parametrize(
    'user, access_form',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
@pytest.mark.django_db
def test_form_is_shown_to_correct_user(
    user,
    access_form,
    news_pk,
):
    response = user.get(reverse('news:detail', args=news_pk))
    assert ('form' in response.context) == access_form
