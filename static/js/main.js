/**
 * Closes the responsive navbar collapse if it is currently expanded.
 */
function closeNavbar() {
    const nav = bootstrap.Collapse.getInstance(document.getElementById('navbarNav'));
    if (nav) nav.hide();
}

// Close the navbar when the account dropdown opens.
document.querySelector('.dropdown').addEventListener('show.bs.dropdown', closeNavbar);

/**
 * Closes the navbar when the user clicks anywhere outside the header.
 * @param {MouseEvent} e - The click event fired on the document.
 */
document.addEventListener('click', function (e) {
    if (!e.target.closest('header')) closeNavbar();
});

/**
 * Wires up each "delete product" button to populate and open the
 * delete-confirmation modal with the target product's name and link.
 * @param {HTMLElement} btn - The delete-product button being configured.
 */
document.querySelectorAll('.delete-product-btn').forEach(function (btn) {
    /**
     * Populates the delete-confirmation modal and shows it.
     * @param {MouseEvent} e - The click event on the delete button.
     */
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('deleteProductModalText').innerHTML =
            'Are you sure you want to delete <strong>' + this.dataset.productName + '</strong>? This cannot be undone.';
        document.getElementById('deleteProductConfirmBtn').href = this.href;
        new bootstrap.Modal(document.getElementById('deleteProductModal')).show();
    });
});

/**
 * Wires up each trigger element to open its associated hidden file input.
 * @param {HTMLElement} btn - The trigger element being configured.
 */
document.querySelectorAll('.trigger-file-input').forEach(function (btn) {
    btn.addEventListener('click', function () {
        const input = document.getElementById(this.dataset.target);
        if (input) input.click();
    });
});

/**
 * Wires up each file input to display the selected filename and, where
 * configured, preview the selected image and toggle the related trigger
 * buttons.
 * @param {HTMLInputElement} input - The file input being configured.
 */
document.querySelectorAll('input[data-filename-target]').forEach(function (input) {
    input.addEventListener('change', function () {
        const file = this.files[0];
        const target = document.getElementById(this.dataset.filenameTarget);
        if (target) target.textContent = file ? file.name : '';

        const selectTrigger = this.dataset.selectTrigger ? document.getElementById(this.dataset.selectTrigger) : null;
        const blankTrigger = this.dataset.blankTrigger ? document.getElementById(this.dataset.blankTrigger) : null;
        const realClearCheckbox = this.dataset.realClearCheckbox ? document.getElementById(this.dataset.realClearCheckbox) : null;

        const previewImg = document.getElementById(this.dataset.previewTarget);
        const previewWrap = previewImg ? previewImg.closest('[id^="preview-wrap-"]') : null;
        if (previewImg && previewWrap) {
            if (file) {
                const reader = new FileReader();
                /**
                 * Renders the selected file as an image preview.
                 * @param {ProgressEvent<FileReader>} e - The FileReader load event.
                 */
                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                    previewWrap.classList.remove('d-none');
                    if (selectTrigger) selectTrigger.classList.add('d-none');
                    if (blankTrigger) blankTrigger.classList.add('d-none');
                };
                reader.readAsDataURL(file);
                const removeCheckbox = document.getElementById('remove-preview-' + this.id);
                if (removeCheckbox) removeCheckbox.checked = false;
                if (realClearCheckbox) realClearCheckbox.checked = false;
            } else {
                previewImg.src = '';
                previewWrap.classList.add('d-none');
                if (realClearCheckbox && realClearCheckbox.checked) {
                    if (blankTrigger) blankTrigger.classList.remove('d-none');
                } else if (selectTrigger) {
                    selectTrigger.classList.remove('d-none');
                }
            }
        }
    });
});

/**
 * Wires up each "remove preview" checkbox to clear its associated file
 * input when checked.
 * @param {HTMLInputElement} checkbox - The remove-preview checkbox being configured.
 */
document.querySelectorAll('.remove-preview-checkbox').forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
        if (!this.checked) return;
        const input = document.getElementById(this.dataset.clearTarget);
        if (!input) return;
        input.value = '';
        input.dispatchEvent(new Event('change'));
    });
});

/**
 * Wires up each "clear image" checkbox to toggle between the "select image"
 * and "blank image" trigger buttons.
 * @param {HTMLInputElement} checkbox - The real-clear checkbox being configured.
 */
document.querySelectorAll('.real-clear-checkbox').forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
        const selectTrigger = this.dataset.selectTrigger ? document.getElementById(this.dataset.selectTrigger) : null;
        const blankTrigger = this.dataset.blankTrigger ? document.getElementById(this.dataset.blankTrigger) : null;
        if (this.checked) {
            if (selectTrigger) selectTrigger.classList.add('d-none');
            if (blankTrigger) blankTrigger.classList.remove('d-none');
        } else {
            if (blankTrigger) blankTrigger.classList.add('d-none');
            if (selectTrigger) selectTrigger.classList.remove('d-none');
        }
    });
});

/**
 * Adds a mouse-tracking parallax effect to each product card, shifting its
 * object and can layers based on cursor position.
 * @param {HTMLElement} card - The product card being configured.
 */
document.querySelectorAll('.product-card').forEach(card => {
    const objects = card.querySelector('.product-card-objects');
    const can = card.querySelector('.product-card-can');

    /**
     * Shifts the card's layers to follow the cursor.
     * @param {MouseEvent} e - The mousemove event on the card.
     */
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        // The overlay layers are optional, so a card may have only a background.
        if (objects) objects.style.transform = `translate(${x * 25}px, ${y * 25}px)`;
        if (can) can.style.transform = `translate(${x * 10}px, ${y * 10}px)`;
    });

    /**
     * Resets the card's layers to their original position.
     */
    card.addEventListener('mouseleave', () => {
        if (objects) objects.style.transform = 'translate(0, 0)';
        if (can) can.style.transform = 'translate(0, 0)';
    });
});
