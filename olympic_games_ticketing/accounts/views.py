from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.forms import SignupForm


def signup_page(request):
    """
    Display and process the user signup form.

    If the user is already authenticated, redirects to the home page.
    On GET requests, renders an empty signup form.
    On POST requests, validates the submitted data:
    - If valid, creates the user and display a success message on the page.
    - If invalid, re-renders the form with error messages.
    """

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "🥇 Inscription réussie ! Connectez-vous dès maintenant pour accéder à votre compte.",
            )
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", context={"form": form})
