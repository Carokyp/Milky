const stars = document.querySelectorAll('.star-btn');
const ratingInput = document.getElementById('rating-input');

function highlightStars(value) {
    stars.forEach((s, index) => {
        s.classList.toggle('fa-solid', index < value);
        s.classList.toggle('fa-regular', index >= value);
    });
}

highlightStars(parseInt(ratingInput.value));

stars.forEach(star => {
    star.addEventListener('click', function () {
        ratingInput.value = this.dataset.value;
        highlightStars(parseInt(this.dataset.value));
    });

    star.addEventListener('mouseover', function () {
        highlightStars(parseInt(this.dataset.value));
    });

    star.addEventListener('mouseout', function () {
        highlightStars(parseInt(ratingInput.value));
    });
});