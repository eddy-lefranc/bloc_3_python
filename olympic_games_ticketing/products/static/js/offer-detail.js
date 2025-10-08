/**
 * Initialize the script:
 * - Attach the event listener to the "Add to Cart" button
 */

function initAddToCart() {
  const addToCartButton = document.getElementById("add-to-cart");

  if (addToCartButton) {
    addToCartButton.addEventListener("click", () => {
      const offerId = addToCartButton.value;
      addOfferToCart(offerId);
    });
  }
}

initAddToCart();

/**
 * Send a POST request to add the offer to the cart
 * @param {string|number} offerId - The ID of the offer to add
 */

function addOfferToCart(offerId) {
  const article = document.querySelector(".offer");

  if (!article) {
    console.error("Offre non trouvée.");
    return;
  }

  const url = article.dataset.addToCartUrl;
  const csrfToken = article.dataset.csrfToken;

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrfToken,
    },
    body: new URLSearchParams({
      offer_id: offerId,
      action: "post",
    }),
  })
    .then((response) => response.json())
    .then((data) => updateCartQuantity(data))
    .catch((error) => handleError(error));
}

/**
 * Update the cart quantity in the header
 * @param {Object} data - Response data from the server
 */

function updateCartQuantity(data) {
  const cartQuantityHeader = document.getElementById("cart-quantity-header");

  if (cartQuantityHeader && typeof data.quantity === "number") {
    cartQuantityHeader.textContent = data.quantity;
  }

  alert("Offre ajoutée au panier !");
}

/**
 * Handle request errors
 * @param {Error} error - The error object
 */

function handleError(error) {
  console.error("Erreur lors de l'ajout de l'offre au panier :", error);
  alert("Une erreur s'est produite lors de l'ajout de l'offre au panier.");
}
