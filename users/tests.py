from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from films.models import Favorite

class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_register_view(self):
        """Test user registration view"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_profile_view(self):
        """Test profile page loads successfully"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_edit_profile_view(self):
        """Test editing user profile"""
        response = self.client.post(reverse('edit_profile'), {
            'username': 'updateduser',
            'email': 'test@example.com'
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Should redirect to profile
        self.assertEqual(self.user.username, 'updateduser')

    def test_favorites_view(self):
        """Test user favorites page"""
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/favorites.html')
