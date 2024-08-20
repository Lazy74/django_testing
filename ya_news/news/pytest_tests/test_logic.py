from http import HTTPStatus
from random import choice

import pytest
from pytest_lazyfixture import lazy_fixture as lf
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
    news
):
    comment_list = Comment.objects.all()
    comment_list.delete()
    buff_comment_count = Comment.objects.count()
    author_client.post(url_detail, data=FORM_DATA)
    assert Comment.objects.count() == buff_comment_count + 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news


def test_user_cant_use_bad_words(author_client, url_detail):
    start_comments_count = Comment.objects.count()
    response = author_client.post(
        url_detail,
        data={'text': choice(BAD_WORDS)},
    )
    assert Comment.objects.count() == start_comments_count
    assertFormError(
        response,
        'form',
        'text',
        WARNING,
    )


@pytest.mark.parametrize(
    'test_client_instance, delta_count',
    (
        (lf('author_client'), 1),
        (lf('admin_client'), 0),
    )
)
def test_can_delete_comment(
    test_client_instance,
    delta_count,
    url_delete,
):
    start_comments_count = Comment.objects.count()
    test_client_instance.post(url_delete)
    end_comments_count = Comment.objects.count()
    assert start_comments_count == end_comments_count + delta_count


@pytest.mark.parametrize(
    'test_client_instance, can_edit_comment , expected_status',
    (
        (
            lf('admin_client'), False, HTTPStatus.NOT_FOUND,
        ),
        (
            lf('author_client'), True, HTTPStatus.FOUND,
        ),
    )
)
def test_edit_comment(
    test_client_instance,
    can_edit_comment,
    expected_status,
    comment,
    url_edit,
):
    original_value = Comment.objects.get(pk=comment.pk)
    response = test_client_instance.post(
        url_edit,
        data=FORM_DATA
    )
    target_value = Comment.objects.get(pk=comment.pk)
    assert response.status_code == expected_status
    if can_edit_comment:
        assert target_value.text == FORM_DATA['text']
    else:
        assert target_value.text == original_value.text
        assert target_value.author == original_value.author
