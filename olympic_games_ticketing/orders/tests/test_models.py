import uuid

from accounts.models import User
from django.db import models
from django.test import TestCase
from products.models import Offer

from orders.models import Order, OrderItem


class TestOrderModel(TestCase):
    """Tests for verifying the behavior of the Order model."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user for all tests."""
        cls.user = User.objects.create_user(
            email="johndoe@gmail.com",
            first_name="John",
            last_name="Doe",
            password="paris2024",
        )

    def setUp(self):
        """Set up a test an order for all tests."""
        self.order = Order.objects.create(user=self.user, total=75)

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

    def test_user_field_verbose_name(self):
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

    def test_order_model_ordering(self):
        """Test that the Order model ordering option is correct."""
        self.assertEqual(Order._meta.ordering, ["-updated_at"])

    def test_order_model_verbose_name(self):
        """Test that the Order model verbose_name is 'Commande'."""
        self.assertEqual(Order._meta.verbose_name, "Commande")

    def test_order_model_verbose_name_plural(self):
        """Test that the Order model verbose_name_plural is 'Commandes'."""
        self.assertEqual(Order._meta.verbose_name_plural, "Commandes")

    def test_str_method_returns_confirmed_status(self):
        """Test that the __str__ method returns expected_value if confirmed."""
        expected_value = f"Commande #{self.order.id} - {self.user} - Confirmée - 75 €"
        self.assertEqual(str(self.order), expected_value)

    def test_str_method_returns_cancelled_status(self):
        """Test that the __str__ method returns expected_value if not confirmed."""
        self.order.is_confirmed = False
        self.order.save()
        expected_value = f"Commande #{self.order.id} - {self.user} - Annulée - 75 €"
        self.assertEqual(str(self.order), expected_value)


class TestOrderItemModel(TestCase):
    """Tests for verifying the behavior of the OrderItem model."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test user for all tests."""
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

    def test_order_field_related_model(self):
        """Ensure that order_field correctly references the Order model."""
        order_field = OrderItem._meta.get_field("order")
        self.assertEqual(order_field.related_model, Order)

    def test_order_field_on_delete(self):
        """
        Ensure the on_delete behavior for OrderItem.order field is 'models.CASCADE'.
        """
        order_field = OrderItem._meta.get_field("order")
        self.assertEqual(order_field.remote_field.on_delete, models.CASCADE)

    def test_order_field_related_name(self):
        """
        Ensure the related_name on OrderItem.order field is 'items'.
        """
        order_field = OrderItem._meta.get_field("order")
        self.assertEqual(order_field.remote_field.related_name, "items")

    def test_order_field_verbose_name(self):
        """Test that the order field verbose name is correct."""
        order_field_verbose_name = OrderItem._meta.get_field("order").verbose_name
        self.assertEqual(order_field_verbose_name, "Commande associée")

    def test_offer_field_related_model(self):
        """Ensure that offer_field correctly references the Offer model."""
        offer_field = OrderItem._meta.get_field("offer")
        self.assertEqual(offer_field.related_model, Offer)

    def test_offer_field_related_name(self):
        """
        Ensure the related_name on OrderItem.offer field is 'order_items'.
        """
        offer_field = OrderItem._meta.get_field("offer")
        self.assertEqual(offer_field.remote_field.related_name, "order_items")

    def test_offer_field_on_delete(self):
        """
        Ensure the on_delete behavior for OrderItem.offer field is 'models.CASCADE'.
        """
        offer_field = OrderItem._meta.get_field("offer")
        self.assertEqual(offer_field.remote_field.on_delete, models.CASCADE)

    def test_offer_field_verbose_name(self):
        """Test that the offer field verbose name is correct."""
        offer_field_verbose_name = OrderItem._meta.get_field("offer").verbose_name
        self.assertEqual(offer_field_verbose_name, "Offre associée")

    def test_name_field_max_length(self):
        """Test that the name field max_length is 255."""
        name_field_max_length = OrderItem._meta.get_field("name").max_length
        self.assertEqual(name_field_max_length, 255)

    def test_name_field_verbose_name(self):
        """Test that the name field verbose name is correct."""
        name_field_verbose_name = OrderItem._meta.get_field("name").verbose_name
        self.assertEqual(name_field_verbose_name, "Nom de l'offre")

    def test_price_field_max_digits(self):
        """Test that price field max digits has the expected value."""
        price_field_max_digits = OrderItem._meta.get_field("price").max_digits
        self.assertEqual(price_field_max_digits, 10)

    def test_price_field_decimal_places(self):
        """Test that price field decimal places has the expected value."""
        price_field_decimal_places = OrderItem._meta.get_field("price").decimal_places
        self.assertEqual(price_field_decimal_places, 2)

    def test_price_field_verbose_name(self):
        """Test that the price field verbose name is correct."""
        price_field_verbose_name = OrderItem._meta.get_field("price").verbose_name
        self.assertEqual(price_field_verbose_name, "Prix unitaire")

    def test_quantity_field_verbose_name(self):
        """Test that the quantity field verbose name is correct."""
        quantity_field_verbose_name = OrderItem._meta.get_field("quantity").verbose_name
        self.assertEqual(quantity_field_verbose_name, "Quantité")

    def test_order_item_model_ordering(self):
        """Test that the OrderItem model ordering option is correct."""
        self.assertEqual(OrderItem._meta.ordering, ["order", "id"])

    def test_order_item_model_verbose_name(self):
        """Test that the OrderItem model verbose_name is correct."""
        self.assertEqual(OrderItem._meta.verbose_name, "Article de commande")

    def test_order_item_model_verbose_name_plural(self):
        """Test that the OrderItem model verbose_name_plural is correct."""
        self.assertEqual(OrderItem._meta.verbose_name_plural, "Articles de commande")

    def test_str_method_returns_expected_format(self):
        """Test that the __str__ method of OrderItem model returns expected_value."""
        expected_value = (
            f"{self.item.quantity} x {self.item.name} (Commande #{self.order.id})"
        )
        self.assertEqual(str(self.item), expected_value)

    def test_offer_sales_incremented_on_order_item_creation(self):
        """
        Test that creating an OrderItem increments the related Offer sales field
        from its initial value (0 in setUpTestData).
        """
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.sales, self.item.quantity)
