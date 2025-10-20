import io
import uuid

import qrcode
from django.core.files.base import ContentFile
from django.db import models
from orders.models import Order
from products.models import Offer


class Ticket(models.Model):
    """
    Represents a unique QR-code ticket for a specific order.

    Each Ticket corresponds to one seat within its Order and includes these fields:

    - order: order to which the ticket is linked.
    - offer: offer to which the ticket is linked.
    - unique_suffix: a randomly generated UUID ensuring
      that each ticket within the same order remains unique.
    - final_key: unique key encoded in the QR code.
    - qr_code: PNG image file generated from final_key.
    - created_at: ticket creation timestamp.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Commande liée au billet",
    )
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Offre liée au billet",
    )
    unique_suffix = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    final_key = models.CharField(
        max_length=200,
        unique=True,
        editable=False,
    )
    qr_code = models.ImageField(
        upload_to="tickets/",
        verbose_name="QR Code",
        help_text="Image PNG générée à partir de la clé finale.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        """
        Meta options for Ticket model:

        - Ordering: displays the most recent tickets first.
        - verbose_name: singular label displayed in the Django admin.
        - verbose_name_plural: plural label displayed in the Django admin.
        """

        ordering = ["-created_at"]
        verbose_name = "Billet"
        verbose_name_plural = "Billets"

    def save(self, *args, **kwargs):
        """
        Override save to generate the final key if it does not exist.
        """
        if not self.final_key:
            registration_key = self.order.user.registration_key
            order_key = self.order.order_key
            self.final_key = f"{registration_key}-{order_key}-{self.unique_suffix}"
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        """
        Generate and attach the QR code image for the ticket.

        The image is stored in the qr_code field under a unique filename
        combining the order ID, offer ID, and the ticket's unique suffix.
        """
        qr_img = qrcode.make(self.final_key)
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)
        filename = f"ticket_{self.order.id}_{self.offer.id}_{self.unique_suffix}.png"
        self.qr_code.save(filename, ContentFile(buffer.read()), save=True)

    def __str__(self):
        """
        Return a readable representation of the Ticket
        for display purposes (e.g., in the admin interface).
        """
        return (
            f"Ticket #{self.id} - Offre : {self.offer.name} (Commande #{self.order.id})"
        )
