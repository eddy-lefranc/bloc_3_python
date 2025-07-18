from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    """
    Custom signup form based on Django's UserCreation form.

    This form is used to create a new user. It includes fields for email, first name,
    and last name, while excluding the username field. It also retains the password
    fields (password1 and password2) for account creation.
    """

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
