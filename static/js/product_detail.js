// Quantity selector on product detail page
document.querySelectorAll('.btn-quantity-detail').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.dataset.action;
        const quantityInput = document.querySelector('.quantity-input');
        const decreaseButton = document.querySelector('button[data-action="decrease"]');
        const increaseButton = document.querySelector('button[data-action="increase"]');

        let quantity = parseInt(quantityInput.value);

        if (action === 'increase' && quantity < 99) {
            quantity += 1;
        } else if (action === 'decrease' && quantity > 1) {
            quantity -= 1;
        } else {
            return;
        }

        quantityInput.value = quantity;
        decreaseButton.disabled = quantity <= 1;
        increaseButton.disabled = quantity >= 99;
    });
});
