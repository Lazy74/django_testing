from http import HTTPStatus
from random import choice

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import FORM_DATA

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
    client,
    news,
):
    comment_count = Comment.objects.count()
    client.post(reverse('news:detail', args=(news.pk,)), data=FORM_DATA)
    assert comment_count == Comment.objects.count()


def test_auth_user_can_create_comment(
    author_client,
    news,
):
    buff_comment_count = Comment.objects.count()
    author_client.post(reverse('news:detail', args=(news.pk,)), data=FORM_DATA)
    assert Comment.objects.count() == buff_comment_count + 1
    assert Comment.objects.get().text == FORM_DATA['text']


def test_user_cant_use_bad_words(author_client, news):
    response = author_client.post(
        reverse('news:detail', args=(news.pk,)),
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
    comment,
):
    start_comments_count = Comment.objects.count()
    user.post(reverse('news:delete', args=(comment.pk,)))
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
):
    originalValue = Comment.objects.get(pk=comment.pk)
    response = user.post(
        reverse('news:edit', args=(comment.pk,)),
        data=FORM_DATA
    )
    targetValue = Comment.objects.get(pk=comment.pk)
    assert response.status_code == expected_status
    if can_edit_comment:
        assert targetValue.text == FORM_DATA['text']
    else:
        assert targetValue.text == originalValue.text
