from django.shortcuts import redirect, render

from accounts.decorators import redirect_to_home_if_authenticated
from accounts.forms import SignupForm


@redirect_to_home_if_authenticated
def signup_page(request):
    """
    Display and process the user signup form.

    If the user is already authenticated, redirects to the home page.
    On GET requests, renders an empty signup form.
    On POST requests, validates the submitted data:
    - If valid, creates the user and display a success message on the page.
    - If invalid, re-renders the form with error messages.
    """

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signup-confirmation")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", context={"form": form})


@redirect_to_home_if_authenticated
def signup_confirmation_page(request):
    """
    Display the signup confirmation page for visitors who have just completed
    the registration process. Accessible only to non-authenticated users.
    """

    return render(request, "accounts/signup-confirmation.html")
