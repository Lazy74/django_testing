from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.tests.base_test_case import BaseTestCase


class TestNoteCreation(BaseTestCase):

    def test_anonymous_user_cant_create_note(self):
        initial_quantity = Note.objects.count()
        self.client.post(self.url_add, data=self.form_data)
        final_quantity = Note.objects.count()
        self.assertEqual(initial_quantity, final_quantity)

    def test_user_can_create_note(self):
        notes = Note.objects.all()
        notes.delete()
        initial_quantity = Note.objects.count()
        response = self.main_author_client.post(
            self.url_add, data=self.form_data
        )
        self.assertRedirects(response, self.url_success)
        final_quantity = Note.objects.count() - 1
        self.assertEqual(initial_quantity, final_quantity)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.main_author)
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cant_create_note_same_slug(self):
        initial_quantity = Note.objects.count()
        self.main_author_client.post(self.url_add, data=self.form_data)
        self.main_author_client.post(self.url_add, data=self.form_data_slug)
        final_quantity = Note.objects.count() - 1
        self.assertEqual(initial_quantity, final_quantity)

    def test_note_slug_is_generated_automatically_if_not_provided(self):
        notes = Note.objects.all()
        notes.delete()
        data = {
            'title': 'Новая заметка',
            'text': 'Текст заметки',
        }
        slug = slugify(data['title'])
        response = self.main_author_client.post(self.url_add, data=data)
        self.assertRedirects(response, self.url_success)
        note = Note.objects.get()
        self.assertEqual(note.slug, slug)


class TestEditDelete(BaseTestCase):

    def test_author_can_edit_note(self):
        response = self.main_author_client.post(
            self.url_edit, data=self.form_data
        )
        self.assertRedirects(response, self.url_success)
        self.one_note.refresh_from_db()
        self.assertEqual(self.one_note.text, self.form_data['text'])
        self.assertEqual(self.one_note.author, self.main_author)
        self.assertEqual(self.one_note.title, self.form_data['title'])
        self.assertEqual(self.one_note.slug, self.form_data['slug'])

    def test_author_can_delete_note(self):
        start_count = Note.objects.count()
        response = self.main_author_client.delete(self.url_delete)
        self.assertRedirects(response, self.url_success)
        self.assertEqual(Note.objects.count(), start_count - 1)

    def test_guest_cant_edit_others_note(self):
        response = self.other_author_client.post(
            self.url_edit, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(pk=self.one_note.pk)
        self.assertEqual(self.one_note.pk, note.pk)
        self.assertEqual(self.one_note.title, note.title)
        self.assertEqual(self.one_note.text, note.text)
        self.assertEqual(self.one_note.author, note.author)
        self.assertEqual(self.one_note.slug, note.slug)

    def test_guest_cant_delete_others_note(self):
        start_count = Note.objects.count()
        response = self.other_author_client.delete(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, start_count)
