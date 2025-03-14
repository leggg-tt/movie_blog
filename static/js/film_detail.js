/**
 * film-detail.js - Movie detail page functionality
 * Handles interactions on the movie detail page, including favorites and reviews
 */

$(document).ready(function() {
    // Favorite functionality
    $('#favorite-btn').click(function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: $(this).data('url'),
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data) {
                if (data.is_favorite) {
                    $('#favorite-btn').removeClass('not-favorited').addClass('favorited');
                    $('#favorite-btn').html('<i class="fas fa-heart"></i> Already saved');
                } else {
                    $('#favorite-btn').removeClass('favorited').addClass('not-favorited');
                    $('#favorite-btn').html('<i class="far fa-heart"></i> Collect');
                }
            }
        });
    });

    // Star rating functionality
    var $stars = $('.star-rating-item');
    var $selectedRating = $('.selected-rating');
    var $hiddenInput = $('#id_rating_hidden');

    // Hover effect for stars
    $stars.hover(
        function() {
            var rating = $(this).data('rating');
            // Reset all stars
            $stars.removeClass('fas').addClass('far');
            // Fill the hovered star and previous stars
            $stars.each(function(index) {
                if (index < rating) {
                    $(this).removeClass('far').addClass('fas');
                }
            });
            $selectedRating.text(rating);
        },
        function() {
            // Restore to the selected rating when mouse leaves
            var selectedRating = $hiddenInput.val();
            updateStars(selectedRating);
        }
    );

    // Click to select rating
    $stars.click(function() {
        var rating = $(this).data('rating');
        $hiddenInput.val(rating);
        updateStars(rating);
    });

    // Update star display
    function updateStars(rating) {
        $stars.removeClass('fas active').addClass('far');
        $stars.each(function(index) {
            if (index < rating) {
                $(this).removeClass('far').addClass('fas active');
            }
        });
        $selectedRating.text(rating);
    }

    // Review functionality
    $('#review-form').submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(data) {
                $('#average-rating').text(data.average_rating.toFixed(1));
                $('#rating-count').text(data.review_count);
                $('#review-success').fadeIn().delay(2000).fadeOut();

                // Clear the form
                $('#review-form')[0].reset();
                updateStars(0);

                // Refresh the page to show the new review
                setTimeout(function() {
                    location.reload();
                }, 2000);
            }
        });
    });

    // Review like functionality
    $('.like-button').click(function() {
        var button = $(this);
        var reviewId = button.data('review-id');

        $.ajax({
            type: 'POST',
            url: "/review/" + reviewId + "/like/",
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
            },
            success: function(data) {
                var likeCount = button.find('.like-count');
                likeCount.text(data.like_count);

                if (data.is_liked) {
                    button.removeClass('not-liked').addClass('liked');
                } else {
                    button.removeClass('liked').addClass('not-liked');
                }
            }
        });
    });
});