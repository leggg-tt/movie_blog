/**
 * common.js - General JavaScript functionality
 * Contains JavaScript functions and initialization code used across the entire website
 */

// Confirmation dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// After the page has loaded
$(document).ready(function() {
    // Enable all tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Auto-hide alert messages
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
});