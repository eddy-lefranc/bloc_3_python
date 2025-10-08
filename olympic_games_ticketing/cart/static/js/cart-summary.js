/**
 * Initialize the script:
 * - Attach event listeners to all delete buttons
 */
function initDeleteButtons() {
  const deleteButtons = document.querySelectorAll(".delete-button");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const offerId = button.dataset.index;
      deleteOfferFromCart(offerId);
    });
  });
}

initDeleteButtons();

/**
 * Send a POST request to delete the offer from the cart
 * @param {string|number} offerId - The ID of the offer to delete
 */
function deleteOfferFromCart(offerId) {
  const wrapper = document.getElementById("cart-wrapper");

  if (!wrapper) {
    console.error("Panier non trouvé.");
    return;
  }

  const url = wrapper.dataset.deleteUrl;
  const csrfToken = wrapper.dataset.csrfToken;

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
    .then((data) => updateCartAfterDelete(offerId, data))
    .catch((error) => handleDeleteError(error));
}

/**
 * Update the cart UI after a successful deletion
 * @param {string|number} offerId - The ID of the deleted offer
 * @param {Object} data - Response data from the server
 */
function updateCartAfterDelete(offerId, data) {
  const item = document.querySelector(`.cart-item[data-index="${offerId}"]`);
  if (item) {
    item.remove();
  }

  const cartQuantityHeader = document.getElementById("cart-quantity-header");
  const cartQuantitySummary = document.getElementById("cart-quantity-summary");
  const cartTotal = document.getElementById("cart-total");

  if (cartQuantityHeader && typeof data.quantity === "number") {
    cartQuantityHeader.textContent = data.quantity;
  }

  if (cartQuantitySummary && typeof data.quantity === "number") {
    cartQuantitySummary.textContent = data.quantity;
  }

  if (cartTotal && data.total_price !== undefined) {
    cartTotal.textContent = data.total_price;
  }
}

/**
 * Handle errors during the delete request
 * @param {Error} error - The error object
 */
function handleDeleteError(error) {
  console.error("Erreur survenue lors de la suppression de l'offre :", error);
  alert("Une erreur est survenue lors de la suppression de l'offre.");
}
