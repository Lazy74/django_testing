from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, news_object',
    (
        ('news:home', None),
        ('users:signup', None),
        ('users:login', None),
        ('users:logout', None),
        ('news:detail', pytest.lazy_fixture('news')),
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name, news_object):
    if news_object is not None:
        news_object = news_object.pk,
    response = client.get(reverse(name, args=news_object))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'client, status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name, news_object',
    (
        ('news:edit', pytest.lazy_fixture('comment_pk')),
        ('news:delete', pytest.lazy_fixture('comment_pk')),
    )
)
def test_pages_availability_to_edit_delete_comment_auth_user(
    client,
    status,
    name,
    news_object,
):
    name = reverse(name, args=news_object)
    response = client.get(name)
    assert response.status_code == status


@pytest.mark.parametrize(
    'name, comment_obj',
    (
        ('news:edit', pytest.lazy_fixture('comment_pk')),
        ('news:delete', pytest.lazy_fixture('comment_pk')),
    )
)
def test_access_to_edit_delete_comment_by_anon(
    client,
    name,
    comment_obj,
):
    name = reverse(name, args=comment_obj)
    login_url = reverse('users:login')
    response = client.get(name)
    expected_url = f'{login_url}?next={name}'
    assertRedirects(response, expected_url)
