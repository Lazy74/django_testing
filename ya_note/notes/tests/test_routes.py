from http import HTTPStatus

from django.urls import reverse

from notes.tests.base_test_case import BaseTestCase


class TestRoutes(BaseTestCase):

    def test_home_page(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_auth_user_get_page(self):
        urls = (
            ('notes:list'),
            ('notes:success'),
            ('notes:add'),
            ('users:login'),
            ('users:logout'),
            ('users:signup'),
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name, args=None)
                response = self.one_author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_access_to_edit_and_delete_note(self):
        users_statuses = (
            (self.one_author_client, HTTPStatus.OK),
            (self.two_author_client, HTTPStatus.NOT_FOUND),
        )
        for client, status in users_statuses:
            for name in ('notes:edit', 'notes:detail', 'notes:delete'):
                with self.subTest(status=status, name=name):
                    url = reverse(name, args=(self.one_note.slug,))
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:edit', (self.one_note.slug,)),
            ('notes:detail', (self.one_note.slug,)),
            ('notes:delete', (self.one_note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
