/**
 * Toggles a contact between its read-only view and its edit form.
 * @param {string} contactId - The id of the contact being toggled.
 */
function toggleEditContact(contactId) {
    const view = document.getElementById(`contact-view-${contactId}`);
    const edit = document.getElementById(`contact-edit-${contactId}`);

    if (!view || !edit) return;

    const isHidden = edit.style.display === 'none' || edit.style.display === '';
    edit.style.display = isHidden ? 'block' : 'none';
    view.style.display = isHidden ? 'none' : 'flex';
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.contact-edit-btn, .contact-cancel-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            toggleEditContact(this.dataset.contactId);
        });
    });

    const deleteModalEl = document.getElementById('deleteContactModal');
    const deleteModal = new bootstrap.Modal(deleteModalEl);
    const confirmBtn = document.getElementById('deleteContactConfirmBtn');
    const modalText = document.getElementById('deleteContactModalText');
    let lastTrigger = null;

    document.querySelectorAll('.contact-delete-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            lastTrigger = this;
            confirmBtn.href = this.dataset.deleteUrl;
            modalText.innerHTML = 'Are you sure you want to delete <strong>' + this.dataset.contactName + '</strong>?';
            deleteModal.show();
        });
    });

    // Restore focus to whichever delete button opened the modal.
    deleteModalEl.addEventListener('hidden.bs.modal', function() {
        if (lastTrigger) lastTrigger.focus();
    });
});