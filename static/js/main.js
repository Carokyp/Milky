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

document.querySelectorAll('input[data-filename-target]').forEach(function(input) {
    input.addEventListener('change', function() {
        var file = this.files[0];
        var target = document.getElementById(this.dataset.filenameTarget);
        if (target) target.textContent = file ? file.name : '';
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
