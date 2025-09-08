from django.shortcuts import render


def cart_summary_page(request):
    """
    Render the cart summary page.

    This view displays the summary of the user's cart.
    """

    return render(request, "cart/summary.html")
