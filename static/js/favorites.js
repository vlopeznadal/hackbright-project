$(window).on("load", function () {
    $.get('/database', response => {
        if (response == "bi-heart-fill") {
            $('#heart').removeClass("bi-heart").addClass(`${response}`);
        } else if (response == "bi-fill") {
            $('#heart').removeClass("bi-heart").addClass(`${response}`);
        }
    });
});

$('#heart').on('click', (event) => {
    if ($('#heart').hasClass("bi-heart")) {
        $('#heart').removeClass('bi-heart');
        $('#heart').addClass('bi-heart-fill');
        event.preventDefault()
    $.get('/favorite', response => {
      });
    } else {
        $('#heart').removeClass('bi-heart-fill');
        $('#heart').addClass('bi-heart');
        event.preventDefault()
    $.get('/unfavorite', response => {
      });
    }
});