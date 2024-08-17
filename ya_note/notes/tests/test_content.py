from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestHomePage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.OneAuthor = User.objects.create(username='OneAuthor')
        cls.OneNote = Note.objects.create(
            title='Новая заметка',
            author=cls.OneAuthor,
            text='Текст заметки',
            slug='slugone',
        )

        cls.TwoAuthor = User.objects.create(username='TwoAuthor')
        cls.TwoNote = Note.objects.create(
            title='Новая заметка',
            author=cls.TwoAuthor,
            text='Текст заметки',
            slug='slugtwo',
        )
        cls.ThreeNote = Note.objects.create(
            title='Новая заметка',
            author=cls.TwoAuthor,
            text='Текст заметки',
            slug='slugthree',
        )

    def test_news_count(self):
        self.client.force_login(self.TwoAuthor)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        news_count = object_list.count()
        self.assertEqual(news_count, 2)

    def test_user_notes_do_not_include_other_users_notes(self):
        self.client.force_login(self.TwoAuthor)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        for note in object_list:
            self.assertEqual(note.author, self.TwoAuthor)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.OneAuthor)
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.OneNote.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
