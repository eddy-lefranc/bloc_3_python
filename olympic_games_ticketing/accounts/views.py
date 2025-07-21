from django.shortcuts import redirect, render

from accounts.forms import SignupForm


def signup_page(request):
    """
    Display and process the user signup form.

    If the user is already authenticated, redirects to the home page.
    On GET requests, renders an empty signup form.
    On POST requests, validates the submitted data:
    - If valid, creates the user and redirects to the signup confirmation page.
    - If invalid, re-renders the form with error messages.
    """

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signup-confirmation")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", context={"form": form})


def signup_confirmation_page(request):
    """
    Render the signup confirmation page.

    Displays a simple confirmation message after successful registration.
    """

    return render(request, "accounts/signup-confirmation.html")
