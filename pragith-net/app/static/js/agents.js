// Agents page scroll animations using IntersectionObserver
document.addEventListener('DOMContentLoaded', function () {
    // Guard for older browsers
    if (!('IntersectionObserver' in window)) {
        // Fallback: just show all elements
        document.querySelectorAll('.anim-hidden').forEach(function (el) {
            el.classList.add('anim-visible');
            el.classList.remove('anim-hidden');
        });
        return;
    }

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('anim-visible');
                entry.target.classList.remove('anim-hidden');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });

    document.querySelectorAll('.anim-hidden').forEach(function (el) {
        observer.observe(el);
    });
});
