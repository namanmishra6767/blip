from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Posts


class AuthenticationAndPostTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='alice',
            email='alice@example.com',
            password='StrongPass123!',
        )
        self.other_user = get_user_model().objects.create_user(
            username='bob',
            email='bob@example.com',
            password='StrongPass123!',
        )

    def test_register_user_creates_account_and_logs_user_in(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'charlie',
                'email': 'charlie@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('post_list'))
        self.assertTrue(
            get_user_model().objects.filter(username='charlie', email='charlie@example.com').exists()
        )

    def test_register_rejects_duplicate_email_case_insensitive(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'dupe',
                'email': 'ALICE@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email already exists.')

    def test_post_create_requires_login(self):
        response = self.client.get(reverse('post_create'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/posts/login/?next=', response.url)

    def test_post_edit_is_restricted_to_owner(self):
        post = Posts.objects.create(user=self.user, text='Owned by Alice')
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('post_edit', args=[post.pk]))

        self.assertEqual(response.status_code, 404)
