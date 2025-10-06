from django.test import SimpleTestCase
from django.urls import resolve

from cart.views import add_offer_to_cart, cart_summary_page, remove_offer_from_cart


class TestCartAppUrls(SimpleTestCase):
    """Test cases for verifying that cart app URLs are configured correctly."""

    def setUp(self):
        """Resolve the URLs for tests."""
        self.match_cart_summary = resolve("/cart/summary/")
        self.match_cart_add = resolve("/cart/add/")
        self.match_cart_delete = resolve("/cart/delete/")

    def test_cart_url_resolves_to_correct_view(self):
        """
        Ensure that '/cart/summary/' URL resolves to the cart_summary_page view.
        """
        self.assertEqual(self.match_cart_summary.func, cart_summary_page)

    def test_cart_url_resolves_to_correct_name(self):
        """Ensure that '/cart/summary/' URL has the correct URL name 'cart'."""
        self.assertEqual(self.match_cart_summary.url_name, "cart")

    def test_cart_add_url_resolves_to_correct_view(self):
        """
        Ensure that '/cart/add/' URL resolves to the add_offer_to_cart view.
        """
        self.assertEqual(self.match_cart_add.func, add_offer_to_cart)

    def test_cart_add_url_resolves_to_correct_name(self):
        """Ensure that '/cart/add/' URL has the correct URL name 'cart-add'."""
        self.assertEqual(self.match_cart_add.url_name, "cart-add")

    def test_cart_delete_url_resolves_to_correct_view(self):
        """
        Ensure that '/cart/delete/' URL resolves to the remove_offer_from_cart view.
        """
        self.assertEqual(self.match_cart_delete.func, remove_offer_from_cart)

    def test_cart_delete_url_resolves_to_correct_name(self):
        """Ensure that '/cart/delete/' URL has the correct URL name 'cart-delete'."""
        self.assertEqual(self.match_cart_delete.url_name, "cart-delete")
