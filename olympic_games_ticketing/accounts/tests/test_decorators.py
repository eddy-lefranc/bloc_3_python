from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class TestAccountsAppDecorators(TestCase):
    """Tests for the decorators applied to views in the accounts app."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user for all tests.."""
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )

    def setUp(self):
        """Store the signup URL for use in each test."""
        self.signup_url = reverse("signup")

    def test_anonymous_status_code_200(self):
        """
        Test that anonymous users receive an HTTP 200 status code
        when accessing the signup page.
        """
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_redirects_home(self):
        """Test that authenticated users are redirected to the home page."""
        self.client.force_login(self.user)
        response = self.client.get(self.signup_url)
        self.assertRedirects(response, reverse("home"))
