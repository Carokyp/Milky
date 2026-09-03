/* jshint esversion: 6 */

/**
 * Adds a "same as delivery address" checkbox to the admin order's invoice
 * fields, copying delivery values into the invoice fields when checked and
 * auto-checking itself if the invoice fields already match on load.
 */
document.addEventListener('DOMContentLoaded', function() {

    // Create the checkbox wrapper
    const checkbox = document.createElement('div');
    checkbox.id = 'same-as-delivery-admin-wrapper';
    checkbox.style.margin = '1rem 0.5rem 1rem';
    checkbox.innerHTML =
        '<label for="same-as-delivery-admin" style="white-space:nowrap;">' +
        '<input type="checkbox" id="same-as-delivery-admin" style="margin-right:6px;">' +
        '<span>Same as delivery address</span>' +
        '</label>';

    // Insert checkbox before the first invoice field
    const invoiceName = document.getElementById('id_invoice_name');
    const invoiceRow = invoiceName && invoiceName.closest('.form-row');
    if (invoiceRow) {
        invoiceRow.parentNode.insertBefore(checkbox, invoiceRow);
    }

    const fieldPairs = [
        ['invoice_name', 'delivery_name'],
        ['invoice_surname', 'delivery_surname'],
        ['invoice_phone', 'delivery_phone'],
        ['invoice_address', 'delivery_address'],
        ['invoice_city', 'delivery_city'],
        ['invoice_county', 'delivery_county'],
        ['invoice_postcode', 'delivery_postcode'],
        ['invoice_country', 'delivery_country']
    ];

    /**
     * Looks up an invoice/delivery field pair by their model field names.
     * @param {string} invoiceKey - The invoice field's model name, e.g. "invoice_name".
     * @param {string} deliveryKey - The matching delivery field's model name, e.g. "delivery_name".
     * @returns {HTMLElement[]} A [invoiceField, deliveryField] pair; either may be null.
     */
    function getFieldPair(invoiceKey, deliveryKey) {
        return [
            document.getElementById('id_' + invoiceKey),
            document.getElementById('id_' + deliveryKey),
        ];
    }

    // Copy delivery values to invoice fields when checked
    const sameAsDelivery = document.getElementById('same-as-delivery-admin');
    if (!sameAsDelivery) return;

    sameAsDelivery.addEventListener('change', function() {
        fieldPairs.forEach(([invoiceKey, deliveryKey]) => {
            const [invoiceField, deliveryField] = getFieldPair(invoiceKey, deliveryKey);
            if (!invoiceField || !deliveryField) return;

            invoiceField.value = this.checked ? deliveryField.value : '';
            invoiceField.dispatchEvent(new Event('change', {
                bubbles: true
            }));
        });
    });

    // Auto-check after admin JS has fully initialised
    setTimeout(function() {
        const allMatch = fieldPairs.every(([invoiceKey, deliveryKey]) => {
            const [invoiceField, deliveryField] = getFieldPair(invoiceKey, deliveryKey);
            if (!invoiceField || !deliveryField) return true;
            return invoiceField.value.trim() === deliveryField.value.trim();
        });

        if (allMatch) {
            sameAsDelivery.checked = true;
        }
    }, 300);
});