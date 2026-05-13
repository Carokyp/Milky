

// Update quantity when clicking + or -
    document.querySelectorAll('.btn-quantity').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const action = this.dataset.action;
            const form = this.closest('form');
            const quantityInput = form.querySelector('.quantity-input');
            const quantityDisplay = form.querySelector('.quantity-value');
            
            let quantity = parseInt(quantityInput.value);

            if (action === 'increase') {
                quantity += 1;
            } else if (action === 'decrease' && quantity > 1) {
                quantity -= 1;
            }

            quantityInput.value = quantity;
            quantityDisplay.textContent = quantity;
            form.submit();
        });
    });