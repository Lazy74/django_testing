from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import COMMENT_TEXTS, FORM_DATA


@pytest.mark.parametrize(
    'user',
    (
        pytest.lazy_fixture('client'),
    )
)
@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    user,
    news,
):
    user.post(reverse('news:detail', args=(news.pk,)), data=FORM_DATA)
    assert Comment.objects.count() == Comment.objects.count()


@pytest.mark.parametrize(
    'user_auth',
    (
        pytest.lazy_fixture('author_client'),
    )
)
@pytest.mark.django_db
def test_auth_user_can_create_comment(
    user_auth,
    news,
):
    buff_comment_count = Comment.objects.count()
    user_auth.post(reverse('news:detail', args=(news.pk,)), data=FORM_DATA)
    assert Comment.objects.count() == buff_comment_count + 1


def test_user_cant_use_bad_words(author_client, news):
    response = author_client.post(
        reverse('news:detail', args=(news.pk,)),
        data={'text': BAD_WORDS[0]},
    )
    assertFormError(
        response,
        'form',
        'text',
        WARNING,
    )
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'user, expected_count',
    (
        (pytest.lazy_fixture('author_client'), 0),
        (pytest.lazy_fixture('admin_client'), 1),
    )
)
def test_can_delete_comment(
    user,
    expected_count,
    comment,
):
    user.post(reverse('news:delete', args=(comment.pk,)))
    comments_count = Comment.objects.count()
    assert comments_count == expected_count


@pytest.mark.parametrize(
    'user, expected_text, expected_status',
    (
        (
            pytest.lazy_fixture('admin_client'), 0, HTTPStatus.NOT_FOUND,
        ),
        (
            pytest.lazy_fixture('author_client'), 1, HTTPStatus.FOUND,
        ),
    )
)
def test_edit_comment(
    user,
    expected_text,
    expected_status,
    comment,
):
    response = user.post(
        reverse('news:edit', args=(comment.pk,)),
        data=FORM_DATA
    )
    assert response.status_code == expected_status
    edited_comment = Comment.objects.get()
    assert edited_comment.text == COMMENT_TEXTS[expected_text]
