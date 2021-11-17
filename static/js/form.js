$('#reviewing').on('submit', evt => {
    evt.preventDefault();

    const formData = {
        rating: $('#rating').val(),
        review: $('#review').val(),
      };
  
    $.post('/reviewing', formData, response => {
        $('#my-review').append('<div class="reviewer"><img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/> You</div>');
        $('#my-review').append('<p id="ratings"></p>');
        for(let i = 1; i <= response['rating']; i++) {
           $('#ratings').append('<i class="bi bi-star-fill"></i> ');
        }
        $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
        $('#reviewing').hide();
    });
  });

$(document).on('click', '.edit-review', function() { 
    $('.edit-form').show();
});

$(document).on('submit', '#updating', function(evt) { 
    evt.preventDefault();

    const formData = {
        updatedrating: $('#updatedrating').val(),
        updatedreview: $('#updatedreview').val(),
      };
  
    $.post('/updating', formData, response => {
        $('#my-review').empty();
        $('#my-review').append('<div class="reviewer"><img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/> You</div>');
        $('#my-review').append('<p id="ratings"></p>');
        for(let i = 1; i <= response['rating']; i++) {
           $('#ratings').append('<i class="bi bi-star-fill"></i>');
        }
        $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
        $('#updating').hide();
    });
  });