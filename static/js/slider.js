// Listen for changes to the range input with id 'rating'
$("#rating").on('change', function() {

    // Creating a variable for the current value of the range input
    let current_value = $('input[type=range]').val();

    // Display range's current value in span with class 'range-value' on details.html
    $('.range-value').html(" " + current_value);
  });

  // Listen for changes to the range input with id 'updatedrating'
  $("#updatedrating").on('change', function () {

    // Creating a variable for the current value of the range input
    let current_value = $('input[type=range]').val();

    // Display range's current value in span with class 'range-value' on details.html
    $('.range-value').html(" " + current_value);
  });
