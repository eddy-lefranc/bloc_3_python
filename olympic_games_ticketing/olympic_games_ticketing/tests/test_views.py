from django.test import SimpleTestCase
from django.urls import reverse


class HomePageViewTests(SimpleTestCase):
    """Tests for verifying the behavior of the home page view."""

    def setUp(self):
        """Set up the home page URL for reuse in tests."""
        self.url = reverse("home")

    def test_home_page_returns_status_200(self):
        """Test that GET request to home page view returns HTTP 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_uses_correct_template(self):
        """Test that the home page view renders the 'home.html' template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "home.html")
