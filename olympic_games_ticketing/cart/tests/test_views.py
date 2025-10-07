from accounts.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from products.models import Offer

from cart.cart import Cart


class TestCartSummaryPageView(TestCase):
    """Tests for verifying the behavior of the cart summary page view."""

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


class TestAddOfferToCartView(TestCase):
    """Tests for verifying the behavior of the add offer to cart view."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user, offers and the cart add URL for reuse in tests."""
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )
        fake_image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        Offer.objects.create(
            name="Solo",
            slug="solo",
            thumbnail=fake_image,
            description="A single seat offer.",
            seats=1,
            price=25,
            is_active=True,
        )
        Offer.objects.create(
            name="Duo",
            slug="duo",
            thumbnail=fake_image,
            description="A double seat offer.",
            seats=2,
            price=40,
            is_active=True,
        )
        cls.cart_add_url = reverse("cart-add")

    def setUp(self):
        """
        Log in the test client before each test to simulate an authenticated session.
        """
        self.client.login(email="johndoe@gmail.com", password="paris2024")

    def test_add_offer_to_cart(self):
        """Test adding offers to an empty shopping cart."""
        response = self.client.post(
            self.cart_add_url, {"offer_id": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"quantity": 1})
        response = self.client.post(
            self.cart_add_url, {"offer_id": 2, "action": "post"}, xhr=True
        )
        self.assertEqual(response.json(), {"quantity": 2})


class TestRemoveOfferFromCartView(TestCase):
    """Tests for verifying the behavior of the remove offer from cart view."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user, an offer and the URLs for reuse in tests."""
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )
        fake_image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        Offer.objects.create(
            name="Solo",
            slug="solo",
            thumbnail=fake_image,
            description="A single seat offer.",
            seats=1,
            price=25,
            is_active=True,
        )
        cls.cart_add_url = reverse("cart-add")
        cls.cart_delete_url = reverse("cart-delete")

    def setUp(self):
        """
        Log in the test client before each test to simulate an authenticated session.
        """
        self.client.login(email="johndoe@gmail.com", password="paris2024")
        self.client.post(self.cart_add_url, {"offer_id": 1, "action": "post"}, xhr=True)

    def test_remove_offer_from_cart(self):
        """Test removing an offer from the shopping cart."""
        response = self.client.post(
            self.cart_delete_url, {"offer_id": 1, "action": "post"}, xhr=True
        )
        self.assertEqual(
            response.json(), {"Deleted": True, "quantity": 0, "total_price": 0}
        )
