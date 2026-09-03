/* jshint esversion: 6 */
/* global bootstrap */

/**
 * Auto-shows every Bootstrap toast on the page once the DOM is ready,
 * auto-hiding each one after a short delay.
 */
document.addEventListener('DOMContentLoaded', function() {
    const toasts = document.querySelectorAll('.toast');
    const delay = 6000;

    toasts.forEach((toast) => {
        bootstrap.Toast.getOrCreateInstance(toast, {
            delay
        }).show();
    });
});