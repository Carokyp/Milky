/**
 * Styles a country <select> like a placeholder until a real value is
 * chosen: gray text while empty, black text once a country is selected.
 * @param {string} fieldId - The id of the country select element.
 */
function handleCountryField(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return;

    field.style.color = field.value ? 'black' : '#adb5bd';

    field.addEventListener('change', function() {
        this.style.color = this.value ? 'black' : '#adb5bd';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    handleCountryField('id_country');
});