from functools import wraps

from django.shortcuts import redirect


def redirect_to_home_if_authenticated(view_func):
    """Redirect to the home page if the user is already logged in."""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view
