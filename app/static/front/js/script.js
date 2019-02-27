jQuery(function ($) {

    'use strict';
    setInterval(function () {
        var event = new Date();
        var options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
        $('#date_time').html(event.toLocaleTimeString('fr-FR', options))
    }, 1000);
    // --------------------------------------------------------------------
    // Back to top
    // --------------------------------------------------------------------

    (function() {
        var offset = 220;
        var duration = 500;
        jQuery(window).scroll(function() {
            if (jQuery(this).scrollTop() > offset) {
                jQuery('.crunchify-top').fadeIn(duration);
            } else {
                jQuery('.crunchify-top').fadeOut(duration);
            }
        });
 
        jQuery('.crunchify-top').click(function(event) {
            event.preventDefault();
            jQuery('html, body').animate({scrollTop: 0}, duration);
            return false;
        })

    }());


    // --------------------------------------------------------------------
    // Owl Carousel Video Slider
    // --------------------------------------------------------------------

    (function() {
     $('.owl-carousel').owlCarousel({
         loop:true,
         margin:30,
         nav:true,
         responsive:{
             0:{
                 items:1
             },
             600:{
                 items:2
             },
             1000:{
                 items:3
             }
         }
        });

     }());

}); // JQuery end
