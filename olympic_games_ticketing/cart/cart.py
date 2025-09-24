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

    def add(self, product):
        """
        Adds a single product to the basket and stores the relevant information
        in a dictionary.
        """

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "name": product.name,
                "image": product.thumbnail.url,
                "seats": product.seats,
                "price": str(product.price),
                "quantity": 1,
            }

        self.session.modified = True

    def __len__(self):
        """Return the number of items in the cart."""

        return len(self.cart)

    def get_products(self):
        """Retrieve a QuerySet of Offer instances in the cart."""

        ids = self.cart.keys()
        products = Offer.objects.filter(id__in=ids)

        return products
