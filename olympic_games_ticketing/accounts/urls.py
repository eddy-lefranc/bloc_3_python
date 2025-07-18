from django.urls import path

from accounts.views import signup_confirmation_page, signup_page

urlpatterns = [
    path("signup/", signup_page, name="signup"),
    path("signup/confirmation/", signup_confirmation_page, name="signup-confirmation"),
]
