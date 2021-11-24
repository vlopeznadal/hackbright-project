// Once HTML document has been loaded
$(document).ready(function(){

  // Grabs the user's profile picture
  $.post('/get-profile-pic', response => {

    // Setting response to a variable
    let profile_pic = response

    // If the user's profile picture exists
    if (profile_pic != "False") {
      
      // Display user's profile picture on page
      $('#profile-pic-display').append('<img src="' + profile_pic + '" class="reviewer_photo"/>');
    
    // If user's profile picture doesn't exist
    } else {

      // Display default profile picture on page
      $('#profile-pic-display').append('<img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/>');
    }
  });
});