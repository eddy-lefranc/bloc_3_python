from django.urls import path

from accounts.views import signup_page

urlpatterns = [
    path("signup/", signup_page, name="signup"),
]
