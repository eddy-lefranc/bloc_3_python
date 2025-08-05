from django.test import TestCase

from accounts.forms import SignupForm


class SignupFormTestCase(TestCase):
    """Tests for verifying the behavior of the signup form."""

    def setUp(self):
        """Initialize an empty signup form and valid_data for reuse in tests."""
        self.form = SignupForm()
        self.valid_data = {
            "first_name": "Jean",
            "last_name": "Dupont",
            "email": "jean.dupont@exemple.com",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
        }

    def build_data(self, **overrides):
        """Return a copy of valid_data updated with any overrides."""
        data = self.valid_data.copy()
        data.update(overrides)
        return data

    def test_username_field_not_in_form(self):
        """Test that the 'username' field is not present in the form fields."""
        self.assertNotIn("username", self.form.fields)

    def test_email_field_in_form(self):
        """Test that the 'email' field is present in the form fields."""
        self.assertIn("email", self.form.fields)

    def test_first_name_field_in_form(self):
        """Test that the 'first_name' field is present in the form fields."""
        self.assertIn("first_name", self.form.fields)

    def test_last_name_field_in_form(self):
        """Test that the 'last_name' field is present in the form fields."""
        self.assertIn("last_name", self.form.fields)

    def test_password1_field_in_form(self):
        """Test that the 'password1' field is present in the form fields."""
        self.assertIn("password1", self.form.fields)

    def test_password2_field_in_form(self):
        """Test that the 'password2' field is present in the form fields."""
        self.assertIn("password2", self.form.fields)

    def test_form_valid_with_correct_data(self):
        """Test that the signup form is valid when provided with valid data."""
        form = SignupForm(data=self.build_data())
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_first_name(self):
        """Test that missing first_name triggers a form error."""
        form = SignupForm(data=self.build_data(first_name=""))
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_form_invalid_without_last_name(self):
        """Test that missing last_name triggers a form error."""
        form = SignupForm(data=self.build_data(last_name=""))
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_form_invalid_without_email(self):
        """Test that missing email triggers a form error."""
        form = SignupForm(data=self.build_data(email=""))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_invalid_without_password1(self):
        """Test that missing password1 triggers a form error."""
        form = SignupForm(data=self.build_data(password1=""))
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_form_invalid_without_password2(self):
        """Test that missing password2 triggers a form error."""
        form = SignupForm(data=self.build_data(password2=""))
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_with_bad_first_name(self):
        """Test that invalid first_name triggers a form error."""
        form = SignupForm(data=self.build_data(first_name="Jean728"))
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_form_invalid_with_bad_last_name(self):
        """Test that invalid last_name triggers a form error."""
        form = SignupForm(data=self.build_data(last_name="Dupont728"))
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_form_invalid_with_bad_email(self):
        """Test that invalid email triggers a form error."""
        form = SignupForm(data=self.build_data(email="not-an-email"))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_invalid_with_password_mismatch(self):
        """Test that mismatched passwords triggers a form error."""
        form = SignupForm(data=self.build_data(password2="DifferentPassword123!"))
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
