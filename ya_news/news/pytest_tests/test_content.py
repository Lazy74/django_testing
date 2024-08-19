import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('news_list')
def test_news_count(client, url_home):
    response = client.get(url_home)
    assert (
        response.context['object_list'].count()
        <= settings.NEWS_COUNT_ON_HOME_PAGE
    )


@pytest.mark.usefixtures('news_list')
def test_news_order(client, url_home):
    response = client.get(url_home)
    news_dates = [news.date for news in response.context['object_list']]
    ordered_dates = sorted(news_dates, reverse=True)
    assert news_dates == ordered_dates


@pytest.mark.usefixtures('comments_list')
def test_comments_order(client, url_detail):
    response = client.get(url_detail)
    all_comments = response.context['news'].comment_set.all()
    assert list(all_comments) == list(all_comments.order_by('created'))


@pytest.mark.parametrize(
    'user, access_form',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_form_is_shown_to_correct_user(
    user,
    access_form,
    url_detail,
):
    response = user.get(url_detail)
    assert ('form' in response.context) == access_form
    if access_form:
        assert isinstance(response.context['form'], CommentForm)
