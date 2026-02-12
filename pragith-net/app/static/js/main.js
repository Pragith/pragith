// Mobile menu toggle
function toggleMobileMenu() {
    document.getElementById('mobile-menu').classList.toggle('hidden');
}

// Theme toggle
function toggleTheme() {
    var d = document.documentElement.classList;
    if (d.contains('dark')) {
        d.remove('dark');
        localStorage.theme = 'light';
    } else {
        d.add('dark');
        localStorage.theme = 'dark';
    }
}

// Dropdown toggle functionality with ARIA support
function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    const button = document.querySelector(`button[onclick*="${id}"]`);
    const allDropdowns = document.querySelectorAll('[id$="-dropdown"]');
    const allButtons = document.querySelectorAll('button[aria-controls]');

    // Close all other dropdowns
    allDropdowns.forEach(d => {
        if (d.id !== id) {
            d.classList.add('hidden');
        }
    });

    // Update all other buttons' aria-expanded
    allButtons.forEach(btn => {
        if (btn.getAttribute('aria-controls') !== id) {
            btn.setAttribute('aria-expanded', 'false');
        }
    });

    // Toggle current dropdown
    const isHidden = dropdown.classList.toggle('hidden');

    // Update aria-expanded for current button
    if (button) {
        button.setAttribute('aria-expanded', !isHidden);
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', function (event) {
    const dropdowns = document.querySelectorAll('[id$="-dropdown"]');
    const buttons = document.querySelectorAll('button[aria-controls]');
    const isDropdownButton = event.target.closest('button[onclick*="toggleDropdown"]');

    if (!isDropdownButton) {
        dropdowns.forEach(d => d.classList.add('hidden'));
        buttons.forEach(btn => btn.setAttribute('aria-expanded', 'false'));
    }
});

// Intersection Observer for animations (if needed)
if ('IntersectionObserver' in window) {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with data-animate attribute
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('[data-animate]').forEach(el => {
            observer.observe(el);
        });
    });
}

// GA Consent Management (basic implementation)
window.gaConsent = {
    granted: false,

    grant: function () {
        this.granted = true;
        localStorage.setItem('ga_consent', 'granted');
        this.loadGA();
    },

    deny: function () {
        this.granted = false;
        localStorage.setItem('ga_consent', 'denied');
    },

    check: function () {
        const consent = localStorage.getItem('ga_consent');
        return consent === 'granted';
    },

    loadGA: function () {
        if (window.gaTag && this.granted) {
            window.dataLayer = window.dataLayer || [];
            function gtag() { dataLayer.push(arguments); }
            gtag('js', new Date());
            gtag('config', window.gaTag, {
                'anonymize_ip': true
            });
        }
    }
};

// Auto-load GA if consent previously granted
if (window.gaConsent.check()) {
    window.gaConsent.grant();
}
