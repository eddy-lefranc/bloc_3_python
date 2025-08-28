from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Offer(models.Model):
    """
    Offer model representing tickets and packages for attending the Olympic Games.

    This model captures the essential details of each offer:
    - name: unique title of the offer.
    - price: cost of the offer as a DecimalField.
    - description: detailed textual description.
    - image: optional image illustrating the offer.

    It also includes a slug, the number of seats associated with the offer,
    creation/update timestamps, an active flag, and a sales counter.
    """

    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=120)
    description = models.TextField(blank=True)
    seats = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        editable=False,
    )
    sales = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Return the offer's name for display purposes, e.g., in the admin interface.
        """

        return f"{self.name}"

    def get_absolute_url(self):
        """Returns the URL of the offer detail page based on the slug."""

        return reverse("product", kwargs={"slug": self.slug})
