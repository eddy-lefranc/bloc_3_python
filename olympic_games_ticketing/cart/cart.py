from decimal import Decimal

from products.models import Offer


class Cart:
    """Manage the shopping cart stored in the user's session."""

    def __init__(self, request):
        """Ensure a cart exists in the session, creating it if absent."""
        self.session = request.session
        cart = self.session.get("session_key")

        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        self.cart = cart

    def add_offer(self, offer):
        """
        Add a single offer to the cart.

        Each offer can only appear once in the cart. If the offer is not already
        in the cart, it is added with its details.
        """
        offer_id = str(offer.id)

        if offer_id not in self.cart:
            self.cart[offer_id] = {
                "name": offer.name,
                "image": offer.thumbnail.url,
                "seats": offer.seats,
                "price": str(offer.price),
                "quantity": 1,
            }

        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and enrich them with related Offer objects,
        decimal prices, and total line prices.
        """
        offer_ids = self.cart.keys()
        offers = Offer.objects.filter(is_active=True, id__in=offer_ids)
        cart = self.cart.copy()

        for offer in offers:
            cart[str(offer.id)]["offer"] = offer

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Return the total quantity of all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Return the total price of the cart."""
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
