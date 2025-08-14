from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class TestSignupView(TestCase):
    """Tests for verifying the behavior of the signup view."""

    def setUp(self):
        """Set up the signup URL and valid registration data for reuse in tests."""
        self.signup_url = reverse("signup")
        self.signup_confirmation_url = reverse("signup-confirmation")
        self.valid_data = {
            "first_name": "Jean",
            "last_name": "Dupont",
            "email": "jean.dupont@example.com",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
        }

    def build_data(self, **overrides):
        """Return a copy of valid_data updated with any overrides."""
        data = self.valid_data.copy()
        data.update(overrides)
        return data

    def test_signup_get_returns_http200(self):
        """Test that a GET request to the signup view returns HTTP 200 status code."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_get_uses_correct_template(self):
        """Test that the signup view renders the 'accounts/signup.html' template."""
        response = self.client.get(self.signup_url)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_signup_get_contains_heading(self):
        """Test that the signup page contains the heading 'Formulaire d'inscription'."""
        response = self.client.get(self.signup_url)
        self.assertContains(response, "Formulaire d'inscription")

    def test_signup_post_with_valid_data_redirects_to_confirmation(self):
        """Test that a valid signup redirects to the signup confirmation page."""
        response = self.client.post(self.signup_url, data=self.build_data())
        self.assertRedirects(response, reverse("signup-confirmation"))

    def test_signup_post_with_valid_data_creates_user(self):
        """Test that submitting valid signup data creates a new user."""
        self.client.post(self.signup_url, data=self.build_data())
        self.assertTrue(User.objects.filter(email="jean.dupont@example.com").exists())

    def test_signup_post_with_invalid_first_name_shows_custom_error_message(self):
        """Test that an invalid first_name triggers the custom regex error message."""
        response = self.client.post(
            self.signup_url, data=self.build_data(first_name="@!#")
        )
        self.assertContains(
            response,
            "Veuillez entrer un nom valide. Seules les lettres, espaces, tirets et apostrophes sont autorisés.",
        )

    def test_signup_post_with_invalid_last_name_shows_custom_error_message(self):
        """Test that an invalid last_name triggers the custom regex error message."""
        response = self.client.post(
            self.signup_url, data=self.build_data(last_name="1234")
        )
        self.assertContains(
            response,
            "Veuillez entrer un nom valide. Seules les lettres, espaces, tirets et apostrophes sont autorisés.",
        )

    def test_signup_confirmation_get_uses_correct_template(self):
        """Test that the signup confirmation view renders the 'accounts/signup/confirmation.html' template."""
        response = self.client.get(self.signup_confirmation_url)
        self.assertTemplateUsed(response, "accounts/signup-confirmation.html")

    def test_signup_confirmation_get_contains_heading(self):
        """Test that the signup confirmation page contains the correct heading."""
        response = self.client.get(self.signup_confirmation_url)
        self.assertContains(
            response,
            "Inscription réussie ! Connectez-vous dès maintenant pour accéder à votre compte.",
        )
