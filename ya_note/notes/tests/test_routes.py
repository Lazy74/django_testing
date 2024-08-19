from http import HTTPStatus

from notes.tests.base_test_case import BaseTestCase


class TestRoutes(BaseTestCase):

    def test_home_page(self):
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_auth_user_get_page(self):
        urls = (
            self.url_list,
            self.url_success,
            self.url_add,
            self.url_login,
            self.url_logout,
            self.url_signup,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.one_author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_access_to_edit_and_delete_note(self):
        users_statuses = (
            (self.one_author_client, HTTPStatus.OK),
            (self.two_author_client, HTTPStatus.NOT_FOUND),
        )
        for client, status in users_statuses:
            for url in (
                self.url_edit, self.url_detail, self.url_delete,
            ):
                with self.subTest(status=status, url=url):
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            self.url_list,
            self.url_success,
            self.url_add,
            self.url_edit,
            self.url_detail,
            self.url_delete,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.url_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
