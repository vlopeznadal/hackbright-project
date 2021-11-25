// Once HTML document has been loaded
$(document).ready(function(){
    // Setting variable to randomly selected background img URL
    const ranBackground = "/static/img/backgrounds/background-" + Math.floor((Math.random() * 5) + 1) + ".jpg";

    // Setting the CSS property 'background-image' of DIV with class 'background' to 
    // the randomly selected background 
    $(".background").css("background-image", "url("+ranBackground + ")");
});
