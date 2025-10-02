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

    return render(request, "cart/cart-summary.html", {"cart": cart})


@login_required
def add_offer_to_cart(
    request,
):
    """
    Add an offer to the shopping cart.

    Handles POST requests to add a single offer to the cart.
    """
    cart = Cart(request)

    if request.POST.get("action") == "post":
        offer_id = int(request.POST.get("offer_id"))
        offer = get_object_or_404(Offer, id=offer_id)
        cart.add_offer(offer=offer)
        cart_quantity = cart.__len__()
        response = JsonResponse({"quantity": cart_quantity})
        return response
