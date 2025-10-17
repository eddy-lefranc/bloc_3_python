import uuid

from accounts.models import User
from django.db import models
from django.test import TestCase

from orders.models import Order


class TestOrderModel(TestCase):
    """Tests for verifying the behavior of the Order model."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user and order for all tests."""
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )
        cls.order = Order.objects.create(user=cls.user, total=75)

    def test_user_field_relationship(self):
        """
        Ensure that the user field correctly references the User who placed the order.
        """
        self.assertEqual(self.order.user, self.user)

    def test_user_field_on_delete(self):
        """
        Ensure the on_delete behavior for Order.user field is 'models.CASCADE'.
        """
        user_field = Order._meta.get_field("user")
        self.assertEqual(user_field.remote_field.on_delete, models.CASCADE)

    def test_user_field_related_name(self):
        """
        Ensure the related_name on Order.user field is 'orders'.
        """
        user_field = Order._meta.get_field("user")
        self.assertEqual(user_field.remote_field.related_name, "orders")

    def test_first_name_field_verbose_name(self):
        """Test that the user field verbose name is correct."""
        user_field_verbose_name = Order._meta.get_field("user").verbose_name
        self.assertEqual(
            user_field_verbose_name, "Utilisateur ayant effectué la commande"
        )

    def test_created_at_field_auto_now_add(self):
        """Test that auto_now_add attribute is True for created_at field."""
        created_at_field = self.order._meta.get_field("created_at")
        self.assertTrue(created_at_field.auto_now_add)

    def test_created_at_field_editable_attribute_is_false(self):
        """Test that created_at field is not editable."""
        created_at_field = self.order._meta.get_field("created_at")
        self.assertFalse(created_at_field.editable)

    def test_created_at_field_verbose_name(self):
        """Test that the created_at field verbose name is 'Date de commande'."""
        created_at_field_verbose_name = self.order._meta.get_field(
            "created_at"
        ).verbose_name
        self.assertEqual(created_at_field_verbose_name, "Date de commande")

    def test_updated_at_field_auto_now_add(self):
        """Test that auto_now attribute is True for updated_at field."""
        updated_at_field = self.order._meta.get_field("updated_at")
        self.assertTrue(updated_at_field.auto_now)

    def test_updated_at_field_editable_attribute_is_false(self):
        """Test that updated_at field is not editable."""
        updated_at_field = self.order._meta.get_field("updated_at")
        self.assertFalse(updated_at_field.editable)

    def test_updated_at_field_verbose_name(self):
        """Test that the updated_at field verbose name is correct."""
        updated_at_field_verbose_name = self.order._meta.get_field(
            "updated_at"
        ).verbose_name
        self.assertEqual(
            updated_at_field_verbose_name, "Date de la dernière mise à jour"
        )

    def test_total_field_value(self):
        """Test that the total field stores the expected value."""
        self.assertEqual(self.order.total, 75)

    def test_total_field_max_digits(self):
        """Test that total field max digits has the expected value."""
        total_field_max_digits = self.order._meta.get_field("total").max_digits
        self.assertEqual(total_field_max_digits, 10)

    def test_total_field_decimal_places(self):
        """Test that total field decimal places has the expected value."""
        total_field_decimal_places = self.order._meta.get_field("total").decimal_places
        self.assertEqual(total_field_decimal_places, 2)

    def test_total_field_verbose_name(self):
        """Test that the total field verbose name is correct."""
        total_field_verbose_name = self.order._meta.get_field("total").verbose_name
        self.assertEqual(total_field_verbose_name, "Montant total de la commande")

    def test_order_key_field_is_generated(self):
        """Test that a order key is generated for the order."""
        self.assertIsNotNone(self.order.order_key)

    def test_order_key_field_default_attribute_is_uuid4(self):
        """Test that order key default attribute is 'uuid.uuid4'."""
        order_key_field = self.order._meta.get_field("order_key")
        self.assertIs(order_key_field.default, uuid.uuid4)

    def test_order_key_field_editable_attribute_is_false(self):
        """Test that order key is not editable."""
        order_key_field = self.order._meta.get_field("order_key")
        self.assertFalse(order_key_field.editable)

    def test_is_confirmed_field_default_value(self):
        """Test that the is_confirmed field has the expected default value."""
        is_confirmed_default_value = self.order._meta.get_field("is_confirmed").default
        self.assertEqual(is_confirmed_default_value, True)

    def test_is_confirmed_field_verbose_name(self):
        """Test that the is_confirmed field verbose name is correct."""
        is_confirmed_verbose_name = self.order._meta.get_field(
            "is_confirmed"
        ).verbose_name
        self.assertEqual(is_confirmed_verbose_name, "Est confirmé")


class TestOrderItemModel(TestCase):
    """Tests for verifying the behavior of the OrderItem model."""
