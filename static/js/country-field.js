function handleCountryField(fieldId) {
    var field = document.getElementById(fieldId);
    if (!field) return;
    
    field.style.color = field.value ? 'black' : '#adb5bd';
    
    field.addEventListener('change', function() {
        this.style.color = this.value ? 'black' : '#adb5bd';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    handleCountryField('id_country');
});