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
