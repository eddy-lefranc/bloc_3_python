from accounts.models import User
from django.test import TestCase
from django.urls import reverse

from cart.cart import Cart


class TestCartSummaryView(TestCase):
    """Tests for verifying the behavior of the cart summary view."""

    @classmethod
    def setUpTestData(cls):
        """
        Set up a test user and the cart summary page url for reuse in tests.
        """
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )
        cls.cart_summary_url = reverse("cart")

    def setUp(self):
        """
        Log in the test client before each test to simulate an authenticated session.
        """
        self.client.login(email="johndoe@gmail.com", password="paris2024")

    def test_cart_summary_requires_login(self):
        """
        Verify that an unauthenticated user is redirected (302) when accessing
        the cart summary page.
        """
        self.client.logout()
        response = self.client.get(self.cart_summary_url)
        self.assertEqual(response.status_code, 302)

    def test_cart_summary_when_logged_in_returns_200(self):
        """
        Verify that an authenticated user can access the cart summary page
        with a 200 response.
        """
        response = self.client.get(self.cart_summary_url)
        self.assertEqual(response.status_code, 200)

    def test_cart_summary_get_uses_correct_template(self):
        """
        Test that the cart summary view renders the correct template.
        """
        response = self.client.get(self.cart_summary_url)
        self.assertTemplateUsed(response, "cart/cart-summary.html")

    def test_cart_summary_get_contains_heading(self):
        """
        Test that the cart summary page contains the heading 'Votre panier'.
        """
        response = self.client.get(self.cart_summary_url)
        self.assertContains(response, "Votre panier")

    def test_cart_summary_page_view_context_contains_cart(self):
        """
        Verify that the cart summary view context includes a Cart instance.
        """
        response = self.client.get(self.cart_summary_url)
        self.assertIsInstance(response.context["cart"], Cart)
