from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.one_author = User.objects.create(username='OneAuthor')
        cls.one_author_client = Client()
        cls.one_author_client.force_login(cls.one_author)
        cls.one_note = Note.objects.create(
            title='Новая заметка',
            author=cls.one_author,
            text='Текст заметки',
            slug='slugone',
        )
        cls.two_author = User.objects.create(username='TwoAuthor')
        cls.two_author_client = Client()
        cls.two_author_client.force_login(cls.two_author)
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
        cls.form_data = {
            'title': 'Новая заметка',
            'text': 'Текст заметки',
            'slug': 'slug',
        }
        cls.form_data_slug = {
            'title': 'Еще новая заметка',
            'text': 'Еще текст заметки',
            'slug': 'slug',
        }
