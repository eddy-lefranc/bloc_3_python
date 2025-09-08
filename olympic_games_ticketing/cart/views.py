from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def cart_summary_page(request):
    """
    Render the cart summary page.

    This view displays a summary of the logged-in user's shopping cart.
    """

    return render(request, "cart/summary.html")
