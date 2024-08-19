from notes.forms import NoteForm
from notes.tests.base_test_case import BaseTestCase


class TestHomePage(BaseTestCase):

    def test_news_count(self):
        response = self.two_author_client.get(self.url_list)
        object_list = response.context['object_list']
        self.assertIn(member=self.two_note, container=object_list)

    def test_user_notes_do_not_include_other_users_notes(self):
        response = self.two_author_client.get(self.url_list)
        object_list = response.context['object_list']
        self.assertIn(member=self.two_note, container=object_list)
        self.assertNotIn(member=self.one_note, container=object_list)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.one_author)
        urls = (
            self.url_add,
            self.url_edit,
        )
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
