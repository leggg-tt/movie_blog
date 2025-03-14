/**
 * edit_profile.js - Profile edit page interaction script
 * Provides avatar preview and file upload interaction functionality
 */

// Preview the selected avatar image
document.getElementById(avatarInputId).addEventListener('change', function(e) {
    if (e.target.files && e.target.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('avatar-preview-image').src = e.target.result;
        }
        reader.readAsDataURL(e.target.files[0]);

        // Update the file name display
        var fileName = e.target.files[0].name;
        var fileLabel = document.querySelector('.custom-file-label');
        if (fileLabel) {
            fileLabel.innerHTML = '<i class="fas fa-check me-2"></i>' + fileName;
            fileLabel.classList.add('file-selected');
        }
    }
});