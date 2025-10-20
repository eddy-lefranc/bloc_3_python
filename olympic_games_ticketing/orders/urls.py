from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create_view, name="create"),
    path("confirmation/", views.order_confirmation_view, name="confirmation"),
]
