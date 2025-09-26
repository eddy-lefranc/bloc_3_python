from django.test import SimpleTestCase
from django.urls import resolve

from products.views import offer_detail_page, offers_list_page


class TestProductsAppUrls(SimpleTestCase):
    """Test cases for verifying that products app URLs are configured correctly."""

    def setUp(self):
        """Resolve the URLs for tests."""
        self.match_offers = resolve("/products/offers/")
        self.match_offer = resolve("/products/offers/solo/")

    def test_offers_url_resolves_to_correct_view(self):
        """
        Ensure that '/products/offers/' URL resolves to the offers_list_page view.
        """
        self.assertEqual(self.match_offers.func, offers_list_page)

    def test_offers_url_resolves_to_correct_name(self):
        """Ensure that '/products/offers/' URL has the correct URL name 'offers'."""
        self.assertEqual(self.match_offers.url_name, "offers")

    def test_offer_url_resolves_to_correct_view(self):
        """
        Ensure that '/products/offers/solo/' URL resolves to the offer_detail_page view.
        """
        self.assertEqual(self.match_offer.func, offer_detail_page)

    def test_offer_url_resolves_to_correct_name(self):
        """
        Ensure that '/products/offers/solo/' URL has the correct URL name 'offer'.
        """
        self.assertEqual(self.match_offer.url_name, "offer")
