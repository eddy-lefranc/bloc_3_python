import uuid

from django.conf import settings
from django.db import models
from django.db.models import F
from products.models import Offer


class Order(models.Model):
    """
    Record a user's purchase order.

    Tracks the customer, creation/updated timestamps, total amount,
    unique order key, and a confirmation flag.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Utilisateur ayant effectué la commande",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Date de commande",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name="Date de la dernière mise à jour",
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Montant total de la commande",
    )
    order_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    is_confirmed = models.BooleanField(
        default=True,
        verbose_name="Est confirmé",
    )

    class Meta:
        """
        Meta options for Order model:

        - ordering: sorts Order instances by `updated_at` descending,
        so the most recently modified orders appear first.
        - verbose_name: singular label displayed in the Django admin.
        - verbose_name_plural: plural label displayed in the Django admin.
        """

        ordering = ["-updated_at"]
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        """
        Return a readable representation of the order
        for display purposes (e.g., in the admin interface).

        Format: Commande #<id> - <user> - <status> - <total> €.
        """
        status = "Confirmée" if self.is_confirmed else "Annulée"
        return f"Commande #{self.id} - {self.user} - {status} - {self.total} €"


class OrderItem(models.Model):
    """
    Represents a single item within an order.

    Stores a snapshot of the offer name, unit price, and quantity at
    the time of purchase, while keeping the FK to Offer for analytics.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Commande associée",
    )
    offer = models.ForeignKey(
        Offer,
        related_name="order_items",
        on_delete=models.CASCADE,
        verbose_name="Offre associée",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Nom de l'offre",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire",
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Quantité",
    )

    class Meta:
        """
        Meta options for OrderItem model:

        - ordering: sorts items first by their parent order, then by id.
        - verbose_name: singular label in the Django admin.
        - verbose_name_plural: plural label in the Django admin.
        """

        ordering = ["order", "id"]
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        """
        Return a readable representation of the order item
        for display purposes (e.g., in the admin interface).

        Format: <quantity> x <offer_name> (Commande #<order_id>).
        """
        return f"{self.quantity} x {self.name} (Commande #{self.order.id})"

    def save(self, *args, **kwargs):
        """
        Override save to increment the `sales` field on Offer
        whenever a new OrderItem is created.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            Offer.objects.filter(pk=self.offer.pk).update(
                sales=F("sales") + self.quantity
            )
