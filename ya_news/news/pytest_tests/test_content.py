import pytest

from django.urls import reverse
from django.conf import settings

URL = reverse('news:home')


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_count(client):
    response = client.get(URL)
    assert (
        response.context['object_list'].count()
        <= settings.NEWS_COUNT_ON_HOME_PAGE
    )


@pytest.mark.django_db
@pytest.mark.usefixtures('news_list')
def test_news_order(client):
    response = client.get(URL)
    news_dates = [news.date for news in response.context['object_list']]
    ordered_dates = sorted(news_dates, reverse=True)
    assert news_dates == ordered_dates


@pytest.mark.usefixtures('comments_list')
def test_comments_order(client, news):
    response = client.get(reverse('news:detail', args=(news.pk,)))
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
    news,
):
    response = user.get(reverse('news:detail', args=(news.pk,)))
    assert ('form' in response.context) == access_form
