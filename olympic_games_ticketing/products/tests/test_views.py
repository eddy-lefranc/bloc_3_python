from django.test import TestCase
from django.urls import reverse

from products.models import Offer


class TestOffersListPageView(TestCase):
    """Tests for verifying the behavior of the offers list page view."""

    @classmethod
    def setUpTestData(cls):
        """
        Create a sample offer and set up the offers list page url for reuse in tests.
        """
        cls.offer = Offer.objects.create(
            name="Solo",
            slug="solo",
            description="A single seat offer.",
            seats=1,
            price=25,
            is_active=True,
        )
        cls.url = reverse("offers")

    def test_offers_list_page_view_returns_status_200(self):
        """
        Test that GET request to offers list page view returns HTTP 200 status code.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_offers_list_page_view_uses_correct_template(self):
        """
        Test that the offers list page view renders the correct template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "products/offers-list.html")

    def test_offers_list_page_view_context_contains_offer(self):
        """
        Test that the offers list page view context includes the created offer.
        """
        response = self.client.get(self.url)
        self.assertIn(self.offer, response.context["offers"])


class TestOfferDetailPageView(TestCase):
    """Tests for verifying the behavior of the offer detail page view."""

    @classmethod
    def setUpTestData(cls):
        """
        Create a sample offer and set up the offer detail page url for reuse in tests.
        """
        cls.offer = Offer.objects.create(
            name="Solo",
            slug="solo",
            description="A single seat offer.",
            seats=1,
            price=25,
            is_active=True,
        )
        cls.url = reverse("offer", kwargs={"slug": cls.offer.slug})

    def test_offer_detail_page_view_returns_status_200(self):
        """
        Test that GET request to offer detail page view returns HTTP 200 status code.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_offer_detail_page_view_uses_correct_template(self):
        """
        Test that the offer detail page view renders the correct template.
        """
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "products/offer-detail.html")

    def test_offer_detail_page_view_context_contains_offer(self):
        """
        Test that the offer detail page view context includes the created offer.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.context["offer"], self.offer)
