/**
 * review_form.js - Movie review form interaction script
 * Handles star rating interaction functionality
 */

$(document).ready(function() {
  // Star rating functionality
  $('.star').on('click', function() {
    const rating = $(this).data('rating');

    // Update visual stars
    $('.star').each(function(index) {
      if (index < rating) {
        $(this).html('<i class="fas fa-star"></i>');
      } else {
        $(this).html('<i class="far fa-star"></i>');
      }
    });

    // Update displayed rating text
    $('.selected-rating').text(rating);

    // Update hidden radio button
    $(`input[name="rating"][value="${rating}"]`).prop('checked', true);
  });

  // Hover effect
  $('.star').hover(
    function() {
      const hoverRating = $(this).data('rating');
      $('.star').each(function(index) {
        if (index < hoverRating) {
          $(this).html('<i class="fas fa-star"></i>');
        }
      });
    },
    function() {
      // Restore to selected rating when mouse leaves
      const selectedRating = $('input[name="rating"]:checked').val() || 0;
      $('.star').each(function(index) {
        if (index < selectedRating) {
          $(this).html('<i class="fas fa-star"></i>');
        } else {
          $(this).html('<i class="far fa-star"></i>');
        }
      });
    }
  );

  // Form validation before submission
  $('form').on('submit', function(e) {
    const rating = $('input[name="rating"]:checked').val();
    const title = $('#' + $('label[for="{{ form.title.id_for_label }}"]').attr('for')).val().trim();
    const content = $('#' + $('label[for="{{ form.content.id_for_label }}"]').attr('for')).val().trim();

    // Client-side validation can be added here if needed
    // For example, checking if a rating is selected, title is filled, etc.
  });
});
