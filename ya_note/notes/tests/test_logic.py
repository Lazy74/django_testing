from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from pytils.translit import slugify

from notes.models import Note


User = get_user_model()


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='testAuthor')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
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

    def test_anonymous_user_cant_create_note(self):
        initialQuantity = Note.objects.count()
        url = reverse("notes:add", args=None)
        self.client.post(url, data=self.form_data)
        finalQuantity = Note.objects.count()
        self.assertEqual(initialQuantity, finalQuantity)

    def test_user_can_create_note(self):
        notes = Note.objects.all()
        notes.delete()
        initialQuantity = Note.objects.count()
        url = reverse("notes:add", args=None)
        response = self.auth_client.post(url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        finalQuantity = Note.objects.count() - 1
        self.assertEqual(initialQuantity, finalQuantity)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cant_create_note_same_slug(self):
        initialQuantity = Note.objects.count()
        url = reverse("notes:add", args=None)
        self.auth_client.post(url, data=self.form_data)
        self.auth_client.post(url, data=self.form_data_slug)
        finalQuantity = Note.objects.count() - 1
        self.assertEqual(initialQuantity, finalQuantity)

    def test_note_slug_is_generated_automatically_if_not_provided(self):
        notes = Note.objects.all()
        notes.delete()
        data = {
            'title': 'Новая заметка',
            'text': 'Текст заметки',
        }
        slug = slugify(data['title'])
        url = reverse("notes:add", args=None)
        response = self.auth_client.post(url, data=data)
        self.assertRedirects(response, reverse('notes:success'))
        note = Note.objects.get()
        self.assertEqual(note.slug, slug)


class TestEditDelete(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='testAuthor')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.note = Note.objects.create(
            title='Новая заметка',
            text='Текст заметки',
            author=cls.author,
            slug='slug',
        )
        cls.form_data = {
            'title': 'Еще новая заметка',
            'text': 'Еще текст заметки',
            'slug': 'newslug',
        }

        cls.user = User.objects.create(username='testUser')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)

    def test_author_can_edit_note(self):
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.author_client.post(url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.form_data['text'])

    def test_author_can_delete_note(self):
        start_count = Note.objects.count()
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.author_client.delete(url)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), start_count - 1)

    def test_guest_cant_edit_others_note(self):
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.user_client.post(url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.note.text)

    def test_guest_cant_delete_others_note(self):
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
