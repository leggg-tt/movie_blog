/**
 * auth.js - Authentication page script
 * Used to enhance forms on login and registration pages
 */

// Execute after the page has loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add classes to Django form controls
    enhanceFormControls();
});

/**
 * Add styling classes to form controls
 */
function enhanceFormControls() {
    // Find all form controls
    const formControls = document.querySelectorAll('input[type="text"], input[type="password"], input[type="email"]');

    // Add classes to each control
    formControls.forEach(function(input) {
        input.classList.add('form-control', 'auth-form-control');
    });
}