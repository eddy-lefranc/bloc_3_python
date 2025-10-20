from cart.cart import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from tickets.models import Ticket

from .models import Order, OrderItem


@require_POST
@login_required
def order_create_view(request):
    """
    Create a new Order and generate QR-code tickets from the session cart.

    - Requires an authenticated user and only handles POST requests.
    - Redirects to the cart page with an error message if the cart is empty.
    - Within an atomic transaction:
        - Creates the Order for the current user with the cart's total price.
        - Bulk-creates OrderItem instances for each cart entry.
        - For each OrderItem, creates one Ticket per seat and calls
          ticket.generate_qr_code() to render and save the QR code.
        - Clears the cart and redirects to the order confirmation page.
    """

    cart = Cart(request)
    if len(cart) == 0:
        messages.error(
            request,
            "Votre panier est vide. Veuillez ajouter au moins une offre avant de commander.",
        )
        return redirect("cart")

    with transaction.atomic():
        order = Order.objects.create(user=request.user, total=cart.get_total_price())
        items_to_create = [
            OrderItem(
                order=order,
                offer=item["offer"],
                name=item["name"],
                price=item["price"],
                quantity=item["quantity"],
            )
            for item in cart
        ]
        OrderItem.objects.bulk_create(items_to_create)

        for item in order.items.select_related("offer"):
            for _ in range(item.offer.seats):
                ticket = Ticket.objects.create(order=order, offer=item.offer)
                ticket.generate_qr_code()

        cart.clear()

        return redirect("orders:confirmation")


@login_required
def order_confirmation_view(request):
    """
    Display the confirmation page for the user's most recent order.

    - Retrieves the latest Order for the authenticated user; otherwise,
      renders the confirmation template with order set to None.
    - Fetches all Ticket instances for that order, grouped by offer name.
    - Renders "orders/order-confirmation.html" with context:
        - order: the retrieved Order or None.
        - tickets_by_offer: dict mapping offer names to lists of Ticket objects.
    """

    order = (
        request.user.orders.prefetch_related("items__offer")
        .order_by("-created_at")
        .first()
    )
    if not order:
        return render(request, "orders/order-confirmation.html", {"order": None})

    tickets = Ticket.objects.filter(order=order).select_related("offer")
    tickets_by_offer = {}
    for ticket in tickets:
        offer_name = ticket.offer.name
        tickets_by_offer.setdefault(offer_name, []).append(ticket)

    return render(
        request,
        "orders/order-confirmation.html",
        {
            "order": order,
            "tickets_by_offer": tickets_by_offer,
        },
    )
