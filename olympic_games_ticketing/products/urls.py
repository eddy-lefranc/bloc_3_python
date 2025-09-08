from django.urls import path

from products.views import offers_list_page

urlpatterns = [
    path("offers/", offers_list_page, name="offers"),
]
