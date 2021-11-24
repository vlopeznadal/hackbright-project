// Once HTML document has been loaded
$(document).ready(function(){

    // Check database to see if cafe is already favorited
    $.get('/favorites-check', response => {

        // If cafe is favorited
        if (response == "True") {
            // Display filled heart
            $('#heart').removeClass("bi-heart").addClass("bi-heart-fill");

        //  If cafe is not favorited
        } else if (response == "False") {
            // Display unfilled heart
            $('#heart').removeClass("bi-heart").addClass("bi-heart");
        }
    });
});

// Listen for click of heart
$('#heart').on('click', (event) => {
    // If heart is unfilled
    if ($('#heart').hasClass("bi-heart")) {

        // Remove class that makes heart unfilled
        $('#heart').removeClass('bi-heart');

        // Add class that fills heart
        $('#heart').addClass('bi-heart-fill');

        // Prevent default action of the event from triggering
        event.preventDefault();

        // Add cafe to Favorites table of DB
        $.get('/favorite', response => {
        });

    } else {

        // Remove class that makes heart filled
        $('#heart').removeClass('bi-heart-fill');

        // Add class that makes heart unfilled
        $('#heart').addClass('bi-heart');

        // Prevent default action of the event from triggering
        event.preventDefault();

        // Remove cafe from Favorites table of DB
        $.get('/unfavorite', response => {
        });
    }
});