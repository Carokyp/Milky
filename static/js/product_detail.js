// Quantity selector on product detail page
document.querySelectorAll('.btn-quantity-detail').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.dataset.action;
        const quantityInput = document.querySelector('.quantity-input');
        const quantityDisplay = document.querySelector('.quantity-value');

        let quantity = parseInt(quantityInput.value);

        if (action === 'increase') {
            quantity += 1;
        } else if (action === 'decrease' && quantity > 1) {
            quantity -= 1;
        }

        quantityInput.value = quantity;
        quantityDisplay.textContent = quantity;
    });
});