from django.shortcuts import render

from products.models import Offer


def offers_list_page(request):
    """
    Renders the offers list page.

    This view displays all the available offers ordered by seat count.
    """

    offers = Offer.objects.filter(is_active=True).order_by("seats")

    return render(request, "products/offers_list.html", {"offers": offers})
