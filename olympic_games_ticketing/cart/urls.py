from django.urls import path

from cart.views import add_offer_to_cart, cart_summary_page, remove_offer_from_cart

urlpatterns = [
    path("summary/", cart_summary_page, name="cart"),
    path("add/", add_offer_to_cart, name="cart-add"),
    path("delete/", remove_offer_from_cart, name="cart-delete"),
]
