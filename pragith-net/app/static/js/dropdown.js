// Dropdown toggle with aria-expanded state management
function toggleDropdown(dropdownId) {
    var dropdown = document.getElementById(dropdownId);
    var button = dropdown ? dropdown.previousElementSibling : null;

    if (!dropdown) return;

    var isHidden = dropdown.classList.contains('hidden');

    // Close all other dropdowns
    document.querySelectorAll('[id$="-dropdown"]').forEach(function (dd) {
        if (dd.id !== dropdownId) {
            dd.classList.add('hidden');
            var btn = dd.previousElementSibling;
            if (btn && btn.hasAttribute('aria-expanded')) {
                btn.setAttribute('aria-expanded', 'false');
            }
        }
    });

    // Toggle current dropdown
    if (isHidden) {
        dropdown.classList.remove('hidden');
        if (button) button.setAttribute('aria-expanded', 'true');
    } else {
        dropdown.classList.add('hidden');
        if (button) button.setAttribute('aria-expanded', 'false');
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', function (event) {
    var isDropdownButton = event.target.closest('button[aria-controls]');
    if (!isDropdownButton) {
        document.querySelectorAll('[id$="-dropdown"]').forEach(function (dropdown) {
            dropdown.classList.add('hidden');
            var button = dropdown.previousElementSibling;
            if (button && button.hasAttribute('aria-expanded')) {
                button.setAttribute('aria-expanded', 'false');
            }
        });
    }
});
