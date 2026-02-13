document.addEventListener('DOMContentLoaded', function () {
    // Render all blocks immediately without entrance transitions.
    document.querySelectorAll('.anim-hidden').forEach(function (el) {
        el.classList.add('anim-visible');
        el.classList.remove('anim-hidden');
    });
});
