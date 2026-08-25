// Helper functions

/**
 * Shows or hides the free-delivery banner and updates its message based on
 * how much more the customer needs to spend to unlock free delivery.
 * @param {number} remaining - Amount remaining until free delivery, in dollars.
 */
function updateBanner(remaining) {
    const banner = document.querySelector('#free-delivery-banner');
    if (!banner) return;
    const text = banner.querySelector('.free-delivery-banner-text');
    if (remaining > 0) {
        banner.classList.remove('d-none');
        if (text) {
            text.innerHTML = `Add <strong>$${remaining.toFixed(2)}</strong> for free delivery`;
        }
    } else {
        banner.classList.add('d-none');
    }
}

/**
 * Refreshes the cart totals, delivery cost, item-count badges, and
 * free-delivery banner from the latest cart data returned by the server.
 * @param {Object} data - Cart data returned by the cart API.
 * @param {number|string} data.total - Cart subtotal.
 * @param {number|string} data.grand_total - Cart total including delivery.
 * @param {number|string} data.delivery - Delivery cost.
 * @param {number|string} data.product_count - Total number of items in the cart.
 * @param {number|string} data.remaining_for_free_delivery - Amount left to unlock free delivery.
 */
function updateCartDisplay(data) {
    // Update totals
    const cartTotalEl = document.querySelector('.cart-total');
    const grandEl = document.querySelector('.cart-grand-total');
    if (cartTotalEl) cartTotalEl.textContent = '$' + parseFloat(data.total).toFixed(2);
    if (grandEl) grandEl.textContent = '$' + parseFloat(data.grand_total).toFixed(2);

    // Update delivery
    const deliveryValue = document.querySelector('.cart-delivery-row dd');
    if (deliveryValue) {
        const deliveryN = parseFloat(data.delivery) || 0;
        deliveryValue.textContent = deliveryN === 0 ? 'Free' : '$' + deliveryN.toFixed(2);
    }

    // Update badge
    const count = parseInt(data.product_count) || 0;
    document.querySelectorAll('.cart-badge').forEach(badge => badge.textContent = count);

    // Update banner
    updateBanner(parseFloat(data.remaining_for_free_delivery) || 0);
}

/**
 * Submits a cart form's data to the server via AJAX and refreshes the cart
 * display with the response.
 * @param {HTMLFormElement} form - The cart quantity form to submit.
 */
function sendCartUpdate(form) {
    fetch(form.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: new FormData(form),
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        updateCartDisplay(data);
    })
    .catch(err => console.error('Cart update failed', err));
}

// Event listeners

/**
 * Wires up each quantity +/- button to adjust the quantity input and push
 * the change to the server.
 * @param {HTMLButtonElement} button - The increase/decrease button being configured.
 */
document.querySelectorAll('button.btn-quantity-cart[data-action]').forEach(button => {
    button.addEventListener('click', function () {
        const action = this.dataset.action;
        const form = this.closest('form');
        const quantityInput = form.querySelector('.quantity-input');
        const decreaseButton = form.querySelector('button[data-action="decrease"]');
        const increaseButton = form.querySelector('button[data-action="increase"]');

        let quantity = parseInt(quantityInput.value);

        if (action === 'increase' && quantity < 99) {
            quantity += 1;
        } else if (action === 'decrease' && quantity > 1) {
            quantity -= 1;
        } else {
            return;
        }

        quantityInput.value = quantity;
        if (decreaseButton) decreaseButton.disabled = quantity <= 1;
        if (increaseButton) increaseButton.disabled = quantity >= 99;
        sendCartUpdate(form);
    });
});

/**
 * Wires up each quantity input for manual entry, clamping the value to a
 * valid range and pushing the change to the server.
 * @param {HTMLInputElement} input - The quantity input being configured.
 */
document.querySelectorAll('.quantity-input').forEach(input => {
    input.addEventListener('change', function () {
        let quantity = parseInt(this.value) || 1;
        if (quantity < 1) quantity = 1;
        if (quantity > 99) quantity = 99;
        this.value = quantity;
        sendCartUpdate(this.closest('form'));
    });
});

/**
 * Wires up each "remove item" form to delete the item via AJAX instead of a
 * full page submit, reloading the page if the cart becomes empty.
 * @param {HTMLFormElement} form - The remove-item form being configured.
 */
document.querySelectorAll('form[action*="/cart/remove/"]').forEach(form => {
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        fetch(form.action, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body: new FormData(form),
            credentials: 'same-origin',
        })
        .then(resp => resp.json())
        .then(data => {
            if (parseInt(data.product_count) === 0) {
                window.location.reload();
                return;
            }
            form.closest('.cart-item-row')?.remove();
            updateCartDisplay(data);
        })
        .catch(err => console.error('Remove failed', err));
    });
});

/**
 * Prevents the default submit for quantity-update forms, since quantity
 * changes are already sent to the server via the buttons/input above.
 * @param {HTMLFormElement} form - The quantity-update form being configured.
 */
document.querySelectorAll('form[action*="/cart/update/"]').forEach(form => {
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        sendCartUpdate(form);
    });
});
