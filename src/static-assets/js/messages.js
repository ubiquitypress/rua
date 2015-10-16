var frm = $('#message_form');
frm.submit(function () {
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            data = $.parseJSON(data);

            $( "#message-list" ).prepend( '<div class="message "><div class="row message-container"><div class="col-md-2"><h3 style="margin-top: 15px;">' + $('#initials').val()  + '</h3></div><div class="col-md-10"><small>' + data.message + '</small></div><div class="col-md-12 message-date"><small>' + data.date_sent + '</small></div></div></div>' );
            $('#id_message').val("");
        },
        error: function(data) {
           $("#MESSAGE-DIV").html("Something went wrong!");
           console.log(data)
        }
    });
    return false;
});
var book_id = document.getElementById("book_id").value;

window.setInterval(function(){
    var last_message = $(".last_message:first").val();
    $.get('/book/'+ book_id +'/messages/', {last_message: last_message}, function(data){
        data = $.parseJSON(data);
        for (i = 0; i < data.messages.length; i++) { 

            $( "#message-list" ).prepend( '<div class="message message-green message-new"><div class="row message-container"><div class="col-md-10"><small>' + data.messages[i].message + '</small></div><div class="col-md-2"><h3>' + data.messages[i].initials  + '</h3></div><div class="col-md-12 message-date"><small>' + data.messages[i].date_sent + '</small></div></div><input class="last_message" type="hidden" value="'+ data.messages[i].message_id+'"></div>' );
            $('#id_message').val("");
            $('.message-new').fadeOut(1000);
            $('.message-new').fadeIn(1000);
        }
        data.messages = new Array();
    });

    $('.message-new').hover(function() {
        $(this).removeClass('message-new');
    });
  
}, 5000);

