document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card[data-href]');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            window.location.href = this.getAttribute('data-href');
        });
    });
});