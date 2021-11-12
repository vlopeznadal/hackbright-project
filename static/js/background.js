$(window).on("load", function () {
    const ranBackground = "/static/img/backgrounds/background-" + Math.floor((Math.random() * 2) + 1) + ".jpg";
    $(".background").css("background-image", "url("+ranBackground + ")");
});
