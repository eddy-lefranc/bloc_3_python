class Cart:
    """Manage the shopping cart stored in the user's session."""

    def __init__(self, request):
        """Ensure a cart exists in the session, creating it if absent."""

        self.session = request.session
        cart = self.session.get("session_key")

        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}

        self.cart = cart
