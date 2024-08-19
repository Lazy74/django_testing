from django.urls import reverse

from notes.forms import NoteForm
from notes.tests.base_test_case import BaseTestCase


class TestHomePage(BaseTestCase):

    def test_news_count(self):
        url = reverse('notes:list')
        response = self.two_author_client.get(url)
        object_list = response.context['object_list']
        self.assertIn(member=self.two_note, container=object_list)

    def test_user_notes_do_not_include_other_users_notes(self):
        url = reverse('notes:list')
        response = self.two_author_client.get(url)
        object_list = response.context['object_list']
        self.assertIn(member=self.two_note, container=object_list)
        self.assertNotIn(member=self.one_note, container=object_list)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.one_author)
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.one_note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
