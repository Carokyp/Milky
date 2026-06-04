// Get Stripe keys and URLs from Django template
const stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);
const checkoutUrl = document.getElementById('payment-form').dataset.checkoutUrl;
const cacheUrl = document.getElementById('payment-form').dataset.cacheUrl;

// Toggle the invoice fields visibility when the "same-as-delivery" 
// checkbox changes — hide them when checked, show them when unchecked.
document.getElementById('same-as-delivery').addEventListener('change', function () {
    const invoiceFields = document.getElementById('invoice-fields');
    invoiceFields.style.display = this.checked ? 'none' : 'block';
});

// Stripe payment handling
const stripe = Stripe(stripePublicKey);
const submitButton = document.querySelector("#submit-button");
const paymentStatus = document.querySelector("#payment-status");
let elements;

// Disable button until Stripe is ready
submitButton.disabled = true;

initialize();
document.querySelector("#payment-form").addEventListener("submit", handleSubmit);

async function initialize() {
    const appearance = {
        theme: 'stripe',
        variables: {
            colorBackground: '#ffffff',
            colorPrimary: '#523122',
        }
    };
    elements = stripe.elements({ appearance, clientSecret });

    const paymentElement = elements.create("payment");
    paymentElement.mount("#payment-element");

    // Enable button when Stripe is ready
    paymentElement.on('ready', function () {
        submitButton.disabled = false;
        paymentStatus.style.display = "none";
    });
}

async function handleSubmit(e) {
    e.preventDefault();

    // Disable button and show processing state
    submitButton.disabled = true;
    submitButton.querySelector('span').textContent = "Processing...";

    const form = document.querySelector("#payment-form");
    const formData = new FormData(form);

    // 1. Save form data to session
    const saveResponse = await fetch(checkoutUrl, {
        method: "POST",
        headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
        body: formData,
    });
    const data = await saveResponse.json();
    if (data.status !== 'ok') {
        document.querySelector("#card-errors").textContent = "Error saving order data.";
        submitButton.disabled = false;
        submitButton.querySelector('span').textContent = "Complete Order";
        return;
    }

    // 2. Cache checkout data in PaymentIntent metadata
    const cacheData = new FormData();
    cacheData.append('client_secret', clientSecret);
    cacheData.append('csrfmiddlewaretoken', formData.get("csrfmiddlewaretoken"));

    const cacheResponse = await fetch(cacheUrl, {
        method: "POST",
        headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
        body: cacheData,
    });
    if (!cacheResponse.ok) {
        document.querySelector("#card-errors").textContent = "Error processing payment data.";
        submitButton.disabled = false;
        submitButton.querySelector('span').textContent = "Complete Order";
        return;
    }

    // 3. Stripe confirms and redirects
    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: window.location.origin + "/checkout/success/",
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
        if (error.type === "card_error") {
            document.querySelector("#card-errors").textContent = error.message;
        } else if (error.type === "validation_error") {
            document.querySelector("#card-errors").textContent = "";
        } else {
            document.querySelector("#card-errors").textContent = "An unexpected error occurred.";
        }
        submitButton.disabled = false;
        submitButton.querySelector('span').textContent = "Complete Order";
    }
}