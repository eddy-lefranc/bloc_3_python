from django.test import SimpleTestCase
from django.urls import resolve

from olympic_games_ticketing.views import home_page


class TestBaseProjectUrls(SimpleTestCase):
    """Test cases for verifying that the base project URLs are configured correctly."""

    def setUp(self):
        """Resolve the '/' URL for tests."""
        self.match = resolve("/")

    def test_base_url_resolves_to_correct_view(self):
        """Ensure that '/' URL resolves to the home_page view."""
        self.assertEqual(self.match.func, home_page)

    def test_base_url_resolves_to_correct_name(self):
        """Ensure that '/' URL has the correct URL name 'home'."""
        self.assertEqual(self.match.url_name, "home")
