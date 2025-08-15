from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager that uses email as the unique identifier for
    authentication instead of username.

    This manager ensures that required fields like first name and last name are
    provided at user creation.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a regular user with the given credentials.

        Raises:
            ValueError: If email, first_name, last_name or password is missing.
        """

        if not email:
            raise ValueError(_("Email address is required."))
        if not extra_fields.get("first_name"):
            raise ValueError(_("First name is required."))
        if not extra_fields.get("last_name"):
            raise ValueError(_("Last name is required."))
        if not password:
            raise ValueError(_("Password is required."))

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given credentials.

        Raises:
            ValueError: If is_staff or is_superuser is not set to True.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)
