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

function updateGiftFriendDetailsState() {
    const contactSelect = document.getElementById('existing_contact');
    const detailFieldIds = ['id_name', 'id_surname', 'id_email', 'id_phone_number'];

    if (!contactSelect) return;

    const selectedOption = contactSelect.selectedOptions[0];
    const hasSelectedContact = Boolean(contactSelect.value);

    detailFieldIds.forEach((fieldId) => {
        const field = document.getElementById(fieldId);
        if (!field) return;

        field.disabled = hasSelectedContact;
        field.classList.toggle('bg-light', hasSelectedContact);
        field.classList.toggle('text-muted', hasSelectedContact);

        if (!hasSelectedContact) {
            field.value = '';
        }
    });

    if (!selectedOption || !hasSelectedContact) {
        return;
    }

    const fieldMappings = {
        id_name: selectedOption.dataset.name || '',
        id_surname: selectedOption.dataset.surname || '',
        id_email: selectedOption.dataset.email || '',
        id_phone_number: selectedOption.dataset.phone || '',
    };

    Object.entries(fieldMappings).forEach(([fieldId, value]) => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = value;
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    updateGiftFriendDetailsState();

    const contactSelect = document.getElementById('existing_contact');
    if (contactSelect) {
        contactSelect.addEventListener('change', updateGiftFriendDetailsState);
    }
});

// Reviews pagination without a full page reload — swaps only the reviews
// list/pagination markup so the rest of the page never moves. Listener is
// on the stable container (not the links themselves) so it still works
// after the links get replaced by each fetch.
const reviewsList = document.getElementById('reviews-list');
if (reviewsList) {
    reviewsList.addEventListener('click', function(event) {
        const link = event.target.closest('.review-nav-btn:not(.disabled)');
        if (!link) return;

        event.preventDefault();

        fetch(link.href, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            credentials: 'same-origin',
        })
            .then(response => response.json())
            .then(data => { reviewsList.innerHTML = data.html; })
            .catch(err => console.error('Failed to load reviews page', err));
    });
}

