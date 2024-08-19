from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestHomePage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.one_author = User.objects.create(username='OneAuthor')
        cls.one_note = Note.objects.create(
            title='Новая заметка',
            author=cls.one_author,
            text='Текст заметки',
            slug='slugone',
        )

        cls.two_author = User.objects.create(username='TwoAuthor')
        cls.two_note = Note.objects.create(
            title='Новая заметка',
            author=cls.two_author,
            text='Текст заметки',
            slug='slugtwo',
        )
        cls.three_note = Note.objects.create(
            title='Новая заметка',
            author=cls.two_author,
            text='Текст заметки',
            slug='slugthree',
        )

    def test_news_count(self):
        self.client.force_login(self.two_author)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        news_count = object_list.count()
        self.assertEqual(news_count, 2)

    def test_user_notes_do_not_include_other_users_notes(self):
        self.client.force_login(self.two_author)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        for note in object_list:
            self.assertEqual(note.author, self.two_author)

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
