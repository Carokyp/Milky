function closeNavbar() {
    var nav = bootstrap.Collapse.getInstance(document.getElementById('navbarNav'));
    if (nav) nav.hide();
}

// Close navbar when account dropdown opens
document.querySelector('.dropdown').addEventListener('show.bs.dropdown', closeNavbar);

// Close navbar when clicking outside of it
document.addEventListener('click', function (e) {
    if (!e.target.closest('header')) closeNavbar();
});

document.querySelectorAll('.delete-product-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        document.getElementById('deleteProductModalText').innerHTML =
            'Are you sure you want to delete <strong>' + this.dataset.productName + '</strong>? This cannot be undone.';
        document.getElementById('deleteProductConfirmBtn').href = this.href;
        new bootstrap.Modal(document.getElementById('deleteProductModal')).show();
    });
});

document.querySelectorAll('.trigger-file-input').forEach(function(btn) {
    btn.addEventListener('click', function() {
        var input = document.getElementById(this.dataset.target);
        if (input) input.click();
    });
});

document.querySelectorAll('input[data-filename-target]').forEach(function(input) {
    input.addEventListener('change', function() {
        var file = this.files[0];
        var target = document.getElementById(this.dataset.filenameTarget);
        if (target) target.textContent = file ? file.name : '';

        var selectTrigger = this.dataset.selectTrigger ? document.getElementById(this.dataset.selectTrigger) : null;
        var blankTrigger = this.dataset.blankTrigger ? document.getElementById(this.dataset.blankTrigger) : null;
        var realClearCheckbox = this.dataset.realClearCheckbox ? document.getElementById(this.dataset.realClearCheckbox) : null;

        var previewImg = document.getElementById(this.dataset.previewTarget);
        var previewWrap = previewImg ? previewImg.closest('[id^="preview-wrap-"]') : null;
        if (previewImg && previewWrap) {
            if (file) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    previewWrap.classList.remove('d-none');
                    if (selectTrigger) selectTrigger.classList.add('d-none');
                    if (blankTrigger) blankTrigger.classList.add('d-none');
                };
                reader.readAsDataURL(file);
                var removeCheckbox = document.getElementById('remove-preview-' + this.id);
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

document.querySelectorAll('.remove-preview-checkbox').forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        if (!this.checked) return;
        var input = document.getElementById(this.dataset.clearTarget);
        if (!input) return;
        input.value = '';
        input.dispatchEvent(new Event('change'));
    });
});

document.querySelectorAll('.real-clear-checkbox').forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        var selectTrigger = this.dataset.selectTrigger ? document.getElementById(this.dataset.selectTrigger) : null;
        var blankTrigger = this.dataset.blankTrigger ? document.getElementById(this.dataset.blankTrigger) : null;
        if (this.checked) {
            if (selectTrigger) selectTrigger.classList.add('d-none');
            if (blankTrigger) blankTrigger.classList.remove('d-none');
        } else {
            if (blankTrigger) blankTrigger.classList.add('d-none');
            if (selectTrigger) selectTrigger.classList.remove('d-none');
        }
    });
});

document.querySelectorAll('.product-card').forEach(card => {
    const objects = card.querySelector('.product-card-objects');
    const can = card.querySelector('.product-card-can');

    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        objects.style.transform = `translate(${x * 25}px, ${y * 25}px)`;
        can.style.transform = `translate(${x * 10}px, ${y * 10}px)`;
    });

    card.addEventListener('mouseleave', () => {
        objects.style.transform = 'translate(0, 0)';
        can.style.transform = 'translate(0, 0)';
    });
});
