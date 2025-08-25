from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class TestSignupView(TestCase):
    """Tests for verifying the behavior of the signup view."""

    def setUp(self):
        """Set up the signup URLs and valid registration data for reuse in tests."""
        self.signup_url = reverse("signup")
        self.signup_confirmation_url = reverse("signup-confirmation")
        self.valid_data = {
            "first_name": "Jean",
            "last_name": "Dupont",
            "email": "jean.dupont@example.com",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
        }

    def build_data(self, **overrides):
        """Return a copy of valid_data updated with any overrides."""
        data = self.valid_data.copy()
        data.update(overrides)
        return data

    def test_signup_get_returns_http200(self):
        """Test that a GET request to the signup view returns HTTP 200 status code."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

    def test_signup_get_uses_correct_template(self):
        """Test that the signup view renders the 'accounts/signup.html' template."""
        response = self.client.get(self.signup_url)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_signup_get_contains_heading(self):
        """Test that the signup page contains the heading 'Formulaire d'inscription'."""
        response = self.client.get(self.signup_url)
        self.assertContains(response, "Formulaire d'inscription")

    def test_signup_post_with_valid_data_redirects_to_confirmation(self):
        """Test that a valid signup redirects to the signup confirmation page."""
        response = self.client.post(self.signup_url, data=self.build_data())
        self.assertRedirects(response, reverse("signup-confirmation"))

    def test_signup_post_with_valid_data_creates_user(self):
        """Test that submitting valid signup data creates a new user."""
        self.client.post(self.signup_url, data=self.build_data())
        self.assertTrue(User.objects.filter(email="jean.dupont@example.com").exists())

    def test_signup_post_with_invalid_first_name_shows_custom_error_message(self):
        """Test that an invalid first_name triggers the custom regex error message."""
        response = self.client.post(
            self.signup_url, data=self.build_data(first_name="@!#")
        )
        self.assertContains(
            response,
            "Veuillez entrer un nom valide. Seules les lettres, espaces, tirets et apostrophes sont autorisés.",
        )

    def test_signup_post_with_invalid_last_name_shows_custom_error_message(self):
        """Test that an invalid last_name triggers the custom regex error message."""
        response = self.client.post(
            self.signup_url, data=self.build_data(last_name="1234")
        )
        self.assertContains(
            response,
            "Veuillez entrer un nom valide. Seules les lettres, espaces, tirets et apostrophes sont autorisés.",
        )

    def test_signup_confirmation_get_uses_correct_template(self):
        """Test that the signup confirmation view renders the 'accounts/signup/confirmation.html' template."""
        response = self.client.get(self.signup_confirmation_url)
        self.assertTemplateUsed(response, "accounts/signup-confirmation.html")

    def test_signup_confirmation_get_contains_heading(self):
        """Test that the signup confirmation page contains the correct heading."""
        response = self.client.get(self.signup_confirmation_url)
        self.assertContains(
            response,
            "Inscription réussie ! Connectez-vous dès maintenant pour accéder à votre compte.",
        )


class TestLoginView(TestCase):
    """Test cases for verifying the behavior of the login view."""

    @classmethod
    def setUpTestData(cls):
        """Create a test user for login view tests."""
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )

    def setUp(self):
        """Set up URLs and valid login data for reuse in tests."""
        self.home_url = reverse("home")
        self.login_url = reverse("login")
        self.valid_data = {
            "email": "johndoe@gmail.com",
            "password": "paris2024",
        }

    def build_data(self, **overrides):
        """Return a copy of valid_data updated with any overrides."""
        data = self.valid_data.copy()
        data.update(overrides)
        return data

    def test_login_get_returns_http200(self):
        """Test that a GET request to the login view returns HTTP 200 status code."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_get_uses_correct_template(self):
        """Test that the login view renders the 'accounts/login.html' template."""
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_get_contains_heading(self):
        """Test that the login page contains the heading 'Formulaire de connexion'."""
        response = self.client.get(self.login_url)
        self.assertContains(response, "Formulaire de connexion")

    def test_login_link_visible_when_user_not_logged_in(self):
        """
        Test that the login link is visible on the home page when the user
        is not logged in.
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Connexion")

    def test_login_successful(self):
        """User can log in with correct credentials."""
        response = self.client.post(self.login_url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)

    def test_login_successful_redirects_to_home(self):
        """After login, user is redirected to the home page."""
        response = self.client.post(self.login_url, data=self.valid_data)
        self.assertRedirects(response, reverse("home"))

    def test_logout_button_visible_when_user_logged_in(self):
        """After login, the header should contain a logout button."""
        self.client.post(self.login_url, data=self.build_data())
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Déconnexion")

    def test_login_failure_shows_error(self):
        """Login with incorrect credentials shows an error message."""
        response = self.client.post(
            self.login_url, data=self.build_data(password="wrongpassword")
        )
        self.assertContains(
            response,
            "Identifiants invalides. Veuillez vérifier vos identifiants et réessayer.",
        )


class TestLogoutView(TestCase):
    """Test cases for verifying the behavior of the logout view."""

    @classmethod
    def setUpTestData(cls):
        """Create a test user and store credentials and URLs for logout tests."""
        cls.credentials = {
            "email": "johndoe@gmail.com",
            "password": "paris2024",
        }
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )
        cls.home_url = reverse("home")
        cls.login_url = reverse("login")
        cls.logout_url = reverse("logout")

    def test_logout_redirects_to_home(self):
        """Test that logging out redirects the user to the home page."""
        self.client.post(self.login_url, data=self.credentials)
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)

    def test_login_button_visible_when_user_logout_out(self):
        """After logout, the header should contain a login button."""
        self.client.login(
            email=self.credentials["email"], password=self.credentials["password"]
        )
        self.client.get(reverse("logout"))
        response = self.client.get(self.home_url)
        self.assertContains(response, "Connexion")
