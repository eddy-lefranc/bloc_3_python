from django.shortcuts import render


def home_page(request):
    """
    Render the home page.

    This view displays the main landing page of the site.
    """
    return render(request, "home.html")
