from django.urls import path

from cart.views import cart_add, cart_summary_page

urlpatterns = [
    path("summary/", cart_summary_page, name="cart"),
    path("add/", cart_add, name="cart-add"),
]
