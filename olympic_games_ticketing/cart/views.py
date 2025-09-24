from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from products.models import Offer

from .cart import Cart


@login_required
def cart_summary_page(request):
    """
    Render the cart summary page.

    This view displays a summary of the logged-in user's shopping cart.
    """

    cart = Cart(request)
    cart_products = cart.get_products()

    return render(request, "cart/summary.html", {"cart_products": cart_products})


@login_required
def cart_add(request):
    """
    Add an offer to the shopping cart.

    This view handles AJAX POST requests to add an offer to the cart
    and returns the updated cart size as JSON.
    """

    cart = Cart(request)

    if request.POST.get("action") == "post":
        offer_id = int(request.POST.get("offer_id"))
        offer = get_object_or_404(Offer, id=offer_id)

        cart.add(offer)

        cart_size = len(cart.cart)

        return JsonResponse({"size": cart_size})
