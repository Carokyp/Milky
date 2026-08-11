(function () {
    // This template renders one of two states (logged in / not logged in), so every
    // element below is looked up defensively — most only exist in the logged-in form.

    // --- Custom product dropdown ---
    var trigger = document.getElementById('gift-product-trigger');
    var optionsEl = document.getElementById('gift-product-options');
    var hiddenInput = document.getElementById('gift-product-id');
    var triggerImg = document.getElementById('gift-trigger-img');
    var triggerLabel = document.getElementById('gift-trigger-label');

    if (trigger && optionsEl) {
        trigger.addEventListener('click', function () {
            optionsEl.classList.toggle('open');
            trigger.classList.toggle('open');
        });

        optionsEl.querySelectorAll('.gift-product-option').forEach(function (opt) {
            opt.addEventListener('click', function () {
                hiddenInput.value = this.dataset.value;
                triggerLabel.textContent = this.dataset.name;
                triggerLabel.classList.remove('gift-trigger-placeholder');
                trigger.style.borderColor = '';

                var img = this.dataset.image;
                if (img) {
                    triggerImg.src = img;
                    triggerImg.style.display = '';
                } else {
                    triggerImg.style.display = 'none';
                }

                optionsEl.querySelectorAll('.gift-product-option').forEach(function (o) { o.classList.remove('selected'); });
                this.classList.add('selected');
                optionsEl.classList.remove('open');
                trigger.classList.remove('open');
            });
        });

        document.addEventListener('click', function (e) {
            if (!trigger.contains(e.target) && !optionsEl.contains(e.target)) {
                optionsEl.classList.remove('open');
                trigger.classList.remove('open');
            }
        });
    }

    // --- Form submit validation ---
    var form = document.querySelector('form[method="POST"]');
    if (form && hiddenInput) {
        form.addEventListener('submit', function (e) {
            if (!hiddenInput.value) {
                e.preventDefault();
                trigger.style.borderColor = 'var(--danger)';
                trigger.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }

    // --- Existing contact toggle ---
    var contactSelect = document.getElementById('existing-contact-select');
    var newFields = document.getElementById('new-contact-fields');

    if (contactSelect && newFields) {
        contactSelect.addEventListener('change', function () {
            if (this.value) {
                newFields.style.display = 'none';
                newFields.querySelectorAll('input').forEach(function (i) { i.removeAttribute('required'); });
            } else {
                newFields.style.display = '';
            }
        });
    }
})();
