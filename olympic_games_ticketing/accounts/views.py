from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from accounts.decorators import redirect_to_home_if_authenticated
from accounts.forms import LoginForm, SignupForm


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


@redirect_to_home_if_authenticated
def login_page(request):
    """
    Handles user login. Displays the login form and processes form submission.

    Supports POST requests to handle form submission. Other request methods (e.g., GET)
    simply display an empty login form.

    If the form is valid, the user is logged in and redirected to the home page.
    If the form is not valid, the page reloads with error messages.
    """

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"], password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(
                    request,
                    "Identifiants invalides. Veuillez vérifier vos identifiants et réessayer.",
                )
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", context={"form": form})


def logout_user(request):
    """Log out the current user and redirect to the homepage."""
    logout(request)
    return redirect("home")
