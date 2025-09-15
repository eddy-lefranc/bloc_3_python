from django.urls import path

from products.views import offer_detail, offers_list_page

urlpatterns = [
    path("offers/", offers_list_page, name="offers"),
    path("offers/<str:slug>/", offer_detail, name="offer"),
]
