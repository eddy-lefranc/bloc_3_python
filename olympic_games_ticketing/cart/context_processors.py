from .cart import Cart


def cart(request):
    """Add the shopping cart instance to the template context."""
    return {"cart": Cart(request)}
