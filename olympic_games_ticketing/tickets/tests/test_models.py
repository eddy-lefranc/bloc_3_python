import uuid

from accounts.models import User
from django.core.files.base import ContentFile
from django.db import models
from django.test import TestCase
from orders.models import Order, OrderItem
from products.models import Offer

from tickets.models import Ticket


class TestTicketModel(TestCase):
    """Tests for verifying the behavior of the Ticket model."""

    @classmethod
    def setUpTestData(cls):
        """Set up a user, order, offer, item and ticket for tests."""
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )
        cls.order = Order.objects.create(user=cls.user, total=75)
        cls.offer = Offer.objects.create(name="Solo", price=25, sales=0)
        cls.item = OrderItem.objects.create(
            order=cls.order,
            offer=cls.offer,
            name=cls.offer.name,
            price=cls.offer.price,
            quantity=1,
        )
        cls.ticket = Ticket.objects.create(order=cls.order, offer=cls.offer)

    def test_order_field_related_model(self):
        """Ensure that order_field correctly references the Order model."""
        order_field = self.ticket._meta.get_field("order")
        self.assertEqual(order_field.related_model, Order)

    def test_order_field_on_delete(self):
        """
        Ensure the on_delete behavior for Ticket.order field is 'models.CASCADE'.
        """
        order_field = self.ticket._meta.get_field("order")
        self.assertEqual(order_field.remote_field.on_delete, models.CASCADE)

    def test_order_field_related_name(self):
        """
        Ensure the related_name on Ticket.order field is 'tickets'.
        """
        order_field = self.ticket._meta.get_field("order")
        self.assertEqual(order_field.remote_field.related_name, "tickets")

    def test_order_field_verbose_name(self):
        """Test that the order field verbose name is correct."""
        order_field_verbose_name = self.ticket._meta.get_field("order").verbose_name
        self.assertEqual(order_field_verbose_name, "Commande liée au billet")

    def test_offer_field_related_model(self):
        """Ensure that offer_field correctly references the Offer model."""
        offer_field = self.ticket._meta.get_field("offer")
        self.assertEqual(offer_field.related_model, Offer)

    def test_offer_field_on_delete(self):
        """
        Ensure the on_delete behavior for Ticket.offer field is 'models.CASCADE'.
        """
        offer_field = self.ticket._meta.get_field("offer")
        self.assertEqual(offer_field.remote_field.on_delete, models.CASCADE)

    def test_offer_field_related_name(self):
        """
        Ensure the related_name on Ticket.offer field is 'tickets'.
        """
        offer_field = self.ticket._meta.get_field("offer")
        self.assertEqual(offer_field.remote_field.related_name, "tickets")

    def test_offer_field_verbose_name(self):
        """Test that the offer field verbose name is correct."""
        offer_field_verbose_name = self.ticket._meta.get_field("offer").verbose_name
        self.assertEqual(offer_field_verbose_name, "Offre liée au billet")

    def test_unique_suffix_field_default_attribute_is_uuid4(self):
        """Test that unique suffix default attribute is 'uuid.uuid4'."""
        unique_suffix_field = self.ticket._meta.get_field("unique_suffix")
        self.assertIs(unique_suffix_field.default, uuid.uuid4)

    def test_unique_suffix_field_editable_attribute_is_false(self):
        """Test that unique suffix is not editable."""
        unique_suffix_field = self.ticket._meta.get_field("unique_suffix")
        self.assertFalse(unique_suffix_field.editable)

    def test_final_key_field_max_length(self):
        """Test that the final key field max_length is 200."""
        final_key_max_length = self.ticket._meta.get_field("final_key").max_length
        self.assertEqual(final_key_max_length, 200)

    def test_final_key_is_unique(self):
        """Test that the final key field has unique=True in the model."""
        final_key_field = self.ticket._meta.get_field("final_key")
        self.assertTrue(final_key_field.unique)

    def test_final_key_field_editable_attribute_is_false(self):
        """Test that final key is not editable."""
        final_key_field = self.ticket._meta.get_field("final_key")
        self.assertFalse(final_key_field.editable)

    def test_qr_code_field_uploads_to_tickets_folder(self):
        """Verify that uploaded qr codes are stored in the 'tickets/' folder."""
        self.ticket.qr_code.save(
            "fake_image.png", ContentFile(b"fake image data"), save=True
        )
        self.assertTrue(self.ticket.qr_code.name.startswith("tickets/"))

    def test_qr_code_field_verbose_name(self):
        """Test that the qr_code field verbose name is correct."""
        qr_code_verbose_name = self.ticket._meta.get_field("qr_code").verbose_name
        self.assertEqual(qr_code_verbose_name, "QR Code")

    def test_qr_code_field_help_text(self):
        """Test that the qr_code field help text has the expected value."""
        qr_code_help_text = self.ticket._meta.get_field("qr_code").help_text
        self.assertEqual(
            qr_code_help_text,
            "Image PNG générée à partir de la clé finale.",
        )

    def test_created_at_field_auto_now_add(self):
        """Test that auto_now_add attribute is True for created_at field."""
        created_at_field = self.ticket._meta.get_field("created_at")
        self.assertTrue(created_at_field.auto_now_add)

    def test_created_at_field_editable_attribute_is_false(self):
        """Test that created_at field is not editable."""
        created_at_field = self.ticket._meta.get_field("created_at")
        self.assertFalse(created_at_field.editable)

    def test_ticket_model_ordering(self):
        """Test that the Ticket model ordering option is correct."""
        self.assertEqual(Ticket._meta.ordering, ["-created_at"])

    def test_ticket_model_verbose_name(self):
        """Test that the Ticket model verbose_name is 'Billet'."""
        self.assertEqual(Ticket._meta.verbose_name, "Billet")

    def test_ticket_model_verbose_name_plural(self):
        """Test that the Order model verbose_name_plural is 'Billets'."""
        self.assertEqual(Ticket._meta.verbose_name_plural, "Billets")

    def test_save_method_generates_final_key(self):
        """
        Ensure that saving a Ticket without an existing final_key
        automatically generates and assigns one.
        """
        ticket = Ticket(order=self.order, offer=self.offer)
        self.assertFalse(ticket.final_key)
        ticket.save()
        self.assertTrue(ticket.final_key)

    def test_generate_qr_code_method_filename(self):
        """
        Verify that generate_qr_code() saves the QR image
        using the expected filename pattern.
        """
        self.ticket.generate_qr_code()
        filename = self.ticket.qr_code.name
        self.assertTrue(
            filename.startswith(f"tickets/ticket_{self.order.id}_{self.offer.id}_")
        )
        self.assertTrue(filename.endswith(".png"))

    def test_str_method_returns_expected_format(self):
        """Test that the __str__ method of Ticket model returns expected_value."""
        expected_value = f"Ticket #{self.ticket.id} - Offre : {self.offer.name} (Commande #{self.order.id})"
        self.assertEqual(str(self.ticket), expected_value)
