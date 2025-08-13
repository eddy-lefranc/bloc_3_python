import uuid

from django.db import IntegrityError
from django.test import TestCase

from accounts.models import User


class CustomUserModelTestCase(TestCase):
    """Tests for verifying the behavior of the custom user model."""

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

    def test_email_field_value(self):
        """Test that the email field stores the expected value."""
        self.assertEqual(self.user.email, "johndoe@gmail.com")

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

    def test_first_name_field_is_in_required_fields_constant(self):
        """Test that 'first_name' is included in the REQUIRED_FIELDS constant."""
        self.assertIn("first_name", self.user.REQUIRED_FIELDS)

    def test_first_name_field_max_length(self):
        """Test that the max length for the first name field is 150."""
        first_name_field_max_length = self.user._meta.get_field("first_name").max_length
        self.assertEqual(first_name_field_max_length, 150)

    def test_first_name_field_verbose_name(self):
        """Test that the first name field verbose name is 'Prénom'."""
        first_name_field_verbose_name = self.user._meta.get_field(
            "first_name"
        ).verbose_name
        self.assertEqual(first_name_field_verbose_name, "Prénom")

    def test_first_name_field_value(self):
        """Test that the first name field stores the expected value."""
        self.assertEqual(self.user.first_name, "John")

    def test_last_name_field_is_in_required_fields_constant(self):
        """Test that 'last_name' is included in the REQUIRED_FIELDS constant."""
        self.assertIn("last_name", self.user.REQUIRED_FIELDS)

    def test_last_name_field_max_length(self):
        """Test that the max length for the last name field is 150."""
        last_name_field_max_length = self.user._meta.get_field("last_name").max_length
        self.assertEqual(last_name_field_max_length, 150)

    def test_last_name_field_verbose_name(self):
        """Test that the last name field verbose name is 'Nom'."""
        last_name_field_verbose_name = self.user._meta.get_field(
            "last_name"
        ).verbose_name
        self.assertEqual(last_name_field_verbose_name, "Nom")

    def test_last_name_field_value(self):
        """Test that the last name field stores the expected value."""
        self.assertEqual(self.user.last_name, "Doe")

    def test_password_field_value(self):
        """Test that the password field stores the expected value."""
        self.assertTrue(self.user.check_password("paris2024"))

    def test_registration_key_field_is_generated(self):
        """Test that a registration key is generated for the user."""
        self.assertIsNotNone(self.user.registration_key)

    def test_registration_key_field_default_attribute_is_uuid4(self):
        """Test that registration key default attribute is 'uuid.uuid4'."""
        registration_key_field = self.user._meta.get_field("registration_key")
        self.assertIs(registration_key_field.default, uuid.uuid4)

    def test_registration_key_field_editable_attribute_is_false(self):
        """Test that registration key is not editable."""
        registration_key_field = self.user._meta.get_field("registration_key")
        self.assertFalse(registration_key_field.editable)

    def test_str_method_returns_full_name(self):
        """Test that the __str__ method returns the full name of the user."""
        self.assertEqual(str(self.user), "John Doe")
