import pytest
from pytest import lazy_fixture as lf
from pytest_django.asserts import assertRedirects
from http import HTTPStatus


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, status',
    (
        (lf('url_home'), lf('client'), HTTPStatus.OK),
        (lf('url_signup'), lf('client'), HTTPStatus.OK),
        (lf('url_login'), lf('client'), HTTPStatus.OK),
        (lf('url_logout'), lf('client'), HTTPStatus.OK),
        (lf('url_detail'), lf('client'), HTTPStatus.OK),
        (lf('url_edit'), lf('author_client'), HTTPStatus.OK),
        (lf('url_delete'), lf('author_client'), HTTPStatus.OK),
        (lf('url_edit'), lf('admin_client'), HTTPStatus.NOT_FOUND),
        (lf('url_delete'), lf('admin_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.django_db
def test_page_accessibility_for_anonymous_and_auth_users(
    reverse_url, parametrized_client, status
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'variable_url',
    (
        (lf('url_edit')),
        (lf('url_delete')),
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
