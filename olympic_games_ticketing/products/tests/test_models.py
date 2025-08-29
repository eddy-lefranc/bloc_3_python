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

    def test_seats_fields_min_value(self):
        """Test that the database rejects less than min value for seats field."""
        with self.assertRaises(IntegrityError):
            Offer.objects.create(
                name="Lorem ipsum",
                slug="solo",
                description="Lorem ipsum dolor sit amet consectetur adipiscing elit.",
                seats=0,
                price=25,
                is_active=True,
            )

    def test_seats_field_help_text(self):
        """Test that the seats field help text has the expected value."""
        seats_field_help_text = self.offer._meta.get_field("seats").help_text
        self.assertEqual(
            seats_field_help_text,
            "Précisez le nombre de places associées à l'offre.",
        )
