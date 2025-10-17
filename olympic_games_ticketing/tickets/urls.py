from django.urls import path

from .views import generate_tickets_for_order

app_name = "tickets"

urlpatterns = [
    path("generate/<int:order_id>/", generate_tickets_for_order, name="generate"),
]
