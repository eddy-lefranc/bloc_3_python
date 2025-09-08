from django.urls import path

from cart.views import cart_summary_page

urlpatterns = [
    path("summary/", cart_summary_page, name="cart"),
]
