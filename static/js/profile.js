function toggleEditContact(contactId) {
  const view = document.getElementById(`contact-view-${contactId}`);
  const edit = document.getElementById(`contact-edit-${contactId}`);

  if (!view || !edit) return;

  const isHidden = edit.style.display === "none" || edit.style.display === "";
  edit.style.display = isHidden ? "block" : "none";
  view.style.display = isHidden ? "none" : "flex";
}
