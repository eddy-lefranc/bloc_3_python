from django.test import SimpleTestCase
from django.urls import resolve

from accounts.views import signup_page


class TestAccountsAppUrls(SimpleTestCase):
    """Test cases for verifying that accounts app URLs are configured correctly."""

    def setUp(self):
        """Resolve the '/accounts/signup/' URL for tests."""
        self.match = resolve("/accounts/signup/")

    def test_signup_url_resolves_to_correct_view(self):
        """Ensure that '/accounts/signup/' URL resolves to the signup_page view."""
        self.assertEqual(self.match.func, signup_page)

    def test_signup_url_resolves_to_correct_name(self):
        """Ensure that '/accounts/signup/' URL has the correct URL name 'signup'."""
        self.assertEqual(self.match.url_name, "signup")
