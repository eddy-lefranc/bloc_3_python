import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import CustomUserManager
from accounts.validators import name_validator


class User(AbstractUser):
    """
    Custom user model which inherits from Django's AbstractUser, using email as the
    unique identifier instead of username.

    This model removes the 'username' field, replacing it with the 'email' field for
    user authentication.

    The 'first_name' and 'last_name' fields are made required, ensuring that a user's
    full name is always provided. Those fields are also validated using a name
    validation regex.

    The 'registration_key' field creates a random UUID that cannot be edited.
    """

    username = None
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Adresse électronique"
    )
    first_name = models.CharField(
        max_length=150, validators=[name_validator], verbose_name="Prénom"
    )
    last_name = models.CharField(
        max_length=150, validators=[name_validator], verbose_name="Nom"
    )
    registration_key = models.UUIDField(
        max_length=36,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Clé d'inscription",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        """
        Return the user's full name for display purposes, e.g., in the admin interface.
        """
        return f"{self.first_name} {self.last_name}"
