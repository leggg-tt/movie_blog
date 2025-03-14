/**
 * blog-detail.js - Blog detail page interaction script
 */

$(document).ready(function() {
    // Comment form submission
    $('#comment-form').submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(data) {
                // Show success message
                $('#comment-success').fadeIn().delay(2000).fadeOut();

                // Add new comment to the list
                var newComment = `
                    <div class="comment-item">
                        <div class="comment-header d-flex justify-content-between">
                            <div class="comment-author">
                                <img src="${$('.avatar-img').attr('src')}" alt="${data.username}" class="avatar-img-sm">
                                <span class="author-name">${data.username}</span>
                            </div>
                            <span class="comment-date">${data.created_at}</span>
                        </div>
                        <div class="comment-content">
                            ${data.content}
                        </div>
                    </div>
                `;

                // Remove "No comments" prompt if it exists
                if ($('#comments-list .no-comments').length) {
                    $('#comments-list').empty();
                }

                // Add to the top of the comments list
                $('#comments-list').prepend(newComment);

                // Clear the form
                $('#comment-form')[0].reset();

                // Update comment count
                var commentCountText = $('.comments-title').text();
                var commentCount = parseInt(commentCountText.match(/\d+/)[0]) + 1;
                $('.comments-title').text('Comments (' + commentCount + ')');
            }
        });
    });

    // Comment area animation effects
    $('.comment-item').hover(
        function() {
            $(this).css('transform', 'translateY(-2px)');
            $(this).css('box-shadow', '0 3px 10px rgba(0,0,0,0.08)');
        },
        function() {
            $(this).css('transform', 'translateY(0)');
            $(this).css('box-shadow', 'none');
        }
    );
});