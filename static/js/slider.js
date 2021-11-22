$("#rating").on('change', function() {
    let current_value = $('input[type=range]').val();
    $('.bubble').html(" " + current_value);
  });

  $("#updatedrating").on('change', function () {
    let current_value = $('input[type=range]').val();
    $('.bubble').html(" " + current_value);
  });
