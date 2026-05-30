document.getElementById('same-as-delivery').addEventListener('change', function() {
    const invoiceFields = document.getElementById('invoice-fields');
    invoiceFields.style.display = this.checked ? 'none' : 'block';
});

