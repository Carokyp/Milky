document.addEventListener('DOMContentLoaded', function() {
    var checkbox = document.createElement('div');
    checkbox.id = 'same-as-delivery-admin-wrapper';
    checkbox.style.margin = '1rem 0.5rem 1rem';
    checkbox.innerHTML =
        '<label for="same-as-delivery-admin" style="white-space:nowrap;">' +
        '<input type="checkbox" id="same-as-delivery-admin" style="margin-right:6px;">' +
        '<span>Same as delivery address</span>' +
        '</label>';

    var invoiceName = document.getElementById('id_invoice_name');
    var target = invoiceName && invoiceName.closest('.form-row, .form-group, .field-box, .fieldBox');

    if (target) {
        target.parentNode.insertBefore(checkbox, target);
    } else if (invoiceName) {
        var fieldset = invoiceName.closest('fieldset');
        if (fieldset) {
            fieldset.insertBefore(checkbox, fieldset.firstChild);
        } else {
            document.body.prepend(checkbox);
        }
    } else {
        document.body.prepend(checkbox);
    }

    var sameAsDelivery = document.getElementById('same-as-delivery-admin');
    if (!sameAsDelivery) {
        return;
    }

    sameAsDelivery.addEventListener('change', function() {

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
        if (this.checked) {
            // On check: save original invoice values once, then copy delivery values.
            map.forEach(function(pair) {
                var invoiceField = document.getElementById('id_' + pair[0]);
                var deliveryField = document.getElementById('id_' + pair[1]);

                if (!invoiceField || !deliveryField) {
                    return;
                }

                if (typeof invoiceField.dataset.savedOrig === 'undefined') {
                    invoiceField.dataset.savedOrig = invoiceField.value || '';
                }

                invoiceField.value = deliveryField.value || '';
                invoiceField.dispatchEvent(new Event('change', { bubbles: true }));
            });
        } else {
            // On uncheck: clear invoice fields (but keep saved original values).
            map.forEach(function(pair) {
                var invoiceField = document.getElementById('id_' + pair[0]);
                if (!invoiceField) {
                    return;
                }

                invoiceField.value = '';
                invoiceField.dispatchEvent(new Event('change', { bubbles: true }));
            });
        }
    });
});