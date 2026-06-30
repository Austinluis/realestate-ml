from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User


class RegisterViewTest(TestCase):

    def test_register_valid(self):
        """Valid form data creates a user in the database."""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(User.objects.filter(email='test@example.com').count(), 1)
        self.assertRedirects(response, reverse('dashboard'))

    def test_register_duplicate_email(self):
        """Duplicate email address returns a form error."""
        User.objects.create_user(
            username='existing', email='dupe@example.com', password='pass'
        )
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'dupe@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'errors' or 'already', status_code=200)

    def test_register_page_loads(self):
        """Register page returns 200."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='TestPass123!'
        )

    def test_login_valid(self):
        """Correct credentials create a session and redirect to dashboard."""
        response = self.client.post(reverse('login'), {
            'email': 'login@example.com',
            'password': 'TestPass123!',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_invalid(self):
        """Wrong password returns 200 with error message."""
        response = self.client.post(reverse('login'), {
            'email': 'login@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid')

    def test_logout(self):
        """Logout redirects to login page."""
        self.client.login(username='login@example.com', password='TestPass123!')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))


class DashboardViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='dashuser', email='dash@example.com', password='TestPass123!'
        )

    def test_dashboard_requires_login(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_loads_for_authenticated_user(self):
        """Logged-in user sees the dashboard."""
        self.client.login(username='dash@example.com', password='TestPass123!')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
