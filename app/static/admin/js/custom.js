$(function () {

    //Enable iCheck plugin for checkboxes
    //iCheck for checkbox and radio inputs
    $('.mailbox-messages input[type="checkbox"]').iCheck({
        checkboxClass: 'icheckbox_flat-blue',
        radioClass: 'iradio_flat-blue'
    });

    //Enable check and uncheck all functionality
    $(".checkbox-toggle").click(function () {
        var clicks = $(this).data('clicks');
        if (clicks) {
            //Uncheck all checkboxes
            $(".mailbox-messages input[type='checkbox']").iCheck("uncheck");
            $(".fa", this).removeClass("fa-check-square-o").addClass('fa-square-o');
        } else {
            //Check all checkboxes
            $(".mailbox-messages input[type='checkbox']").iCheck("check");
            $(".fa", this).removeClass("fa-square-o").addClass('fa-check-square-o');
        }
        $(this).data("clicks", !clicks);
    });

    //Handle starring for glyphicon and font awesome
    $(".mailbox-star").click(function (e) {
        e.preventDefault();
        //detect type
        var $this = $(this).find("a > i");
        var glyph = $this.hasClass("glyphicon");
        var fa = $this.hasClass("fa");

        //Switch states
        if (glyph) {
            $this.toggleClass("glyphicon-star");
            $this.toggleClass("glyphicon-star-empty");
        }

        if (fa) {
            $this.toggleClass("fa-star");
            $this.toggleClass("fa-star-o");
        }
    });

    $('.summernote').summernote();
    window.alert = function (message, type = 'red') {
        $.alert({ title: 'Alert!', content: message, type: type });
    };
    window.confirmation = function (content = "", callback, title = "Confirmation", dialogType = "dark", btnClass = "btn-primary") {
        $.confirm({
            title: title,
            content: content,
            columnClass: 'col-md-5 col-md-offset-4',
            icon: 'fa fa-question-circle',
            type: dialogType,
            buttons: {
                ok: {
                    text: "OK",
                    btnClass: btnClass,
                    keys: ['enter'],
                    action: callback
                },
                cancel: {
                    text: 'Annuler'
                }
            }
        });
    };

    $('.delete').click(function (event) {
        event.preventDefault();
        const message = $(this).attr('title');
        const goto = $(this).attr('href');
        confirmation(message, function () {
            window.location.href = goto;
        })
    });
}
);