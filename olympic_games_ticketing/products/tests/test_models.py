from django.db import IntegrityError
from django.test import TestCase

from products.models import Offer


class TestOfferModel(TestCase):
    """Tests for verifying the behavior of the offer model."""

    @classmethod
    def setUpTestData(cls):
        """Set up a test offer and retrieve the offer for tests."""
        Offer.objects.create(
            name="Solo",
            slug="solo",
            description="Lorem ipsum dolor sit amet consectetur adipiscing elit.",
            seats=1,
            price=25,
            is_active=True,
        )
        cls.offer = Offer.objects.get(id=1)

    def test_name_field_value(self):
        """Test that the name field stores the expected value."""
        self.assertEqual(self.offer.name, "Solo")

    def test_name_field_is_unique(self):
        """Test that the name field has unique=True in the model."""
        name_field = self.offer._meta.get_field("name")
        self.assertTrue(name_field.unique)

    def test_duplicate_name_raises_IntegrityError(self):
        """Test that the database rejects duplicate names."""
        with self.assertRaises(IntegrityError):
            Offer.objects.create(
                name="Solo",
                slug="lorem-ipsum",
                description="Lorem ipsum dolor sit amet consectetur adipiscing elit.",
                seats=1,
                price=25,
                is_active=True,
            )

    def test_name_field_max_length(self):
        """Test that the max length for the name field is 100."""
        name_field_max_length = self.offer._meta.get_field("name").max_length
        self.assertEqual(name_field_max_length, 100)

    def test_name_field_verbose_name(self):
        """Test that the name field verbose name is 'Nom'."""
        name_field_verbose_name = self.offer._meta.get_field("name").verbose_name
        self.assertEqual(name_field_verbose_name, "Nom")

    def test_slug_field_value(self):
        """Test that the slug field stores the expected value."""
        self.assertEqual(self.offer.slug, "solo")

    def test_slug_field_is_unique(self):
        """Test that the slug field has unique=True in the model."""
        slug_field = self.offer._meta.get_field("slug")
        self.assertTrue(slug_field.unique)

    def test_duplicate_slug_raises_IntegrityError(self):
        """Test that the database rejects duplicate slugs."""
        with self.assertRaises(IntegrityError):
            Offer.objects.create(
                name="Lorem ipsum",
                slug="solo",
                description="Lorem ipsum dolor sit amet consectetur adipiscing elit.",
                seats=1,
                price=25,
                is_active=True,
            )

    def test_slug_field_max_length(self):
        """Test that the max length for the slug field is 120."""
        slug_field_max_length = self.offer._meta.get_field("slug").max_length
        self.assertEqual(slug_field_max_length, 120)

    def test_slug_field_help_text(self):
        """Test that the slug field help text has the expected value."""
        slug_field_help_text = self.offer._meta.get_field("slug").help_text
        self.assertEqual(
            slug_field_help_text,
            "La valeur se remplit automatiquement en renseignant le nom de l'offre.",
        )

    def test_description_field_value(self):
        """Test that the description field stores the expected value."""
        self.assertEqual(
            self.offer.description,
            "Lorem ipsum dolor sit amet consectetur adipiscing elit.",
        )

    def test_description_field_help_text(self):
        """Test that the description field help text has the expected value."""
        description_field_help_text = self.offer._meta.get_field(
            "description"
        ).help_text
        self.assertEqual(
            description_field_help_text, "Ajoutez une description de l'offre."
        )

    def test_seats_field_value(self):
        """Test that the seats field stores the expected value."""
        self.assertEqual(self.offer.seats, 1)

    def test_seats_field_default_value(self):
        """Test that the seats field has the expected default value."""
        seats_field_default_value = self.offer._meta.get_field("seats").default
        self.assertEqual(seats_field_default_value, 1)

    def test_seats_field_help_text(self):
        """Test that the seats field help text has the expected value."""
        seats_field_help_text = self.offer._meta.get_field("seats").help_text
        self.assertEqual(
            seats_field_help_text,
            "Précisez le nombre de places associées à l'offre.",
        )

    def test_price_field_value(self):
        """Test that the price field stores the expected value."""
        self.assertEqual(self.offer.price, 25)

    def test_price_field_max_digits(self):
        """Test that price field max digits has the expected value."""
        price_field_max_digits = self.offer._meta.get_field("price").max_digits
        self.assertEqual(price_field_max_digits, 10)

    def test_price_field_decimal_places(self):
        """Test that price field decimal places has the expected value."""
        price_field_decimal_places = self.offer._meta.get_field("price").decimal_places
        self.assertEqual(price_field_decimal_places, 2)

    def test_price_field_verbose_name(self):
        """Test that the price field verbose name is 'Prix'."""
        price_field_verbose_name = self.offer._meta.get_field("price").verbose_name
        self.assertEqual(price_field_verbose_name, "Prix")

    def test_is_active_field_value(self):
        """Test that the is_active field stores the expected value."""
        self.assertTrue(self.offer.is_active)

    def test_is_active_field_default_value(self):
        """Test that the is_active field has the expected default value."""
        is_active_field = self.offer._meta.get_field("is_active")
        self.assertTrue(is_active_field.default)

    def test_is_active_field_verbose_name(self):
        """Test that the is_active field verbose name is 'Est en vente'."""
        is_active_field_verbose_name = self.offer._meta.get_field(
            "is_active"
        ).verbose_name
        self.assertEqual(is_active_field_verbose_name, "Est en vente")

    def test_is_active_field_help_text(self):
        """Test that the is_active field help text has the expected value."""
        is_active_field_help_text = self.offer._meta.get_field("is_active").help_text
        self.assertEqual(
            is_active_field_help_text,
            "Cochez la case si l'offre est en vente.",
        )

    def test_created_at_field_auto_now_add(self):
        """Test that auto_now_add attribute is True for created_at field."""
        created_at_field = self.offer._meta.get_field("created_at")
        self.assertTrue(created_at_field.auto_now_add)

    def test_created_at_field_editable_attribute_is_false(self):
        """Test that created_at field is not editable."""
        created_at_field = self.offer._meta.get_field("created_at")
        self.assertFalse(created_at_field.editable)

    def test_created_at_field_verbose_name(self):
        """Test that the created_at field verbose name is 'Date de création'."""
        is_active_field_verbose_name = self.offer._meta.get_field(
            "created_at"
        ).verbose_name
        self.assertEqual(is_active_field_verbose_name, "Date de création")

    def test_updated_at_field_auto_now_add(self):
        """Test that auto_now attribute is True for updated_at field."""
        updated_at_field = self.offer._meta.get_field("updated_at")
        self.assertTrue(updated_at_field.auto_now)

    def test_updated_at_field_editable_attribute_is_false(self):
        """Test that updated_at field is not editable."""
        updated_at_field = self.offer._meta.get_field("updated_at")
        self.assertFalse(updated_at_field.editable)

    def test_updated_at_field_verbose_name(self):
        """Test that the updated_at field verbose name is correct."""
        updated_at_field_verbose_name = self.offer._meta.get_field(
            "updated_at"
        ).verbose_name
        self.assertEqual(
            updated_at_field_verbose_name, "Date de la dernière mise à jour"
        )

    def test_sales_field_default_value(self):
        """Test that the sales field has the expected default value."""
        sales_field_default_value = self.offer._meta.get_field("sales").default
        self.assertEqual(sales_field_default_value, 0)

    def test_sales_field_verbose_name(self):
        """Test that the sales field verbose name is 'Nombre de ventes'."""
        sales_field_verbose_name = self.offer._meta.get_field("sales").verbose_name
        self.assertEqual(sales_field_verbose_name, "Nombre de ventes")

    def test_sales_field_editable_attribute_is_false(self):
        """Test that sales field is not editable."""
        sales_field = self.offer._meta.get_field("updated_at")
        self.assertFalse(sales_field.editable)

    def test_str_method_returns_offer_name(self):
        """Test that the __str__ method returns the name of the offer."""
        self.assertEqual(str(self.offer), "Solo")
