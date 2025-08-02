from django.db import IntegrityError
from django.test import TestCase

from accounts.models import User


class UserModelTest(TestCase):
    """Test cases for verifying the behavior of the accounts models."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user for all tests."""
        User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )

    def setUp(self):
        """Retrieve the test user for each test case."""
        self.user = User.objects.get(id=1)

    def test_username_field_is_removed(self):
        """Test that the username field is removed from the user model."""
        self.assertIsNone(self.user.username)

    def test_email_field_is_username_field_constant(self):
        """Test that the USERNAME_FIELD constant is set to 'email'."""
        self.assertEqual(self.user.USERNAME_FIELD, "email")

    def test_email_field_max_length(self):
        """Test that the max length for the email field is 254."""
        email_field_max_length = self.user._meta.get_field("email").max_length
        self.assertEqual(email_field_max_length, 254)

    def test_email_field_is_unique(self):
        """Test that the email field has unique=True in the model."""
        email_field = self.user._meta.get_field("email")
        self.assertTrue(email_field.unique)

    def test_duplicate_email_raises_IntegrityError(self):
        """Test that the database rejects duplicate email addresses."""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=self.user.email,
                first_name="Jane",
                last_name="Doe",
                password="paris2024",
            )

    def test_email_field_verbose_name(self):
        """Test that the email field verbose name is 'Adresse électronique'."""
        email_field_verbose_name = self.user._meta.get_field("email").verbose_name
        self.assertEqual(email_field_verbose_name, "Adresse électronique")
