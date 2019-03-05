jQuery(function ($) {

    'use strict';
    setInterval(function () {
        var event = new Date();
        var options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
        $('#date_time').html(event.toLocaleTimeString('fr-FR', options));
        $('#copyright_date').html(event.getFullYear());
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

    $("#contact_form").on('submit', function (e) {
        e.preventDefault();
        //get input field values
        var user_name = $('input[name=name]').val();
        var user_email = $('input[name=email]').val();
        var user_subject = $('input[name=subject]').val();
        var user_message = $('textarea[name=message]').val();
        var proceed = true;
        if (user_name === "") {
            $('input[name=name]').css('border-color', 'red');
            proceed = false;
        }
        if (user_email === "") {
            $('input[name=email]').css('border-color', 'red');
            proceed = false;
        }
        if (user_subject === "") {
            $('input[name=subject]').css('border-color', 'red');
            proceed = false;
        }
        if (user_message === "") {
            $('textarea[name=message]').css('border-color', 'red');
            proceed = false;
        }
        if (proceed) {
            //data to be sent to server
            var post_data = {
                'name': user_name,
                'email': user_email,
                'subject': user_subject,
                'message': user_message
            };
            var output;
            //Ajax post data to server
            var contact_url = $(this).attr('action');
            $.post(contact_url, post_data, function (response) {
                //load json data from server and output message
                if (response.type === 'error') {
                    output = '<div class="error">' + response.text + '</div>';
                } else {
                    output = '<div class="success">' + response.text + '</div>';
                    //reset values in all input fields
                    $('#contact_form input').val('');
                    $('#contact_form textarea').val('');
                }
                $("#result").hide().html(output).slideDown().delay(4000).slideUp();
            }, 'json');
        }
    });

    $("#register_form").on('submit', function (e) {
        e.preventDefault();
        var post_data = {
            'name': $('#name').val(),
            'email': $('#email').val(),
            'phone': $('#phone').val(),
            'facebook': $('#facebook').val(),
            'password': $('#password').val()
        };
        var output;
        //Ajax post data to server
        var url = $(this).attr('action');
        $.post(url, post_data, function (response) {
            //load json data from server and output message
            if (response.type === 'error') {
                output = '<div class="alert alert-danger" role="alert">' + response.text + '</div>';
            } else {
                output = '<div class="alert alert-success" role="alert">' + response.text + '</div>';
                //reset values in all input fields
                $('#register_form input').val('');
            }
            $("#result").hide().html(output).slideDown().delay(10000).slideUp();
        }, 'json');
    });

}); // JQuery end
