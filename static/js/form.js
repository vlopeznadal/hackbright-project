$(window).on("load", function () {
  $.post('/reviews', response => {
    if (response != "False"){
      $('#my-review').append('<div class="reviewer"><img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/> You</div>');
    $('#my-review').append('<p id="ratings"></p>');
    for(let i = 1; i <= response['rating']; i++) {
       $('#ratings').append('<i class="bi bi-star-fill"></i> ');
    }
    $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
    }
  });
});


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
           $('#ratings').append('<i class="bi bi-star-fill"></i> ');
        }
        $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
        $('#updating').hide();
        $('#updating').trigger("reset");
    });
  });



  $(document).on('click', '.edit-review', function() { 
    if ($('#updating').is(":hidden")) {
      $('#updating').show();
      $('.edit-form').show();
      $("html, body").animate({ scrollTop: $(document).height() }, "slow");
      return false;
    }
    else if ($('#updating').is(":visible")) {
      $('#updating').hide();
      $('#updating').trigger("reset");
      $('.edit-form').hide();
    }
});