from django.core.validators import MinValueValidator
from django.db import models


class Offer(models.Model):
    """
    Offer model representing tickets and packages for attending the Olympic Games.

    This model captures the essential details of each offer:
    - name: unique title of the offer.
    - price: cost of the offer as a DecimalField.
    - description: detailed textual description.
    - thumbnail: image illustrating the offer.

    It also includes a slug, the number of seats associated with the offer,
    creation/update timestamps, an active flag, and a sales counter.
    """

    name = models.CharField(unique=True, max_length=100, verbose_name="Nom")
    slug = models.SlugField(
        unique=True,
        max_length=120,
        help_text="La valeur se remplit automatiquement en renseignant le nom de l'offre.",
    )
    thumbnail = models.ImageField(upload_to="images/", verbose_name="image")
    description = models.TextField(help_text="Ajoutez une description de l'offre.")
    seats = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1, message="Nombre de places minimum : 1")],
        verbose_name="Nombre de places",
        help_text="Précisez le nombre de places associées à l'offre.",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix",
        validators=[
            MinValueValidator(0.01, message="Le prix doit être au moins de 0,01€.")
        ],
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Est en vente",
        help_text="Cochez la case si l'offre est en vente.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Date de la dernière mise à jour",
    )
    sales = models.PositiveIntegerField(
        default=0, verbose_name="Nombre de ventes", editable=False
    )

    def __str__(self):
        """
        Return the offer's name for display purposes, e.g., in the admin interface.
        """

        return self.name
