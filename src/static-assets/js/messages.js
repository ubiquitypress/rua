var frm = $('#message_form');
frm.submit(function () {
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            data = $.parseJSON(data);

            if ($('#message-list > div').length %2 != 0){
                var style = 'even'
            }else{
                var style = 'odd'
            }

            $( "#message-list" ).prepend( '<div class="message ' + style + '"><div class="row message-container"><div class="col-md-2"><h3 style="margin-top: 15px;">' + $('#initials').val()  + '</h3></div><div class="col-md-10"><small>' + data.message + '</small></div><div class="col-md-12 message-date"><small>' + data.date_sent + '</small></div></div></div>' );
            $('#id_message').val("");
        },
        error: function(data) {
           $("#MESSAGE-DIV").html("Something went wrong!");
           console.log(data)
        }
    });
    return false;
});