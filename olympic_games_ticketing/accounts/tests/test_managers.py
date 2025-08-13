from django.test import TestCase

from accounts.models import User


class CreateUserTestCase(TestCase):
    """Tests for the create_user method of the custom user manager."""

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

    def test_create_user_sets_email_correctly(self):
        """Test that create_user sets the email correctly."""
        self.assertEqual(self.user.email, "johndoe@gmail.com")

    def test_create_user_sets_first_name_correctly(self):
        """Test that create_user sets the first name correctly."""
        self.assertEqual(self.user.first_name, "John")

    def test_create_user_sets_last_name_correctly(self):
        """Test that create_user sets the last name correctly."""
        self.assertEqual(self.user.last_name, "Doe")

    def test_create_user_does_not_store_plaintext_password(self):
        """Test that create_user does not store the password in plaintext."""
        self.assertNotEqual(self.user.password, "paris2024")
        self.assertTrue(self.user.password.startswith("pbkdf2_"))

    def test_create_user_password_is_set_correctly(self):
        """Test that the user's password can be verified with check_password()."""
        self.assertTrue(self.user.check_password("paris2024"))

    def test_create_user_is_active_by_default(self):
        """Test that a user is active by default after creation."""
        self.assertTrue(self.user.is_active)

    def test_create_user_is_not_staff_by_default(self):
        """Test that a user is not staff by default after creation."""
        self.assertFalse(self.user.is_staff)

    def test_create_user_is_not_superuser_by_default(self):
        """Test that a user is not a superuser by default after creation."""
        self.assertFalse(self.user.is_superuser)

    def test_create_user_without_email_raises_value_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                first_name="John",
                last_name="Doe",
                password="paris2024",
            )

    def test_create_user_without_first_name_raises_value_error(self):
        """Test that creating a user without a first name raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="johndoe@gmail.com",
                first_name="",
                last_name="Doe",
                password="paris2024",
            )

    def test_create_user_without_last_name_raises_value_error(self):
        """Test that creating a user without a last name raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="johndoe@gmail.com",
                first_name="John",
                last_name="",
                password="paris2024",
            )

    def test_create_user_without_password_raises_value_error(self):
        """Test that creating a user without a password raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="johndoe@gmail.com",
                first_name="John",
                last_name="Doe",
                password="",
            )


class CreateSuperuserTestCase(TestCase):
    """Tests for the create_superuser method of the custom user manager."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test superuser for all tests."""
        User.objects.create_superuser(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )

    def setUp(self):
        """Retrieve the test superuser for each test case."""
        self.user = User.objects.get(id=1)

    def test_create_superuser_sets_email_correctly(self):
        """Test that create_superuser sets the email correctly."""
        self.assertEqual(self.user.email, "johndoe@gmail.com")

    def test_create_superuser_sets_first_name_correctly(self):
        """Test that create_superuser sets the first name correctly."""
        self.assertEqual(self.user.first_name, "John")

    def test_create_superuser_sets_last_name_correctly(self):
        """Test that create_superuser sets the last name correctly."""
        self.assertEqual(self.user.last_name, "Doe")

    def test_create_superuser_does_not_store_plaintext_password(self):
        """Test that create_superuser does not store the password in plaintext."""
        self.assertNotEqual(self.user.password, "paris2024")
        self.assertTrue(self.user.password.startswith("pbkdf2_"))

    def test_create_superuser_password_is_set_correctly(self):
        """Test that the superuser's password can be verified with check_password()."""
        self.assertTrue(self.user.check_password("paris2024"))

    def test_create_superuser_is_active_by_default(self):
        """Test that a superuser is active by default after creation."""
        self.assertTrue(self.user.is_active)

    def test_create_superuser_is_staff_by_default(self):
        """Test that a superuser is staff by default after creation."""
        self.assertTrue(self.user.is_staff)

    def test_create_superuser_is_superuser_by_default(self):
        """Test that a superuser is superuser by default after creation."""
        self.assertTrue(self.user.is_superuser)

    def test_create_superuser_with_is_staff_false_raises_value_error(self):
        """Test that creating a superuser with is_staff=False raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="johndoe@gmail.com",
                first_name="John",
                last_name="Doe",
                password="paris2024",
                is_staff=False,
            )

    def test_create_superuser_with_is_superuser_false_raises_value_error(self):
        """Test that creating a superuser with is_superuser=False raises a ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="johndoe@gmail.com",
                first_name="John",
                last_name="Doe",
                password="paris2024",
                is_superuser=False,
            )
