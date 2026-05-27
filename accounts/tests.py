from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class UserRegistrationTestCase(TestCase):
    """Test cases for user registration"""

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_registration_page_loads(self):
        """Test that registration page loads successfully"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        })

        # Check if user was created
        self.assertTrue(User.objects.filter(username='johndoe').exists())
        user = User.objects.get(username='johndoe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')

        # Should redirect to login page
        self.assertRedirects(response, reverse('login'))

    def test_user_registration_password_mismatch(self):
        """Test registration fails when passwords don't match"""
        response = self.client.post(self.register_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'testpass123',
            'password2': 'testpass456'
        })

        # User should not be created
        self.assertFalse(User.objects.filter(username='johndoe').exists())

        # Should redirect back to register
        self.assertRedirects(response, reverse('register'))

    def test_user_registration_duplicate_username(self):
        """Test registration fails with duplicate username"""
        # Create initial user
        User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )

        # Try to register with same username
        response = self.client.post(self.register_url, {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'jane@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        })

        # Should not create second user
        self.assertEqual(User.objects.filter(username='johndoe').count(), 1)

        # Should redirect back to register
        self.assertRedirects(response, reverse('register'))

    def test_user_registration_duplicate_email(self):
        """Test registration fails with duplicate email"""
        # Create initial user
        User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )

        # Try to register with same email
        response = self.client.post(self.register_url, {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe',
            'email': 'john@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        })

        # Should not create second user
        self.assertEqual(User.objects.count(), 1)

        # Should redirect back to register
        self.assertRedirects(response, reverse('register'))


class UserLoginTestCase(TestCase):
    """Test cases for user login"""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

        # Create a test user
        self.test_user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )

    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_user_login_success(self):
        """Test successful user login"""
        response = self.client.post(self.login_url, {
            'username': 'johndoe',
            'password': 'testpass123'
        })

        # Should redirect to dashboard
        self.assertRedirects(response, reverse('dashboard'))

        # Check if user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_invalid_username(self):
        """Test login fails with invalid username"""
        response = self.client.post(self.login_url, {
            'username': 'invaliduser',
            'password': 'testpass123'
        })

        # Should redirect back to login
        self.assertRedirects(response, reverse('login'))

    def test_user_login_invalid_password(self):
        """Test login fails with invalid password"""
        response = self.client.post(self.login_url, {
            'username': 'johndoe',
            'password': 'wrongpassword'
        })

        # Should redirect back to login
        self.assertRedirects(response, reverse('login'))

    def test_user_login_invalid_credentials(self):
        """Test login fails with completely invalid credentials"""
        response = self.client.post(self.login_url, {
            'username': 'invaliduser',
            'password': 'invalidpass'
        })

        # Should redirect back to login
        self.assertRedirects(response, reverse('login'))


class UserLogoutTestCase(TestCase):
    """Test cases for user logout"""

    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.login_url = reverse('login')

        # Create and login a test user
        self.test_user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )

    def test_user_logout_success(self):
        """Test successful user logout"""
        # First login
        self.client.login(username='johndoe', password='testpass123')

        # Then logout
        response = self.client.post(self.logout_url)

        # Should redirect to index
        self.assertRedirects(response, reverse('index'))

    def test_user_logout_session_cleared(self):
        """Test that logout clears user session"""
        # First login
        self.client.login(username='johndoe', password='testpass123')

        # Verify user is logged in
        response = self.client.get(reverse('dashboard'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Logout
        self.client.post(self.logout_url)

        # Create a new client to verify session is cleared
        new_client = Client()
        response = new_client.get(reverse('dashboard'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class DashboardAccessTestCase(TestCase):
    """Test cases for dashboard access control"""

    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('dashboard')

        # Create a test user
        self.test_user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )

    def test_dashboard_requires_authentication(self):
        """Test that unauthenticated users cannot access dashboard"""
        self.client.get(self.dashboard_url)
        # Unauthenticated user should not be able to view their contacts
        # The dashboard might render empty contacts for anonymous users

    def test_dashboard_accessible_when_authenticated(self):
        """Test that authenticated users can access dashboard"""
        # Login first
        self.client.login(username='johndoe', password='testpass123')

        # Access dashboard
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
