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
           $('#ratings').append('<i class="bi bi-star-fill"></i>');
        }
        $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
        $('#reviewing').hide();
    });
  });

$(document).on('click', '.edit-review', function() { 
    $('#edit-form').html('<form name="updating" id="updating" action="/updating" method="POST"><div class="mb-3"><label for="rating" class="form-label">Rating</label><input type="range" class="form-range" min="1" max="5" id="rating" name="rating"> <label for="review" class="form-label">Review</label><textarea class="form-control" id="review" rows="3" name="review"></textarea></div><button type="submit" class="btn btn-primary">Submit</button></form>');
});

// $(document).on('submit', '#updating', function() { 
//     evt.preventDefault();

//     const formData = {
//         rating: $('#rating').val(),
//         review: $('#review').val(),
//       };
  
//     $.post('/updating', formData, response => {
//         $('#my-review').append('<div class="reviewer"><img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/> You</div>');
//         $('#my-review').append('<p id="ratings"></p>');
//         for(let i = 1; i <= response['rating']; i++) {
//            $('#ratings').append('<i class="bi bi-star-fill"></i>');
//         }
//         $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
//         $('#edit-form').hide();
//     });
// });

// $('#updating').on('submit', evt => {
//     evt.preventDefault();

//     const formData = {
//         rating: $('#rating').val(),
//         review: $('#review').val(),
//       };
  
//     $.post('/updating', formData, response => {
//         $('#my-review').append('<div class="reviewer"><img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/> You</div>');
//         $('#my-review').append('<p id="ratings"></p>');
//         for(let i = 1; i <= response['rating']; i++) {
//            $('#ratings').append('<i class="bi bi-star-fill"></i>');
//         }
//         $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
//         $('#edit-form').hide();
//     });
//   });