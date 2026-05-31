// Get Stripe keys from Django template
const stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);
const checkoutUrl = document.getElementById('payment-form').dataset.checkoutUrl;

// Toggle the invoice fields visibility when the "same-as-delivery" 
// checkbox changes — hide them when checked, show them when unchecked.

document.getElementById('same-as-delivery').addEventListener('change', function () {
    const invoiceFields = document.getElementById('invoice-fields');
    invoiceFields.style.display = this.checked ? 'none' : 'block';
});

// Stripe payment handling
const stripe = Stripe(stripePublicKey);
let elements;

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
}

async function handleSubmit(e) {
    e.preventDefault();

    document.querySelector("#submit-button").disabled = true;
    document.querySelector("#submit-button").textContent = "Processing...";

    // 1. First, save the data to the session.
    const form = document.querySelector("#payment-form");
    const formData = new FormData(form);

    const saveResponse = await fetch(checkoutUrl, {
        method: "POST",
        headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
        body: formData,
    });
    const data = await saveResponse.json();
    if (data.status !== 'ok') {
        document.querySelector("#card-errors").textContent = "Error saving order data.";
        document.querySelector("#submit-button").disabled = false;
        document.querySelector("#submit-button").textContent = "Complete Order";
        return;
    }

    // 2. Then, Stripe confirms and redirects
    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: window.location.origin + "/checkout/success/",
        },
    });

    if (error) {
        if (error.type === "card_error" || error.type === "validation_error") {
            document.querySelector("#card-errors").textContent = error.message;
        } else {
            document.querySelector("#card-errors").textContent = "An unexpected error occurred.";
        }
        document.querySelector("#submit-button").disabled = false;
        document.querySelector("#submit-button").textContent = "Complete Order";
    }
}