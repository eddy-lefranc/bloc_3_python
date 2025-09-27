from django.urls import path

from cart.views import add_offer_to_cart, cart_summary_page

urlpatterns = [
    path("summary/", cart_summary_page, name="cart"),
    path("add/", add_offer_to_cart, name="cart-add"),
]
