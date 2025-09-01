from django.contrib import admin

from products.models import Offer


class ProductAdmin(admin.ModelAdmin):
    """
    This ModelAdmin class use a prepopulated_field to avoid manually adding a slug.
    """

    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Offer, ProductAdmin)
