from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.main_author = User.objects.create(username='main_author')
        cls.main_author_client = Client()
        cls.main_author_client.force_login(cls.main_author)
        cls.one_note = Note.objects.create(
            title='Новая заметка',
            author=cls.main_author,
            text='Текст заметки',
            slug='slugone',
        )
        cls.other_author = User.objects.create(username='other_author')
        cls.other_author_client = Client()
        cls.other_author_client.force_login(cls.other_author)
        cls.two_note = Note.objects.create(
            title='Новая заметка',
            author=cls.other_author,
            text='Текст заметки',
            slug='slugtwo',
        )
        cls.three_note = Note.objects.create(
            title='Новая заметка',
            author=cls.other_author,
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
        cls.url_login = reverse('users:login')
        cls.url_logout = reverse('users:logout')
        cls.url_signup = reverse('users:signup')
        cls.url_home = reverse('notes:home')
        cls.url_list = reverse('notes:list')
        cls.url_add = reverse('notes:add')
        cls.url_success = reverse('notes:success')
        cls.url_edit = reverse('notes:edit', args=(cls.one_note.slug,))
        cls.url_delete = reverse('notes:delete', args=(cls.one_note.slug,))
        cls.url_detail = reverse('notes:detail', args=(cls.one_note.slug,))
