from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import FORM_DATA

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
    client,
    url_detail,
):
    comment_count = Comment.objects.count()
    client.post(url_detail, data=FORM_DATA)
    assert comment_count == Comment.objects.count()


def test_auth_user_can_create_comment(
    author_client,
    url_detail,
):
    buff_comment_count = Comment.objects.count()
    author_client.post(url_detail, data=FORM_DATA)
    assert Comment.objects.count() == buff_comment_count + 1
    assert Comment.objects.get().text == FORM_DATA['text']


def test_user_cant_use_bad_words(author_client, url_detail):
    response = author_client.post(
        url_detail,
        data={'text': choice(BAD_WORDS)},
    )
    assert Comment.objects.count() == 0
    assertFormError(
        response,
        'form',
        'text',
        WARNING,
    )


@pytest.mark.parametrize(
    'user, delta_count',
    (
        (pytest.lazy_fixture('author_client'), 1),
        (pytest.lazy_fixture('admin_client'), 0),
    )
)
def test_can_delete_comment(
    user,
    delta_count,
    url_delete,
):
    start_comments_count = Comment.objects.count()
    user.post(url_delete)
    end_comments_count = Comment.objects.count()
    assert start_comments_count == end_comments_count + delta_count


@pytest.mark.parametrize(
    'user, can_edit_comment , expected_status',
    (
        (
            pytest.lazy_fixture('admin_client'), False, HTTPStatus.NOT_FOUND,
        ),
        (
            pytest.lazy_fixture('author_client'), True, HTTPStatus.FOUND,
        ),
    )
)
def test_edit_comment(
    user,
    can_edit_comment,
    expected_status,
    comment,
    url_edit,
):
    originalValue = Comment.objects.get(pk=comment.pk)
    response = user.post(
        url_edit,
        data=FORM_DATA
    )
    targetValue = Comment.objects.get(pk=comment.pk)
    assert response.status_code == expected_status
    if can_edit_comment:
        assert targetValue.text == FORM_DATA['text']
    else:
        assert targetValue.text == originalValue.text
