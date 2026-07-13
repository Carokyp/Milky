function toggleEditContact(contactId) {
  const view = document.getElementById(`contact-view-${contactId}`);
  const edit = document.getElementById(`contact-edit-${contactId}`);

  if (!view || !edit) return;

  const isHidden = edit.style.display === "none" || edit.style.display === "";
  edit.style.display = isHidden ? "block" : "none";
  view.style.display = isHidden ? "none" : "flex";
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".contact-edit-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      toggleEditContact(this.dataset.contactId);
    });
  });

  document.querySelectorAll(".contact-cancel-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      toggleEditContact(this.dataset.contactId);
    });
  });

  var deleteModalEl = document.getElementById("deleteContactModal");
  var deleteModal = new bootstrap.Modal(deleteModalEl);
  var confirmBtn = document.getElementById("deleteContactConfirmBtn");
  var modalText = document.getElementById("deleteContactModalText");
  var lastTrigger = null;

  document.querySelectorAll(".contact-delete-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      lastTrigger = this;
      confirmBtn.href = this.dataset.deleteUrl;
      modalText.innerHTML = "Are you sure you want to delete <strong>" + this.dataset.contactName + "</strong>?";
      deleteModal.show();
    });
  });

  deleteModalEl.addEventListener("hide.bs.modal", function () {
    if (document.activeElement) document.activeElement.blur();
  });

  deleteModalEl.addEventListener("hidden.bs.modal", function () {
    if (lastTrigger) lastTrigger.focus();
  });
});
