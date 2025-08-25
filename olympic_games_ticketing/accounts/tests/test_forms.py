from django.forms import PasswordInput
from django.test import SimpleTestCase, TestCase

from accounts.forms import LoginForm, SignupForm


class TestSignupForm(TestCase):
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

    def test_signup_form_fields_order(self):
        """Test that the signup form fields appears in order."""
        fields_order = ["email", "first_name", "last_name", "password1", "password2"]
        self.assertEqual(list(self.form.fields), fields_order)

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


class TestLoginForm(SimpleTestCase):
    """Tests for verifying the behavior of the login form"""

    def setUp(self):
        """Initialize an empty login form and valid_data for reuse in tests."""
        self.form = LoginForm()
        self.valid_data = {
            "email": "jean.dupont@exemple.com",
            "password": "TestPassword123!",
        }

    def build_data(self, **overrides):
        """Return a copy of valid_data updated with any overrides."""
        data = self.valid_data.copy()
        data.update(overrides)
        return data

    def test_login_form_fields_order(self):
        """Test that the login form fields appears in order."""
        fields_order = ["email", "password"]
        self.assertEqual(list(self.form.fields), fields_order)

    def test_email_field_in_form(self):
        """Test that the 'email' field is present in the form fields."""
        self.assertIn("email", self.form.fields)

    def test_email_field_max_length(self):
        """Test that the max length for the email field is '254'."""
        self.assertEqual(self.form.fields["email"].max_length, 254)

    def test_email_field_label(self):
        """Test that the email field label is 'Adresse électronique'."""
        self.assertEqual(self.form.fields["email"].label, "Adresse électronique")

    def test_password_field_in_form(self):
        """Test that the 'password' field is present in the form fields."""
        self.assertIn("password", self.form.fields)

    def test_password_field_max_length(self):
        """Test that the max length for the password field is '128'."""
        self.assertEqual(self.form.fields["password"].max_length, 128)

    def test_password_field_widget(self):
        """Test that the password field uses a PasswordInput widget."""
        self.assertIsInstance(self.form.fields["password"].widget, PasswordInput)

    def test_password_field_label(self):
        """Test that the password field label is 'Mot de passe'."""
        self.assertEqual(self.form.fields["password"].label, "Mot de passe")

    def test_form_valid_with_correct_data(self):
        """Test that the login form is valid when provided with valid data."""
        form = LoginForm(data=self.build_data())
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_email(self):
        """Test that missing email triggers a form error."""
        form = LoginForm(data=self.build_data(email=""))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_invalid_without_password(self):
        """Test that missing password triggers a form error."""
        form = LoginForm(data=self.build_data(password=""))
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_form_invalid_with_bad_email(self):
        """Test that invalid email triggers a form error."""
        form = LoginForm(data=self.build_data(email="not-an-email"))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_invalid_with_bad_password(self):
        """Test that a password longer than defined max length triggers a form error."""
        form = LoginForm(data=self.build_data(password="A" * 130))
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)
