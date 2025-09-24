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

    def add(self, offer):
        """
        Adds a single offer to the cart and stores the relevant information
        in a dictionary.
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

    def get_products(self):
        """Retrieve a QuerySet of Offer instances in the cart and returns it."""

        ids = self.cart.keys()

        return Offer.objects.filter(id__in=ids)
