document.addEventListener('DOMContentLoaded', function() {

    // Create the checkbox wrapper
    var checkbox = document.createElement('div');
    checkbox.id = 'same-as-delivery-admin-wrapper';
    checkbox.style.margin = '1rem 0.5rem 1rem';
    checkbox.innerHTML =
        '<label for="same-as-delivery-admin" style="white-space:nowrap;">' +
        '<input type="checkbox" id="same-as-delivery-admin" style="margin-right:6px;">' +
        '<span>Same as delivery address</span>' +
        '</label>';

    // Insert checkbox before the first invoice field
    var invoiceName = document.getElementById('id_invoice_name');
    var target = invoiceName && invoiceName.closest('.form-row');
    if (target) {
        target.parentNode.insertBefore(checkbox, target);
    }

    var map = [
        ['invoice_name', 'delivery_name'],
        ['invoice_surname', 'delivery_surname'],
        ['invoice_phone', 'delivery_phone'],
        ['invoice_address', 'delivery_address'],
        ['invoice_city', 'delivery_city'],
        ['invoice_county', 'delivery_county'],
        ['invoice_postcode', 'delivery_postcode'],
        ['invoice_country', 'delivery_country']
    ];

    // Copy delivery values to invoice fields when checked
    var sameAsDelivery = document.getElementById('same-as-delivery-admin');
    if (!sameAsDelivery) return;

    sameAsDelivery.addEventListener('change', function() {
        map.forEach(function(pair) {
            var invoiceField = document.getElementById('id_' + pair[0]);
            var deliveryField = document.getElementById('id_' + pair[1]);
            if (!invoiceField || !deliveryField) return;

            invoiceField.value = this.checked ? deliveryField.value : '';
            invoiceField.dispatchEvent(new Event('change', { bubbles: true }));
        }.bind(this));
    });

    // Auto-check after admin JS has fully initialised
    setTimeout(function() {
        var allMatch = map.every(function(pair) {
            var invoiceField = document.getElementById('id_' + pair[0]);
            var deliveryField = document.getElementById('id_' + pair[1]);
            if (!invoiceField || !deliveryField) return true;
            return invoiceField.value.trim() === deliveryField.value.trim();
        });

        if (allMatch) {
            sameAsDelivery.checked = true;
        }
    }, 300);
});