from accounts.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from products.models import Offer


class TestOrderCreateView(TestCase):
    """Tests for verifying the behavior of the order create view."""

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
        cls.order_create_url = reverse("orders:create")

    def setUp(self):
        """
        Log in the test client before each test to simulate an authenticated session.
        """
        self.client.login(email="johndoe@gmail.com", password="paris2024")

    def test_order_create_returns_http302_when_cart_is_empty(self):
        """
        Test that a POST request to the order create view returns HTTP 302 status code
        when cart is empty.
        """
        response = self.client.post(self.order_create_url)
        self.assertEqual(response.status_code, 302)

    def test_order_create_redirects_to_cart_url_when_cart_is_empty(self):
        """
        Test that a POST request to the order create view redirects to the cart url
        when cart is empty.
        """
        response = self.client.post(self.order_create_url)
        self.assertRedirects(response, reverse("cart"))

    def test_order_create_post_shows_message_when_cart_is_empty(self):
        """
        Test that a post request to the order create view adds an error message
        when cart is empty and displays it.
        """
        self.client.post(self.order_create_url)
        response = self.client.get(reverse("cart"))
        self.assertContains(
            response,
            "Votre panier est vide. Veuillez ajouter au moins une offre avant de commander.",
        )
