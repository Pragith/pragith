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

function trackEvent(eventName, params) {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', eventName, params || {});
}

// Enrich all /contact CTA links with attribution + prefill params.
document.addEventListener('DOMContentLoaded', function () {
    const pagePath = window.location.pathname || '/';
    const marketing = window.appMarketing || {};
    const utmDefaults = marketing.utm_defaults || {};
    const projectRules = Array.isArray(marketing.project_type_rules) ? marketing.project_type_rules : [];
    const defaultProjectType = marketing.default_project_type || 'Other / Unsure';

    function projectTypeFromPath(path) {
        const lowerPath = (path || '').toLowerCase();
        for (const rule of projectRules) {
            const contains = (rule && rule.contains) ? String(rule.contains).toLowerCase() : '';
            if (contains && lowerPath.includes(contains)) {
                return rule.project_type || defaultProjectType;
            }
        }
        return defaultProjectType;
    }

    document.querySelectorAll('a[href^="/contact"]').forEach((link, idx) => {
        const href = link.getAttribute('href');
        if (!href) return;

        const url = new URL(href, window.location.origin);
        const ctaId = link.dataset.analytics || `cta-${pagePath.replace(/\W+/g, '-').replace(/^-+|-+$/g, '')}-${idx + 1}`;

        if (!url.searchParams.has('utm_source')) url.searchParams.set('utm_source', utmDefaults.source || 'pragith_net');
        if (!url.searchParams.has('utm_medium')) url.searchParams.set('utm_medium', utmDefaults.medium || 'website_cta');
        if (!url.searchParams.has('utm_campaign')) url.searchParams.set('utm_campaign', utmDefaults.campaign || 'inbound_consulting');
        if (!url.searchParams.has('utm_content')) url.searchParams.set('utm_content', ctaId);
        if (!url.searchParams.has('ref_page')) url.searchParams.set('ref_page', pagePath);
        if (!url.searchParams.has('cta_id')) url.searchParams.set('cta_id', ctaId);
        if (!url.searchParams.has('project_type')) url.searchParams.set('project_type', projectTypeFromPath(pagePath));

        // If user clicked from a package detail page, capture package slug for prefill context.
        const packageMatch = pagePath.match(/^\/packages\/([^/]+)$/);
        if (packageMatch && !url.searchParams.has('package')) {
            url.searchParams.set('package', packageMatch[1]);
        }

        link.setAttribute('href', `${url.pathname}?${url.searchParams.toString()}`);
    });

    // DRY instrumentation: track all marked CTA clicks consistently.
    document.addEventListener('click', function (event) {
        const el = event.target.closest('[data-analytics], a[href], button[type="submit"]');
        if (!el) return;

        const tag = (el.getAttribute('data-analytics') || '').trim();
        const href = el.getAttribute('href') || '';
        const label = tag || (href ? `link:${href}` : (el.textContent || '').trim().slice(0, 80));

        trackEvent('cta_click', {
            cta_id: label,
            page_path: pagePath,
            destination: href || '(form-submit)'
        });
    }, true);

    // Track all form submissions with endpoint context.
    document.querySelectorAll('form').forEach((form) => {
        form.addEventListener('submit', function () {
            const action = form.getAttribute('action') || pagePath;
            trackEvent('form_submit', {
                form_action: action,
                page_path: pagePath
            });
        });
    });
});
