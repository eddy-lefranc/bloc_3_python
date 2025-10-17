from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from orders.models import Order

from .models import Ticket


@login_required
@require_POST
def generate_tickets_for_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        return HttpResponseForbidden("Opération non autorisée.")

    if Ticket.objects.filter(order=order).exists():
        return redirect("orders:confirmation")

    with transaction.atomic():
        for item in order.items.select_related("offer"):
            for _ in range(item.offer.seats):
                ticket = Ticket.objects.create(order=order, offer=item.offer)
                ticket.generate_qr_code()

    return redirect("orders:confirmation")
