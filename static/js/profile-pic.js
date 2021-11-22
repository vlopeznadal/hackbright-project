$(window).on("load", function () {
    $.post('/profile-pic', response => {
        let profile_pic = response
        if (profile_pic != "False") {
          $('#profile-pic-display').append('<img src="' + profile_pic + '" class="reviewer_photo"/>');
        } else {
          $('#profile-pic-display').append('<img src="/static/img/default_reviewer.jpg" class="reviewer_photo"/>');
        }
    });
  });