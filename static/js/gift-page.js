(function () {
    // This template renders one of three states — logged out, logged in with a gift
    // already in progress, or logged in with the form — so every element below is
    // looked up defensively; most only exist in the last state.

    // --- Custom product dropdown ---
    const trigger = document.getElementById('gift-product-trigger');
    const optionsEl = document.getElementById('gift-product-options');
    const hiddenInput = document.getElementById('gift-product-id');
    const triggerImg = document.getElementById('gift-trigger-img');
    const triggerLabel = document.getElementById('gift-trigger-label');

    if (trigger && optionsEl) {
        trigger.addEventListener('click', function () {
            optionsEl.classList.toggle('open');
            trigger.classList.toggle('open');
        });

        /**
         * Selects a gift product option: stores its value, updates the
         * trigger's label/image, and closes the dropdown.
         * @param {HTMLElement} opt - The gift product option being configured.
         */
        optionsEl.querySelectorAll('.gift-product-option').forEach(function (opt) {
            opt.addEventListener('click', function () {
                hiddenInput.value = this.dataset.value;
                triggerLabel.textContent = this.dataset.name;
                triggerLabel.classList.remove('gift-trigger-placeholder');
                trigger.style.borderColor = '';

                const img = this.dataset.image;
                if (img) {
                    triggerImg.src = img;
                    triggerImg.style.display = '';
                } else {
                    triggerImg.style.display = 'none';
                }

                optionsEl.querySelectorAll('.gift-product-option').forEach(function (option) { option.classList.remove('selected'); });
                this.classList.add('selected');
                optionsEl.classList.remove('open');
                trigger.classList.remove('open');
            });
        });

        /**
         * Closes the dropdown when the user clicks outside of it.
         * @param {MouseEvent} e - The click event on the document.
         */
        document.addEventListener('click', function (e) {
            if (!trigger.contains(e.target) && !optionsEl.contains(e.target)) {
                optionsEl.classList.remove('open');
                trigger.classList.remove('open');
            }
        });
    }

    // --- Form submit validation ---
    const form = document.querySelector('form[method="POST"]');
    if (form && hiddenInput) {
        /**
         * Blocks submission and highlights the product dropdown if no gift
         * product has been selected.
         * @param {SubmitEvent} e - The form submit event.
         */
        form.addEventListener('submit', function (e) {
            if (!hiddenInput.value) {
                e.preventDefault();
                trigger.style.borderColor = 'var(--danger)';
                trigger.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }

    // --- Existing contact toggle ---
    const contactSelect = document.getElementById('existing-contact-select');
    const newFields = document.getElementById('new-contact-fields');

    if (contactSelect && newFields) {
        /**
         * Shows the new-contact fields when no existing contact is
         * selected, hiding them (and dropping their "required" validation)
         * otherwise.
         */
        contactSelect.addEventListener('change', function () {
            if (this.value) {
                newFields.style.display = 'none';
                newFields.querySelectorAll('input').forEach(function (input) { input.removeAttribute('required'); });
            } else {
                newFields.style.display = '';
            }
        });
    }
})();
