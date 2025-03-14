/**
 * favorites.js - Favorite movies page interaction script
 * Handles the removal of favorite movies
 */

$(document).ready(function() {
    $('.remove-favorite').click(function() {
        var filmId = $(this).data('id');
        var card = $(this).closest('.col-md-3');

        if (confirm('Are you sure you want to remove this movie from your favorites?')) {
            $.ajax({
                type: 'POST',
                url: `/favorite/${filmId}/`,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                data: {
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(data) {
                    card.addClass('removing');
                    setTimeout(function() {
                        card.fadeOut('slow', function() {
                            $(this).remove();

                            // If there are no favorites left, show a message
                            if ($('.film-card').length === 0) {
                                $('.row').html(emptyFavoritesHTML);
                            }
                        });
                    }, 300);
                },
                error: function(xhr, status, error) {
                    console.error("Error removing favorite:", error);
                    alert("Failed to remove from favorites. Please try again.");
                }
            });
        }
    });
});