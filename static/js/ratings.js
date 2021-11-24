// Creating variable to set star width
let starWidth = 16;

// Creating stars method
$.fn.stars = function() {

  // For each span with class 'stars' 
  return $(this).each(function() {

    // Determine width of stars based on number in span
    $(this).html($('<span />').width(Math.max(0, (Math.min(5, parseFloat($(this).html())))) * starWidth));
  });
}

// Once HTML document has been loaded
$(document).ready(function() {

  // Apply the stars method to the spans with class 'stars'
  $('span.stars').stars();
});