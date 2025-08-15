from django.test import SimpleTestCase
from django.urls import resolve

from accounts.views import signup_confirmation_page, signup_page


class TestAccountsAppUrls(SimpleTestCase):
    """Test cases for verifying that accounts app URLs are configured correctly."""

    def setUp(self):
        """Resolve the '/accounts/signup/' URL for tests."""
        self.match_signup = resolve("/accounts/signup/")
        self.match_signup_confirmation = resolve("/accounts/signup/confirmation/")

    def test_signup_url_resolves_to_correct_view(self):
        """Ensure that '/accounts/signup/' URL resolves to the signup_page view."""
        self.assertEqual(self.match_signup.func, signup_page)

    def test_signup_url_resolves_to_correct_name(self):
        """Ensure that '/accounts/signup/' URL has the correct URL name 'signup'."""
        self.assertEqual(self.match_signup.url_name, "signup")

    def test_signup_confirmation_url_resolves_to_correct_view(self):
        """Ensure that '/accounts/signup/confirmation/' URL resolves to the signup_page view."""
        self.assertEqual(self.match_signup_confirmation.func, signup_confirmation_page)

    def test_signup_confirmation_url_resolves_to_correct_name(self):
        """Ensure that '/accounts/signup/confirmation/' URL has the correct URL name 'signup-confirmation'."""
        self.assertEqual(self.match_signup_confirmation.url_name, "signup-confirmation")
