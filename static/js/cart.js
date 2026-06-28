// Helper functions

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
        if (text) {
            text.textContent = 'Free delivery unlocked';
        }
    }
}

function updateDOM(data) {
    // Update totals
    const cartTotalEl = document.querySelector('.cart-total');
    const grandEl = document.querySelector('.cart-grand-total');
    if (cartTotalEl) cartTotalEl.textContent = '$' + parseFloat(data.total).toFixed(2);
    if (grandEl) grandEl.textContent = '$' + parseFloat(data.grand_total).toFixed(2);

    // Update delivery
    const deliveryRow = document.querySelectorAll('.row.mt-3 .col-12.d-flex.justify-content-between')[1];
    if (deliveryRow) {
        const pEls = deliveryRow.querySelectorAll('p.text-muted');
        if (pEls.length >= 2) {
            const deliveryN = parseFloat(data.delivery) || 0;
            pEls[1].textContent = deliveryN === 0 ? 'Free' : '$' + deliveryN.toFixed(2);
        }
    }

    // Update badge
    const count = parseInt(data.product_count) || 0;
    document.querySelectorAll('.cart-badge').forEach(b => b.textContent = count);

    // Update banner
    updateBanner(parseFloat(data.remaining_for_free_delivery) || 0);
}

function sendCartUpdate(form) {
    fetch(form.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: new FormData(form),
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        updateDOM(data);
    })
    .catch(err => console.error('Cart update failed', err));
}

// Event listeners 

// + and - buttons
document.querySelectorAll('button.btn-quantity-cart[data-action]').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.dataset.action;
        const form = this.closest('form');
        const quantityInput = form.querySelector('.quantity-input');
        const decreaseButton = form.querySelector('button[data-action="decrease"]');
        const increaseButton = form.querySelector('button[data-action="increase"]');

        let quantity = parseInt(quantityInput.value);

        if (action === 'increase') {
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

// Manual input
document.querySelectorAll('.quantity-input').forEach(input => {
    input.addEventListener('change', function() {
        let quantity = parseInt(this.value) || 1;
        if (quantity < 1) quantity = 1;
        if (quantity > 99) quantity = 99;
        this.value = quantity;
        sendCartUpdate(this.closest('form'));
    });
});

// Delete button
document.querySelectorAll('form[action*="remove_from_cart"]').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        fetch(form.action, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body: new FormData(form),
            credentials: 'same-origin',
        })
        .then(resp => resp.json())
        .then(data => {
            form.closest('.row').remove();
            updateDOM(data);
        })
        .catch(err => console.error('Remove failed', err));
    });
});

// Prevent default submit for update forms
document.querySelectorAll('form[action*="update_cart"]').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        sendCartUpdate(form);
    });
});
