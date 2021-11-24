// Once HTML document has been loaded
$(document).ready(function(){

  // Grabbing reviews from Reviews table in DB
  $.post('/user-reviews', response => {

    // Setting response to a variable (reviews)
    let review = response

    // Grabbing user's profile picture from User table in DB
    $.post('/get-profile-pic', response => {

      // Setting response to variable (profile picture)
      let profile_pic = response

      // If user has a profile picture set
      if (profile_pic != "False") {

        // Display profile picture from database in DIV with ID 'my-review'
        $('#my-review').append('<div class="reviewer"><img src="' + profile_pic + '" class="reviewer_photo"/> You</div>');

      // If user doesn't have a profile picture set
      } else {

        // Display a default profile picture in DIV with ID 'my-review'
        $('#my-review').append('<div class="reviewer"><img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/> You</div>');
      }

      // If a review by the current user for the current cafe exists
      if (review != "False") {

        // Create a paragraph with ID 'ratings' for ratings stars
        $('#my-review').append('<p id="ratings"></p>');

        // For the rating number
        for(let i = 1; i <= review['rating']; i++) {

          // Insert a filled star icon into paragraph with ID 'ratings'
          $('#ratings').append('<i class="bi bi-star-fill"></i> ');
        }

        // Display review date, text, and an edit button
        $('#my-review').append('<p>' + review['date']+'</p><p>"' + review['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
      }
    });
  });
});

// Listen for the submission of the review form
$('#reviewing').on('submit', evt => {

  // Prevent default action of the event from triggering
  evt.preventDefault();

  // Create a dictionary with the values of the rating and review inputs of the form
  const formData = {
    rating: $('#rating').val(),
    review: $('#review').val(),
  };

  // Grabbing user's profile picture from User table in DB
  $.post('/get-profile-pic', response => {

    // Setting response to variable (profile picture)
    let profile_pic = response

    // Empty out review DIV
    $('#my-review').empty();

    // If user has a profile picture set
    if (profile_pic != "False") {

      // Display profile picture from database in DIV with ID 'my-review'
      $('#my-review').append('<div class="reviewer"><img src="' + profile_pic + '" class="reviewer_photo"/> You</div>');

      // If user doesn't have a profile picture set
    } else {

      // Display a default profile picture in DIV with ID 'my-review'
      $('#my-review').append('<div class="reviewer"><img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/> You</div>');
    }
  });

  // Adding review to DB and displaying it on page
  $.post('/reviewing', formData, response => {

    // Create a paragraph with ID 'ratings' for ratings stars
    $('#my-review').append('<p id="ratings"></p>');

    // For number in rating
    for(let i = 1; i <= response['rating']; i++) {
      // Insert a filled star icon into paragraph with ID 'ratings'
      $('#ratings').append('<i class="bi bi-star-fill"></i> ');
    }

      // Display review date, text, and an edit button
      $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
      
      // Hide review form
      $('#reviewing').hide();
  });
});

// Listen for the submission of the edit form
$(document).on('submit', '#updating', function(evt) { 

  // Prevent default action of the event from triggering
  evt.preventDefault();

  // Create a dictionary with the values of the rating and review inputs of the form
  const formData = {
    updatedrating: $('#updatedrating').val(),
    updatedreview: $('#updatedreview').val(),
  };

  // Grabbing user's profile picture from User table in DB
  $.post('/get-profile-pic', response => {

    // Setting response to variable (profile picture)
    let profile_pic = response

    // Empyty out review DIV
    $('#my-review').empty();

    // If user has a profile picture set
    if (profile_pic != "False") {
  
      // Display profile picture from database in DIV with ID 'my-review'
      $('#my-review').append('<div class="reviewer"><img src="' + profile_pic + '" class="reviewer_photo"/> You</div>');
  
      // If user doesn't have a profile picture set
    } else {
  
      // Display a default profile picture in DIV with ID 'my-review'
      $('#my-review').append('<div class="reviewer"><img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/> You</div>');
    }
  });

  // Updating review in DB and displaying it on page
  $.post('/updating', formData, response => {

    // Create a paragraph with ID 'ratings' for ratings stars
    $('#my-review').append('<p id="ratings"></p>');

    // For number in rating
    for(let i = 1; i <= response['rating']; i++) {
      // Insert a filled star icon into paragraph with ID 'ratings'
      $('#ratings').append('<i class="bi bi-star-fill"></i> ');
    }
      // Display review date, text, and an edit button
      $('#my-review').append('<p>' + response['date']+'</p><p>"' + response['review'] + '"</p><button class="btn btn-primary edit-review">Edit Review</button>');
      
      // Hide edit form
      $('#updating').hide();

      // Clear out edit form 
      $('#updating').trigger("reset");

      // Creating a variable for the current value of the range input
      let current_value = $('input[type=range]').val();

      // Display updated range value once form is emptied (default value of 3)
      $('.range-value').html(" " + current_value);
  });
});


// Listening for click of edit review button
$(document).on('click', '.edit-review', function() { 

  // If the edit form is hidden
  if ($('#updating').is(":hidden")) {

    // Show edit form
    $('#updating').show();

    // Show DIV of edit form
    $('.edit-form').show();

    // Scroll to bottom of page to show opening of edit form
    $("html, body").animate({ scrollTop: $(document).height() }, "slow");
    // return false;
  }
  // If the edit form is showing
  else if ($('#updating').is(":visible")) {

    // Hide edit form
    $('#updating').hide();

    // Clear out editing form
    $('#updating').trigger("reset");

    // Creating a variable for the current value of the range input (default value of 3)
    let current_value = $('input[type=range]').val();

    // Display updated range value once form is emptied (default value of 3)
    $('.range-value').html(" " + current_value);

    // Hide DIV of edit form
    $('.edit-form').hide();
  }
});