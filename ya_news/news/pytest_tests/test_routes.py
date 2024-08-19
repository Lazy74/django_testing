from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'variable_url',
    (
        pytest.lazy_fixture('url_home'),
        pytest.lazy_fixture('url_signup'),
        pytest.lazy_fixture('url_login'),
        pytest.lazy_fixture('url_logout'),
        pytest.lazy_fixture('url_detail'),
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, variable_url):
    response = client.get(variable_url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'client, status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'variable_url',
    (
        (pytest.lazy_fixture('url_edit')),
        (pytest.lazy_fixture('url_delete')),
    )
)
def test_pages_availability_to_edit_delete_comment_auth_user(
    client,
    status,
    variable_url,
):
    response = client.get(variable_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'variable_url',
    (
        (pytest.lazy_fixture('url_edit')),
        (pytest.lazy_fixture('url_delete')),
    )
)
def test_access_to_edit_delete_comment_by_anon(
    client,
    variable_url,
    url_login,
):
    response = client.get(variable_url)
    expected_url = f'{url_login}?next={variable_url}'
    assertRedirects(response, expected_url)
