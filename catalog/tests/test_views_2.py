from django.test import TestCase
from django.urls import reverse

import datetime
from django.utils import timezone
from django.contrib.auth.models import User # Required to assign User as a borrower

from catalog.models import Author, BookInstance, Book, Genre, Language

import uuid
from django.contrib.auth.models import Permission # Required to grant the permission needed to set a book as returned.



class AuthorCreateViewTest(TestCase):
    """Test case for the AuthorCreate view (Created as Challenge)."""

    def setUp(self):
        # Create a user
        test_userA = User.objects.create_user(username='testuserA', password='1X<ISRUkw+tuK')
        test_userB = User.objects.create_user(username='testuserB', password='2HJ1vRV0Z&3iD')

        test_userA.save()
        test_userB.save()

        permission = Permission.objects.get(name='Set book as returned')
        test_userB.user_permissions.add(permission)
        test_userB.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-create'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/author/create/')

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuserA', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission(self):
        login = self.client.login(username='testuserB', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuserB', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')

    def test_form_date_of_death_initially_set_to_expected_date(self):
        login = self.client.login(username='testuserB', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

        expected_initial_date = datetime.date(2050, 12, 31)
        response_date = response.context['form'].initial['date_of_death']
        response_date = datetime.datetime.strptime(response_date, "%d/%m/%Y").date()
        self.assertEqual(response_date, expected_initial_date)

    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(username='testuserB', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('author-create'),
                                    {'first_name': 'Christian Name', 'last_name': 'Surname'})
        # Manually check redirect because we don't know what author was created
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/author/'))
