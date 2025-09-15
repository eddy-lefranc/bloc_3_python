from django.shortcuts import get_object_or_404, render

from products.models import Offer


def offers_list_page(request):
    """
    Renders the offers list page.

    This view displays all the available offers ordered by seat count.
    """

    offers = Offer.objects.filter(is_active=True).order_by("seats")
    context = {"offers": offers}

    return render(request, "products/offers-list.html", context)


def offer_detail_page(request, slug):
    """
    Renders the offer detail page.

    This view displays the details of a single offer identified by its slug.
    """

    offer = get_object_or_404(Offer, slug=slug)
    context = {"offer": offer}

    return render(request, "products/offer-detail.html", context)
