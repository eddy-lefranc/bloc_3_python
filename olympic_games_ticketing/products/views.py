from django.shortcuts import render


def offers_list_page(request):
    """
    Render the offers list page.

    This view displays all the available offers
    """

    return render(request, "products/offers_list.html")
