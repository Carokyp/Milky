/* jshint esversion: 6 */

const stars = document.querySelectorAll('.star-btn');
const ratingInput = document.getElementById('rating-input');

/**
 * Updates each star icon to reflect the given rating: solid for stars at or
 * below the rating, outlined for the rest.
 * @param {number} value - The rating to highlight, from 1 to the star count.
 */
function highlightStars(value) {
    stars.forEach((star, index) => {
        star.classList.toggle('fa-solid', index < value);
        star.classList.toggle('fa-regular', index >= value);
    });
}

highlightStars(parseInt(ratingInput.value));

/**
 * Wires up each star to set the rating on click and preview the rating on
 * hover, reverting to the saved rating when the mouse leaves.
 * @param {HTMLElement} star - The star icon being configured.
 */
stars.forEach(star => {
    star.addEventListener('click', function() {
        ratingInput.value = this.dataset.value;
        highlightStars(parseInt(this.dataset.value));
    });

    star.addEventListener('mouseover', function() {
        highlightStars(parseInt(this.dataset.value));
    });

    star.addEventListener('mouseout', function() {
        highlightStars(parseInt(ratingInput.value));
    });
});