// Disable automatic scroll restoration to prevent the page from jumping to the previous scroll position on reload.
if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}
window.scrollTo(0, 0);

// Toggle the invoice fields visibility when the "same-as-delivery"
// checkbox changes — hide them when checked, show them when unchecked.
document.getElementById('same-as-delivery').addEventListener('change', function () {
    const invoiceFields = document.getElementById('invoice-fields');
    invoiceFields.style.display = this.checked ? 'none' : 'block';
});

// Stripe payment handling

// Get Stripe keys and URLs from Django template
const stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);
const paymentForm = document.getElementById('payment-form');
const checkoutUrl = paymentForm.dataset.checkoutUrl;
const cacheUrl = paymentForm.dataset.cacheUrl;

const stripe = Stripe(stripePublicKey);
const submitButton = document.querySelector('#submit-button');
const paymentStatus = document.querySelector('#payment-status');
let elements;

// Disable button until Stripe is ready
submitButton.disabled = true;

paymentForm.addEventListener('submit', handleSubmit);

// Initialize Stripe only when the payment section enters the viewport
const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        observer.disconnect();
        initialize();
    }
}, { threshold: 0.1 });
observer.observe(document.getElementById('payment-element'));

/**
 * Creates and mounts the Stripe Payment Element, enabling the submit
 * button once it is ready for input.
 */
async function initialize() {
    elements = stripe.elements({ clientSecret });

    const paymentElement = elements.create('payment');
    paymentElement.mount('#payment-element');

    paymentElement.on('ready', function () {
        submitButton.disabled = false;
        paymentStatus.style.display = 'none';
    });
}

/**
 * Re-enables the submit button and restores its label after a failed
 * checkout attempt.
 */
function resetSubmitButton() {
    submitButton.disabled = false;
    submitButton.querySelector('span').textContent = 'Complete Order';
}

/**
 * Handles checkout form submission: saves the order data, caches it
 * against the Stripe PaymentIntent, then confirms payment with Stripe.
 * @param {SubmitEvent} e - The form submit event.
 */
async function handleSubmit(e) {
    e.preventDefault();

    const cardErrorsEl = document.querySelector('#card-errors');

    // Disable button and show processing state
    submitButton.disabled = true;
    submitButton.querySelector('span').textContent = 'Processing...';

    try {
        const formData = new FormData(paymentForm);

        // 1. Save form data to session
        const saveResponse = await fetch(checkoutUrl, {
            method: 'POST',
            headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
            body: formData,
        });
        const data = await saveResponse.json();
        if (data.status !== 'ok') {
            cardErrorsEl.textContent = 'Error saving order data.';
            resetSubmitButton();
            return;
        }

        // 2. Cache checkout data in PaymentIntent metadata
        const cacheData = new FormData();
        cacheData.append('client_secret', clientSecret);
        cacheData.append('csrfmiddlewaretoken', formData.get('csrfmiddlewaretoken'));

        const cacheResponse = await fetch(cacheUrl, {
            method: 'POST',
            headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
            body: cacheData,
        });
        if (!cacheResponse.ok) {
            cardErrorsEl.textContent = 'Error processing payment data.';
            resetSubmitButton();
            return;
        }

        // 3. Stripe confirms and redirects
        const { error } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: window.location.origin + '/checkout/success/',
                shipping: {
                    name: document.querySelector('[name="delivery_name"]').value + ' ' + document.querySelector('[name="delivery_surname"]').value,
                    phone: document.querySelector('[name="delivery_phone"]').value,
                    address: {
                        line1: document.querySelector('[name="delivery_address"]').value,
                        city: document.querySelector('[name="delivery_city"]').value,
                        postal_code: document.querySelector('[name="delivery_postcode"]').value,
                        country: document.querySelector('[name="delivery_country"]').value,
                    }
                },
            },
        });

        if (error) {
            if (error.type === 'card_error') {
                cardErrorsEl.textContent = error.message;
            } else if (error.type === 'validation_error') {
                cardErrorsEl.textContent = '';
            } else {
                cardErrorsEl.textContent = 'An unexpected error occurred.';
            }
            resetSubmitButton();
        }
    } catch (err) {
        console.error('Checkout submission failed', err);
        cardErrorsEl.textContent = 'A network error occurred. Please check your connection and try again.';
        resetSubmitButton();
    }
}
